from DQ.surveyMaster import getFreeIceCreamCode
from popup import displayToUser
import threading


def showTaskScheduler():
    def target():
        import ADHDassist.main
    thread = threading.Thread(target=target)
    thread.start()


def showIcecreamCode():
    def target():
        freeIceCreamCode = getFreeIceCreamCode()
        displayToUser('DQ', f"Your icecream my leige: {freeIceCreamCode}", 800)

    thread = threading.Thread(target=target)
    thread.start()




