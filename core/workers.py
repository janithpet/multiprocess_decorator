import multiprocessing as mp


def standard_worker_decorator(f):
    def wrapper(q, lock):
        while True:
            args, kwargs = q.get()
            if args is not None:
                f(*args, **kwargs)
            else:
                print(mp.current_process().pid, ' exiting')
                break
    return wrapper

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


def standard_worker(f, q, lock):
    while True:
        args = q.get()
        if args is not None:
            f(args)
        else:
            print(mp.current_process().pid, 'exiting')
            break


def setup_worker_decorator(o):
    def wrapper(q, lock):
        while True:
            args = q.get()
            if args is not None:
                try: func = o()
                except: func = o
                with lock:
                    func.setup(args)
                func.run(args)
            else:
                print(mp.current_process().pid, 'exiting')
                break
    return wrapper


def setup_worker(o, q, lock):
    while True:
        args = q.get()
        if args is not None:
            with lock:
                o.setup(args)
            o.f(args)
        else:
            print(mp.current_process().pid, 'exiting')
            break
