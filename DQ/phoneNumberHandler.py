import subprocess
from dateutil.relativedelta import relativedelta
from datetime import date
import pickle
import os


def getUsablePhoneNumber():

    if not os.path.exists("kyPhoneNumbers.pickle"):
        subprocess.run(['python', 'phoneNumbers.py'])

    with open('kyPhoneNumbers.pickle', 'rb') as file:
        kyPhoneNumbers = pickle.load(file)

    tooRecent = date.today() - relativedelta(months=1)
    for number, lastUsed in kyPhoneNumbers:
        if lastUsed < tooRecent:
            return number
    raise RuntimeError("There are no usable phone numbers at this moment.")


def markNumberUsed(phoneNumber):
    with open('kyPhoneNumbers.pickle', 'rb') as file:
        kyPhoneNumbers = pickle.load(file)

    for i in range(len(kyPhoneNumbers)):
        if kyPhoneNumbers[i][0] == phoneNumber:
            kyPhoneNumbers[i][1] = date.today()
            return

    raise ValueError(f"Phone number '{phoneNumber}' was not found in the list of phone numbers and couldn't be updated.")


