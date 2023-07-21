from DQ.phoneNumberHandler import getUsablePhoneNumber, markNumberUsed
from DQ.completeDQSurvey import completeSurvey
from DQ.parseDqCode import parseCode



def getFreeIceCreamCode(depth=0, numbersBurned=0):

    usablePhoneNumber = getUsablePhoneNumber()
    finalhtml = completeSurvey(usablePhoneNumber)
    freeIceCreamCode = parseCode(finalhtml)
    if freeIceCreamCode:
        markNumberUsed(usablePhoneNumber)
        return freeIceCreamCode

    if depth < 3:  # Max number of times to try the same number
        getFreeIceCreamCode(depth + 1, numbersBurned)
    else:
        markNumberUsed(usablePhoneNumber)
        if numbersBurned < 3:  # Max number of numbers to go through is 3
            getFreeIceCreamCode(numbersBurned=numbersBurned+1)




if __name__ == '__main__':
    print(getFreeIceCreamCode())
