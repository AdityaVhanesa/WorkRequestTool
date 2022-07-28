import threading
import time

from flask import redirect

isTimeout = False
timeOutPeriod = 10


def redirectHome():
    return redirect("/fail")


def task_countPeriod():
    global isTimeout
    time.sleep(5)
    isTimeout = True
    print("Times_up")
    redirectHome()


def startWatchDog():
    loginWatchDog = threading.Thread(target=task_countPeriod)
    loginWatchDog.start()
