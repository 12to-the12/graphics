import time
running = time.time()
def timer(message):
    global running
    time_taken = round(time.time()-running, 3) * 1000 # in milliseconds
    #print(f"{message}:\t{time_taken}\tms")
    running = time.time()
    return time_taken
