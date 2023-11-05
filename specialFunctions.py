from DQ.surveyMaster import getFreeIceCreamCode
from popup import displayToUser
import importlib
import threading
import sys
import os


def showTaskScheduler():
    def target():
        global taskSchedulerPath, taskSchedulerModule
        print("Ran the target")
        os.chdir(taskSchedulerPath)
        taskSchedulerModule.main()

    thread = threading.Thread(target=target)
    thread.start()


def showIcecreamCode():
    def target():
        freeIceCreamCode = getFreeIceCreamCode()
        displayToUser('DQ', f"Your icecream my leige: {freeIceCreamCode}", 800)

    thread = threading.Thread(target=target)
    thread.start()


def init():
    global taskSchedulerPath, taskSchedulerModule
    #  For the task scheduler
    taskSchedulerPath = "\\".join(__file__.split("\\")[:-1] + ["ADHDassist"])
    sys.path.append(taskSchedulerPath)
    taskSchedulerModule = importlib.import_module("ADHDassist.main", "ADHDassist")


taskSchedulerModule = None
taskSchedulerPath = None
init()
