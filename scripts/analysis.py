import functools
from scripts.clear_terminal import clear_terminal

import scripts.timer as timer, scripts.tree as tree
from scripts.timer import t
from scripts.tree import tree


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
