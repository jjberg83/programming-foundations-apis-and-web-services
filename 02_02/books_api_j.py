from flask import Flask
from flask import request
from flask import url_for
from markupsafe import escape

app = Flask(__name__)

to_do_list = {"1": "dra over gulvene", "2": "rydde boden"}


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/my-to-do-list")
def read_to_do_list():
    return "<p>Another result</p>"


@app.route("/hello")
def hello():
    name = request.args.get("name", "Flask")
    return f"Hello, {escape(name)}!"


@app.route("/user/<username>")
def show_user_profile(username):
    # show the user profile for that user
    return f"User {escape(username)}"
    # return f"User {escape(username)}, this is your to-do list: {escape(to_do_list)}"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return "Du bruker POST"
    return "Du bruker GET"


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         return do_the_login()
#     else:
#         return show_the_login_form()


# url_for returnerer selve strengen til url´en som genereres
# men da den relative etter root (og kun i terminalen, det er ikke noe bruker ser)
# syntaks er url_for(metodenavn, ...argumenter)
with app.test_request_context():
    print(url_for("show_user_profile", username="Karl"))
    print(url_for("show_user_profile", username="Johan"))
