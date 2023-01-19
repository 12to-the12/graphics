import time
running = time.time()
def timer(message):
    global running
    #print(f"{message}: {round(time.time()-running, 3) * 1000} ms")
    #running = time.time()