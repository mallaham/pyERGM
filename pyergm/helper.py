from time import time
import logging 

def timer_func(func):
    """Decorator function to calcuate time it took to execute a function

    Args:
        func (python function): function passed to decorator 
    """
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        if hasattr(func,' __name__'):
            logging.info(f'Function {func.__name__!r} executed in {(t2-t1):.4f} seconds')
        else:
            logging.info(f'Function executed in {(t2-t1):.4f} seconds')
        return result
    return wrap_func

