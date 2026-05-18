from flask import Flask

app = Flask(__name__)

to_do_list = {"1": "dra over gulvene", "2": "rydde boden"}


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/my-to-do-list")
def read_to_do_list():
    return "<p>Another result</p>"
