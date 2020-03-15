from core.workers import standard_worker_decorator
from core.workers import standard_worker

import multiprocessing as mp
from multiprocessing.managers import SyncManager
import socket
import pickle

from time import sleep
from functools import partial

def start_process(f, q, lock):
    p = mp.Process(target=f, args=[q, lock])
    p.start()

    return p

def multi_decorator(n):
    def faux_decorator(f):
        def wrapper(list_of_parameters):
            q = mp.Queue()
            lock = mp.Lock()
            [q.put(item) for item in list_of_parameters]
            [(q.put(None), start_process(f, q, lock)) for i in range(n)]

        return wrapper
    return faux_decorator

def queued_start_process(f, q, lock, return_object):
    p = mp.Process(target=f, args=[q, lock, return_object])
    p.start()

    return p

def joinable_returnable_process_manager(n, ):

    '''
    This decorator runs n processes to complete a list of tasks given to the decorated function. It waits until all compuations have completed, and returns a list of results.
    :param n: Number of processes to run in parallel
    :return: List of results
    '''

    manager = SyncManager()
    manager.start()
    return_object = manager.list()

    def faux_decorator(f):
        def wrapper(list_of_parameters):
            q = manager.Queue()
            lock = manager.Lock()
            [q.put(item) for item in list_of_parameters]
            processes = [[q.put(None), queued_start_process(f, q, lock, return_object)] for i in range(n)]

            [p[1].join() for p in processes]
            return return_object
        return wrapper
    return faux_decorator


def socket_multi_decorator(n, port=9000):
    host = 'localhost'
    s = socket.socket()
    s.bind((host, port))
    def faux_decorator(f):
        def wrapper(list_of_parameters):
            q = mp.Queue()
            lock = mp.Lock()
            [start_process(f, q, lock) for i in range(n)]

            [q.put(item) for item in list_of_parameters]
            while True:
                try:
                    s.listen(1)
                    conn, addr = s.accept()
                    data = conn.recv(1024)
                    data = pickle.loads(data)

                    if data == 'exit':
                        [q.put(None) for i in range(n)]
                        conn.close()
                        s.close()
                        break
                    else:
                        q.put(data)
                except Exception as e:
                    print(e)
                    conn.close()
                    s.close()
                    exit()
        return wrapper
    return faux_decorator

# def smart_socket_multi_decorator(port=9001):



if __name__ == '__main__':
    @multi_decorator(3)
    @standard_worker_decorator
    def f(*args, **kwargs):
        print(f'Input: {args}, {kwargs}')
        # sleep(5)
        return None


    list_of_parameters= ['testing', 'blah', 'blah']
    f(list_of_parameters)

