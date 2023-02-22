import functools
from clear_terminal import clear_terminal

import timer, tree
from timer import t
from tree import tree


def analyze(funct):
    """master wrapper
    all logging, timing, debugging, should go here"""
    
    @t
    @functools.wraps(funct)
    def out_funct(*args, **kwargs):

        out = funct(*args, **kwargs)

        return out

    return out_funct

def dump():
    clear_terminal()
    print('function timing:')
    timer.dump()
    print('\n'*3)
    print('tree struct:')
    tree.dump()
