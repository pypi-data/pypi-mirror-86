import os
import sys
import logging  # 引入logging模块
logging.basicConfig(level=logging.NOTSET)  # 设置日志级别
import threading
import time

def add_path(path):
    global RESET_LIB
    if path not in sys.path:
        sys.path.insert(0, path)
        RESET_LIB = True

this_dir = os.path.dirname(__file__)

# Add lib to PYTHONPATH
lib_path = os.path.join(this_dir, '../')
add_path(lib_path)

from pubsub import subscriber, publisher

def reset_robot_config_path(env ,root, folder):
    try:
        os.environ[env] = os.path.join(root, folder)
    except Exception as e:
        os.environ.setdefault(env,os.path.join(root, folder))

class SwitchSignalTest():
    def __init__(self):
        # use ROBOT_CONFIGS
        _root = sys.path[0]
        print('run in root: {}'.format(_root))
        reset_robot_config_path('ROBOT_CONFIGS', _root, 'testcases/switch_configs')
        from pubsub.configs import ROBOT_CFGS
        self.ROBOT_CFGS = ROBOT_CFGS
        print(self.ROBOT_CFGS)
        self.root = _root
        self.changeTarget()
        self.sendMsg()                

    def changeTarget(self):        
        self.switch_config = self.ROBOT_CFGS['control_singal_load_track_feature']
        _source = self.switch_config['source']
        _host = self.switch_config['host']
        _port = self.switch_config['port']
        _db = self.switch_config['db']
        _name = self.switch_config['name']
        # self._name_feedback = self.switch_config['name_feedback']
        _topic = self.switch_config['topic']
        # self._topic_feedback = self.switch_config['topic_feedback']
        self.tgtpub = publisher.Publisher(name=_name,
                host=_host, port=_port, db=_db)
    

    def sendMsg(self):        
        self.model_config = self.ROBOT_CFGS['switch_send']
        _source = self.model_config['source']
        _host = self.model_config['host']
        _port = self.model_config['port']
        _db = self.model_config['db']
        _name = self.model_config['name']
        # self._name_feedback = self.switch_config['name_feedback']
        _topic = self.model_config['topic']
        # self._topic_feedback = self.switch_config['topic_feedback']
        self.msgpub = publisher.Publisher(name=_name,
                host=_host, port=_port, db=_db)
    
    def send_listener(self):
        target_change_listener = threading.Thread(target=self.sendTarget, args=())        
        target_model_listener = threading.Thread(target=self.sendMsgToRecog, args=()) 
        self.listeners = [target_change_listener, target_model_listener]
        for listener in self.listeners:
            listener.start()


    def sendTarget(self):
        while True:
            self.tgtpub.send(self.switch_config['topic'], 'target change {}\n'.format(time.time()))
            time.sleep(1)
        
    def sendMsgToRecog(self):
        while True:
            self.msgpub.send(self.model_config['topic'], 'target model {}\n'.format(time.time()))        
            time.sleep(2)


if __name__ == '__main__':
    switch = SwitchSignalTest()        
    switch.send_listener()
        # print('send {} \n'.format(msg))
        