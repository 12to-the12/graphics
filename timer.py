import time
from clear_terminal import clear_terminal
running = time.time()
printout = ''


def pprint(message, value):
    global running
    global printout
    value = round(value, 2)
    padding = ( 20 - len(message) ) * ' '
    printout += f"{message+padding}:\t{value}\tms\n"

def timer(message):
    global running
    global printout
    time_taken = (time.time()-running) * 1000 # in milliseconds

    padding = ( 20 - len(message) ) * ' '
    pprint(message, time_taken)
    running = time.time()
    #return time_taken

def dump():
    global printout
    clear_terminal()
    print(printout)
    
    printout = ''
