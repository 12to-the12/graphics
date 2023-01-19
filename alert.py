

alert_flag = False


def alert(message,*args):
    if alert_flag:
        print(message)
        for x in args: print(x)