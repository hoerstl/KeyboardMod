from typing import Any
import os
import dotenv
import PIL.Image as Image
from PIL import ImageGrab
import time

from google import genai

# Define globals
gemini_model = None


def requiresDefinedModel(func):
    def wrapper(*args, **kwargs):
        if not os.environ.get('GEMINI_API_KEY'):
            print("It looks like we were unable to load the `GEMINI_API_KEY` environment variable.")
            return "GEMINI_API_KEY environment variable not found."
        return func(*args, **kwargs)
    return wrapper



def getScreenshot(coords=[None, None]) -> Image:
    p1, p2 = coords
    if not p1 or not p2:
        return ImageGrab.grab()
    
    # Unpack coordinates
    x1, y1 = p1
    x2, y2 = p2
    
    # proper ordering (top-left to bottom-right)
    left = min(x1, x2)
    top = min(y1, y2)
    right = max(x1, x2)
    bottom = max(y1, y2)
    
    bbox = (left, top, right, bottom)
    
    return ImageGrab.grab(bbox=bbox)


@requiresDefinedModel
def askGemeni(prompt: str, image: Image = None):
    global gemini_model
    response = None

    if image:
        response = gemini_model.models.generate_content(
            model="gemini-3-flash-preview", contents=[prompt, image]
        )
    else:
        response = gemini_model.models.generate_content(
            model="gemini-3-flash-preview", contents=prompt
        )

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
def answerVisableExtendedResponseQuestion(coords=[None, None]) -> str:
    try:
        prompt = "This is a screenshot of an extended response question. Write a decently lengthy response to the question (about a paragraph or so)."
        answer = askGemeni(prompt,
                           getScreenshot(coords))
    except:
        answer = "Something went wrong when we tried to ask Gemini this question"

    return answer


@requiresDefinedModel
def answerVisableCodingQuestion(coords=[None, None], chatHistory=[]) -> str:
    history = "\n\nPrevious message: ".join(chatHistory)
    try:
        prompt = "This is a programming question. Given the code you see available to you and the context provided here, return just the code to answer the question, do not use any backticks or frame the code in any way. Please return just the plaintext. Do not write any comments in the code. Chat history: \n\n" + history
        answer = askGemeni(prompt,
                           getScreenshot(coords))
    except:
        answer = "Something went wrong when we tried to ask Gemini this question"

    return answer


def init(api_key=None):
    global gemini_model
    if api_key: 
        os.environ["GEMINI_API_KEY"] = api_key
    gemini_model = genai.Client()


def main():
    init()
    time.sleep(5)
    getScreenshot()
    print(answerVisableQuizQuestion())
    print(answerVisableExtendedResponseQuestion())

if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
