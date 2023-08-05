import os
import sys

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
        self.root = _root
        self.switch_config = ROBOT_CFGS['switch_send']
        self._source = self.switch_config['source']
        self._host = self.switch_config['host']
        self._port = self.switch_config['port']
        self._db = self.switch_config['db']
        self._name = self.switch_config['name']
        # self._name_feedback = self.switch_config['name_feedback']
        self._topic = self.switch_config['topic']
        # self._topic_feedback = self.switch_config['topic_feedback']
        self.pub = publisher.Publisher(name=self._name,
                host=self._host, port=self._port, db=self._db)
        self.start_listeners()      

    def start_listeners(self):        
        target_change_listener = threading.Thread(target=self.listen_to_target_change, args=())        
        target_model_listener = threading.Thread(target=self.listen_to_target_model, args=()) 
        self.listeners = [target_change_listener, target_model_listener]
        for listener in self.listeners:
            listener.start()

    def process_target_change_signal(self, pdata, *args):
        print('>> process target change signal: {} at {} with {} \n'.format(pdata, time.time(), args))
        time.sleep(3)
        print('>> rework target change signal: {} at {} \n'.format(pdata, time.time()))

    def process_target_model_signal(self, pdata, *args):
        print('>> process target model signal: {} at {} with {} \n'.format(pdata, time.time(), args))
        time.sleep(3)
        print('>> rework target model signal:{} at {} \n'.format(pdata, time.time()))

    def listen_to_target_change(self):
        target_config = self.ROBOT_CFGS['control_singal_load_track_feature']
        name, host, port, db, topic = target_config['name'], target_config[
            'host'], target_config['port'], target_config['db'], target_config[
                'topic']
        sub = subscriber.Subscriber(name=name, host=host, port=port, db=db)
        print('>> listen_to_target_change call recv at {}'.format(time.time()))
        sub.recv(topic, self.process_target_change_signal)

    def listen_to_target_model(self):
        target_config = self.ROBOT_CFGS['switch_send']
        name, host, port, db, topic = target_config['name'], target_config[
            'host'], target_config['port'], target_config['db'], target_config[
                'topic']
        sub = subscriber.Subscriber(name=name, host=host, port=port, db=db)
        print('>> listen_to_target_model call recv at {}'.format(time.time()))
        sub.recv(topic, self.process_target_model_signal)
        # target_model_listener = threading.Thread(target=sub.recv, args=(topic, self.process_target_model_signal))
        # target_model_listener.start()


if __name__ == '__main__':
    switch = SwitchSignalTest()    
