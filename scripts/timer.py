from scripts.clear_terminal import clear_terminal
from time import time, perf_counter, sleep
from scripts.tree import tree
from scripts.config import config
import numpy as np
import functools
# from rich.console import Console

running = time()
buffer = '' 

def set_buffer(value):
    global buffer
    buffer = value

def clear_buffer():
    global buffer
    buffer = ''

class FPS:
    def __init__(self,fps):
        self.fps = fps
x = FPS(60)

def fps(funct):
    """(wrapper)
    adds the frames per second of the function to the buffer"""
    @functools.wraps(funct)
    def out(*args):
        start = time()
        out = funct(*args)
        end = time()

        # global fps
        x.fps = 1/(end-start)
        
        pprint(f"<> fps of {funct.__name__}",x.fps, suffix='')
        #pprint(f"avg fps with {funct.__name__}",1/(end-start),suffix='')
        return out

    return out


indent = -1
timings = {} # [name] = (count, value)
timings['update'] = np.array([0,1])
running_avg_size = config['timing']['running_avg_size']

def t(funct):
    """wrapper
    adds the function's time taken  to the buffer"""
    global indent
    @functools.wraps(funct)
    def out_funct(*args, **kwargs):
        global indent
        indent += 1


        start = perf_counter()
        out   = funct(*args, **kwargs)
        end   = perf_counter()


        name  = funct.__name__ # the name of the target function
        if name in timings.keys():
            count, avg = timings[name]
            if count<running_avg_size: count += 1
            # count += 1
            new_avg = (avg*(count-1) + (end-start)*1000)  / count

            timings[name] = (count, new_avg )
        else:
            timings[name] = np.array([1,(end-start)*1000])
        prefix = '|  ' * indent
        
        pprint(prefix+name, timings[name][1], end='')
        
        percent = (timings[name][1]/timings['update'][1])*100
        # percent = round(percent,-1)
        push(f"{percent :>4.0f} %")
        if indent <= 1: push('')
        indent -= 1
        return out

    return out_funct




def push(message, end='\n'):
    """pushes message to the message heap"""
    global buffer
    buffer +=  message + end

def pprint(message, value, suffix='ms', end='\n'): 
    """pushes message+value to the message heap"""
    assert type(value)   == np.float64 or float, f"{type(value)}"
    assert type(message) == str,   f"{message}"
    value = round(value, 2)
    push ( f"{message :<36s}:{value :>4.0f} {suffix}" ,end=end )


def timer(message):
    """ppprints the time since last call"""
    global running
    global buffer
    time_taken = (time()-running) * 1000 # in milliseconds

    padding = ( 20 - len(message) ) * ' '
    pprint(message, time_taken)
    running = time()
    #return time_taken

@t
def dump():
    global buffer
    clear_terminal()
    print(buffer)
    buffer = ''
