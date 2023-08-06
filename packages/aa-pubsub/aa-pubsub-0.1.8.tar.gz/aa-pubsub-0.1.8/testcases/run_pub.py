
import threading
import time
import os
import sys

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

def callback(pdata, *args):
    if pdata == 1:
        print('')
        return
    print('callback: {}'.format(pdata))

name = 'test_pub'

def listener():
    sub = subscriber.Subscriber(name)
    sub.recv(name, callback)

if __name__ == '__main__':
    print('start thread')
    thread = threading.Thread(target=listener, args=())
    thread.start()
    pub = publisher.Publisher(name)
    while True:
        msg = time.time()
        pub.send(name, msg)
        print(msg)
        time.sleep(10)