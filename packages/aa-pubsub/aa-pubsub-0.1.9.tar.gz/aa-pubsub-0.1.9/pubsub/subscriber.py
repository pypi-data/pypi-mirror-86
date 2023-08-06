import logging
from concurrent.futures import ThreadPoolExecutor
import threading
import time

import redis

gitem = None


def skip_frame(callback):
    global gitem
    while 1:
        if callback and gitem is not None:
            callback(gitem['data'], 'robot_reids_sub', '', time.time())


class Subscriber(object):
    # _instance_lock = threading.Lock()

    def __init__(self,
                 name='robot_reids_sub',
                 host='127.0.0.1',
                 port='6379',
                 db=3,
                 health_check_interval=1,
                 max_workers=20):
        self.item = None        
        self.name = name
        self.host, self.port = host, port
        self.db, self.health_check_interval = db, health_check_interval
        self.pool = redis.ConnectionPool(host=host, port=port, db=self.db)
        self.threadpools = ThreadPoolExecutor(max_workers=max_workers)
        self.listen = {}
        self.recved = {}        
        logging.debug('create a redis pool at {}:{} for subscriber {}'.format(
            host, port, name))

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(Subscriber, '_instance'):
    #         with Subscriber._instance_lock:
    #             if not hasattr(Subscriber, '_instance'):
    #                 Subscriber._instance = object.__new__(cls)
    #     return Subscriber._instance

    def finish_task(self, task):
        # ret = task.result()
        # if ret is None:
        #     print('call nothing back \n')
        # else:
        #     print('finish callback at {} \n'.format(ret))
        print('finish callback at {} \n'.format(time.time()))
        
    def start_listen(self, topic, item, callback=None):
        # t = threading.Thread(target=self.pop_listen, args=(topic, callback))
        # t.start()
        # logging.info('start a new thread {}'.format(topic))
        # self.listen[topic] = t
        name, _timestamp = self.name, time.time()
        task = self.threadpools.submit(callback, item['data'], name, topic, _timestamp)
        print('get a new thread {} at {} \n'.format(threading.current_thread().name, _timestamp))
        logging.info('get a new thread {} at {} \n'.format(threading.current_thread().name, _timestamp))
        task.add_done_callback(self.finish_task)
        # logging.info('task done at {}'.format(time.time()))


    def get_connection(self):
        conn = redis.StrictRedis(connection_pool=self.pool,
                                 db=self.db,
                                 socket_connect_timeout=4,
                                 retry_on_timeout=True,
                                 socket_timeout=4)        
        return conn

    def pop_listen(self, topic, item, callback):
        _timestamp = None              
        name = self.name        
        if callback and item and item['channel'] == topic.encode():
            _timestamp = time.time()
            t = threading.Thread(target=callback, args=(item['data'], name, topic, _timestamp))
            t.start()
            # callback(item['data'], name, topic, _timestamp)
            # self.start_listen(topic, item, callback=callback)
        return _timestamp

    def recv(self, topic, callback=None):
        # global gitem
        # if topic not in self.listen:
        #     self.start_listen(topic, callback)
        # rc = Subscriber._instance.get_connection()
        # name = Subscriber._instance.name
        rc = self.get_connection()
        name = self.name
        ps = rc.pubsub()
        # ps.check_health()
        ps.subscribe(topic)
        try:
            if callback:
                for item in ps.listen():
                    self.item = item
                    # callback with threadpool
                    # self.start_listen(topic, item, callback)
                    self.pop_listen(topic, item, callback)
                    # self.recved[topic] = True
                    # if callback:
                    #     callback(item['data'], name, topic, time.time())
                    logging.debug(
                        'Redis server {}\'s top {} subscribe a data at {}.'.format(
                            name, topic, time.time()))
        except redis.exceptions.ConnectionError:
            logging.error('connect close by server, retry...')
            # host, port = \
            #     Subscriber._instance.host, Subscriber._instance.port
            # Subscriber._instance.rc = Subscriber._instance.get_connection()
            host, port = \
                self.host, self.port
            self.rc = self.get_connection()
            logging.error('reconnect at {}:{}'.format(host, port))
            self.recv(topic, callback=callback)
