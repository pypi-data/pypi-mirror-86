
import time
import threading
import os
import sys

import cv2

def add_path(path):
    global RESET_LIB
    if path not in sys.path:
        sys.path.insert(0, path)
        RESET_LIB = True

this_dir = os.path.dirname(__file__)

# Add lib to PYTHONPATH
lib_path = os.path.join(this_dir, '../')
add_path(lib_path)

from pubsub import camera
from pubsub.configs import ROBOT_CFGS

img = None

def _detect_trace(pdata, *args):    
    global img
    if 1 == pdata :
        print('!!!!!!!!!!! heart beat')
    else:
        name, topic, _timestamp = args        
        img, _ = camera.unpackImage(pdata)
        print('>>>>>>>>>>> get {} {}, pick at {} send at {} rec at {} \n'.format(name, topic, _, _timestamp, time.time()))
        # do what you want in your own process
        time.sleep(2)
        
    return time.time()


if __name__ == '__main__':
    robot_configs = ROBOT_CFGS['mono']
    _source = robot_configs['source']
    _name = robot_configs['name']
    _host = robot_configs['host']
    _port = robot_configs['port']
    _db = robot_configs['db']

    task = camera.CameraSub(pipe=int(_source),
                            name=_name,
                            host=_host,
                            port=_port,
                            db=int(_db))
    t = threading.Thread(target=task.subscribe, args=(robot_configs['topic'], _detect_trace))
    t.start()
    # (callback=_detect_trace)
    print('try to subscribe')
    while True:
        if img is None:
            continue
        cv2.imshow('process', img)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()        
