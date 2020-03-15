from functools import wraps


def foo(f):
    def bar():
        f()

    return bar

def f():
    print('bar')

f = foo(f)

if __name__ == '__main__':
    print(f.__name__)
