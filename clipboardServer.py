from flask import Flask, jsonify
import pyperclip
app = Flask(__name__)

@app.route("/")
def getClipboard():
    return jsonify(pyperclip.paste())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
