from core.main import multi_decorator, socket_multi_decorator, joinable_returnable_process_manager
from core.workers import *

import multiprocessing as mp
from multiprocessing.managers import SyncManager

import time


@multi_decorator(3)
@standard_worker_decorator
def f(*args):
    print(args)
    return None

@socket_multi_decorator(30)
@setup_worker_decorator
class foo:
    def __init__(self):
        pass

    def setup(self, *args, **kwargs):
        print(mp.current_process().pid, ' setting up with inputs: ', args, kwargs)

    def run(self, *args, **kwargs):
        print(mp.current_process().pid, 'running with inputs: ', args, kwargs)
        time.sleep(2)


manager = SyncManager()
manager.start()
return_object = manager.list()

@joinable_returnable_process_manager(10, )
@returnable_standard_worker
def f(*args):
    time.sleep(1)
    return args[0]

def timer(f, *args):
    st = time.time()

    rv = f(*args)

    print(time.time()- st)

    return rv


if __name__ == '__main__':
    # print(mp.current_process().pid)
    args = [
        [[{1: 10}], {}],
        [[{2: 20}],  {}],
        [[{3: 30}],  {}],
        [[{3: 30}], {}],
        [[{1: 10}], {}],
        [[{2: 20}], {}],
        [[{3: 30}], {}],
        [[{1: 10}], {}],
        [[{2: 20}], {}],
        [[{3: 30}], {}],
        [[{1: 10}], {}],
        [[{2: 20}], {}],
        [[{3: 30}], {}],
    ]

    timer(f, args)




