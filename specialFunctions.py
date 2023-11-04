from DQ.surveyMaster import getFreeIceCreamCode
from popup import displayToUser
import importlib
import threading
import sys
import os


def showTaskScheduler():
    def target(pathToFile):
        print("Ran the target")
        targetPath = "\\".join(pathToFile.split("\\")[:-1] + ["ADHDassist"])
        sys.path.append(targetPath)
        os.chdir(targetPath)
        module = importlib.import_module("ADHDassist.main", "ADHDassist")
        module.main()

    thread = threading.Thread(target=lambda: target(__file__))
    thread.start()


def showIcecreamCode():
    def target():
        freeIceCreamCode = getFreeIceCreamCode()
        displayToUser('DQ', f"Your icecream my leige: {freeIceCreamCode}", 800)

    thread = threading.Thread(target=target)
    thread.start()


