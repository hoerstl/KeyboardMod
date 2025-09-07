from typing import Any
import os
import dotenv
import PIL.Image as Image
from PIL import ImageGrab
import time

import google.generativeai as genai

# Define globals
gemini_model = None


def requiresDefinedModel(func):
    def wrapper(*args, **kwargs):
        if not os.environ.get('GOOGLE_API_KEY'):
            print("It looks like we were unable to load the `GOOGLE_API_KEY` environment variable.")
            return "GOOGLE_API_KEY environment variable not found."
        return func(*args, **kwargs)
    return wrapper



def getScreenshot() -> Image:
    return ImageGrab.grab()


@requiresDefinedModel
def askGemeni(prompt: str, image: Image = None):
    global gemini_model
    response = None

    if image:
        response = gemini_model.generate_content([prompt, image])
    else:
        response = gemini_model.generate_content(prompt)

    return response.text


@requiresDefinedModel
def answerVisableQuizQuestion(verbose: bool = False) -> str:
    try:
        prompt = "This image is a picture of a multiple choice question on a quiz. Please transcribe the question in the following format, you may use more or fewer choices depending on the number of options given:\nQuestion here\na. Option 1\nb. Option 2\nc. Option 3\nd. Option 4"
        question = askGemeni(prompt,
                           getScreenshot())
        prompt = f"The following is a multiple choice question on a quiz. Which is/are correct answer(s)?\n{question}"
        if not verbose: prompt += " Respond only with the correct answer."
        answer = askGemeni(prompt)
    except Exception as e:
        answer = "Something went wrong when we tried to ask Gemini this question"

    return answer


@requiresDefinedModel
def answerVisableExtendedResponseQuestion() -> str:
    try:
        prompt = "This is a screenshot of an extended response question. Write a decently lengthy response to the question (about a paragraph or so)."
        answer = askGemeni(prompt,
                           getScreenshot())
    except:
        answer = "Something went wrong when we tried to ask Gemini this question"

    return answer


def init(api_key=None):
    global gemini_model
    if api_key: 
        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')


def main():
    init()
    time.sleep(5)
    print(answerVisableQuizQuestion())
    print(answerVisableExtendedResponseQuestion())

if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
