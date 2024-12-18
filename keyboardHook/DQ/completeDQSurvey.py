import requests
import time
from datetime import date
from bs4 import BeautifulSoup


def padDate(date, desiredLength: int):
    if isinstance(date, int):
        date = str(date)
    while desiredLength - len(date) > 0:
        date = "0" + date
    return date


def completeSurvey(phoneNumber):
    waitTime = .01
    today = date.today()
    month = padDate(today.month, 2)
    day = padDate(today.day - 1, 2)
    year = str(today.year)[2:]
    with requests.Session() as session:
        http = session.get("https://dqfanfeedback.com/").text
        soup = BeautifulSoup(http, "lxml")
        c = soup.find("form", id="surveyEntryForm")["action"].split("=")[-1]
        queryData = {
            "c": c
        }
        phone1, phone2, phone3 = phoneNumber.split('-')

        # Submit the welcome page
        time.sleep(waitTime)
        payload = {  # 859-868-1034
            "JavaScriptEnabled": "1",
            "FIP": "True",
            "CN1": phone1,
            "CN2": phone2,
            "CN3": phone3,
            "InputMonth": month,
            "InputDay": day,
            "InputYear": year,
            "InputHour": "06",
            "InputMinute": "09",
            "InputMeridian": "PM",
            "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
            "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page.",
            "NextButton": "Start"
        }
        session.post("https://dqfanfeedback.com/Survey.aspx", data=payload, params=queryData)
        # Answer the first question (I went to this location)
        time.sleep(waitTime)
        payload = {
            "R000137": "1",
            "IoNF": "1",
            "PostedFNS": "R000137",
            "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
            "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page."
        }
        session.post("https://dqfanfeedback.com/Survey.aspx", data=payload, params=queryData)
        # Answer the second question (I was neither satisfied nor dissatisfied with my visit.)
        time.sleep(waitTime)
        payload = {
            "R000007": "3",
            "IoNF": "6",
            "PostedFNS": "S000002 | S000003 | R000007",
            "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
            "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page."
        }
        session.post("https://dqfanfeedback.com/Survey.aspx", data=payload, params=queryData)
        # Answer the third question (I got curbside pickup)
        time.sleep(waitTime)
        payload = {
            "R000010": "6",
            "IoNF": "9",
            "PostedFNS": "R000010",
            "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
            "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page."
        }
        session.post("https://dqfanfeedback.com/Survey.aspx", data=payload, params=queryData)
        # Answer the fourth question (I only ordered a drink)
        time.sleep(waitTime)
        payload = {
            "R000015": "1",
            "R000130Other": "",
            "IoNF": "18",
            "PostedFNS": "R000012|R000014|R000015|R000013|R000130",
            "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
            "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page."
        }
        session.post("https://dqfanfeedback.com/Survey.aspx", data=payload, params=queryData)
        # Answer the fifth question (It was okay)
        time.sleep(waitTime)
        payload = {
            "R000020": "3",
            "R000018": "3",
            "R000021": "3",
            "R000023": "3",
            "R000028": "3",
            "R000030": "3",
            "R000022": "3",
            "IoNF": "30",
            "PostedFNS": "R000020|R000018|R000021|R000023|R000028|R000030|R000022",
            "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
            "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page."
        }
        session.post("https://dqfanfeedback.com/Survey.aspx", data=payload, params=queryData)
        # Answer the sixth question (Still sitting on the fence)
        time.sleep(waitTime)
        payload = {
            "R000017": "3",
            "R000025": "3",
            "R000031": "3",
            "IoNF": "36",
            "PostedFNS": "R000017|R000025|R000031",
            "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
            "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page."
        }
        session.post("https://dqfanfeedback.com/Survey.aspx", data=payload, params=queryData)
        # Answer the seventh question (No problems with my visit)
        time.sleep(waitTime)
        payload = {
            "R000032": "2",
            "IoNF": "43",
            "PostedFNS": "R000032",
            "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
            "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page."
        }
        session.post("https://dqfanfeedback.com/Survey.aspx", data=payload, params=queryData)
        # Answer the eighth question (I might reccomend and might return)
        time.sleep(waitTime)
        payload = {
            "R000036": "3",
            "R000035": "3",
            "IoNF": "86",
            "PostedFNS": "R000036|R000035",
            "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
            "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page."
        }
        session.post("https://dqfanfeedback.com/Survey.aspx", data=payload, params=queryData)
        # Answer the ninth question (How did you like your visit in 3 or more sentences.)
        time.sleep(waitTime)
        payload = {
            "S000037": "Oh, I just really enjoy your water. In fact, your water dispenser is like the best thing in the entire universe. If I could come back, I would get the same thing. It's the coolest.",
            "IoNF": "87",
            "PostedFNS": "S000037",
            "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
            "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page."
        }
        session.post("https://dqfanfeedback.com/Survey.aspx", data=payload, params=queryData)
        # Answer the tenth question (They were very nice to me when I went there)
        time.sleep(waitTime)
        payload = {
            "R000108": "1",
            "R000105": "1",
            "R000106": "1",
            "IoNF": "99",
            "PostedFNS": "R000108|R000105|R000106",
            "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
            "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page."
        }
        session.post("https://dqfanfeedback.com/Survey.aspx", data=payload, params=queryData)
        # Answer the eleventh question (I didn't use the mobile app)
        time.sleep(waitTime)
        payload = {
            "R000225": "2",
            "IoNF": "189",
            "PostedFNS": "R000225",
            "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
            "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page."
        }
        session.post("https://dqfanfeedback.com/Survey.aspx", data=payload, params=queryData)
        # Answer the twelth question (I came alone, also first time in the last month)
        time.sleep(waitTime)
        payload = {
            "R000328": "1",
            "R000111": "1",
            "IoNF": "201",
            "PostedFNS": "R000328|R000111",
            "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
            "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page."
        }
        session.post("https://dqfanfeedback.com/Survey.aspx", data=payload, params=queryData)
        # Answer the thirteenth question (This was not my first ever visit)
        time.sleep(waitTime)
        payload = {
            "R000112": "2",
            "IoNF": "202",
            "PostedFNS": "R000112",
            "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
            "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page."
        }
        session.post("https://dqfanfeedback.com/Survey.aspx", data=payload, params=queryData)
        # Answer the fourteenth question (I haven't seen any promotions in the last month)
        time.sleep(waitTime)
        payload = {
            "R000455": "1",
            "IoNF": "210",
            "PostedFNS": "R000452 | R000451 | R000450 | R000449 | R000453 | R000454 | R000455",
            "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
            "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page."
        }
        session.post("https://dqfanfeedback.com/Survey.aspx", data=payload, params=queryData)
        # Answer the fifteenth question (I came here for a cupin or promotion)
        time.sleep(waitTime)
        payload = {
            "R000113": "1",
            "IoNF": "212",
            "PostedFNS": "R000113",
            "OneQuestionLeftUnansweredErrorMessageTemplate": "There is {0} error on the page.",
            "MoreQuestionsLeftUnansweredErrorMessageTemplate": "There are {0} errors on the page."
        }
        finalResponse = session.post("https://dqfanfeedback.com/Survey.aspx", data=payload, params=queryData)

    return finalResponse.text
