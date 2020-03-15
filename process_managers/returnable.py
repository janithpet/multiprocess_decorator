import multiprocessing as mp
from multiprocessing.managers import SyncManager

def _queued_start_process(f, q, lock, return_object):
    p = mp.Process(target=f, args=[q, lock, return_object])
    p.start()

    return p

def joinable_returnable_process_manager(n, ):

    '''
    This decorator runs n processes to complete a list of tasks given to the decorated function. It waits until all compuations have completed, and returns a list of results.
    Keep in mind that the order of the list is not preserved; the output list will be in the order that each process completes its task.
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
            processes = [[q.put(None), _queued_start_process(f, q, lock, return_object)] for i in range(n)]

            [p[1].join() for p in processes]
            return return_object
        return wrapper
    return faux_decorator