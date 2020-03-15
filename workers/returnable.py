import multiprocessing as mp

def returnable_standard_worker(f):
    '''
    A decorator that adds the outputs to a return object. This is specified in the process decorator.
    :param f:
    :return:
    '''
    def wrapper(q, lock, return_object):
        while True:
            _args = q.get()
            try:
                args, kwargs = _args
            except Exception as e:
                args = _args
                if args is not None:
                    raise TypeError
            if args is not None:
                rv = f(*args, **kwargs)
                return_object.append(rv)
            else:
                # print(mp.current_process().pid, ' exiting')
                break
    return wrapper