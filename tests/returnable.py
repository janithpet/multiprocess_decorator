from process_managers.returnable import joinable_returnable_process_manager
from workers.returnable import returnable_standard_worker

import time

@joinable_returnable_process_manager(7, )
@returnable_standard_worker
def f(x):
    time.sleep(1)
    return x*2

def timer(f, *args):
    st = time.time()

    rv = f(*args)

    print(time.time()- st)

    return rv

if __name__ == '__main__':
    # print(mp.current_process().pid)
    args = [
        [[1], {}],
        [[2], {}],
        [[3], {}],
        [[4], {}],
        [[5], {}],
        [[6], {}],
        [[1], {}],
        [[2], {}],
        [[3], {}],
        [[4], {}],
        [[5], {}],
        [[6], {}],
    ]

    rv = timer(f, args)
    print(rv)