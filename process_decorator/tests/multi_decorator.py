from process_decorator.core.main import multi_decorator, socket_multi_decorator
from process_decorator.core.workers import *

import multiprocessing as mp
from time import sleep
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
        sleep(2)

if __name__ == '__main__':
    params = list(range(100))
    foo(params)



