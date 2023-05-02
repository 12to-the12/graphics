import functools
from utilities.clear_terminal import clear_terminal

import utilities.timer as timer, utilities.tree as tree
from utilities.timer import t
from utilities.tree import tree


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
