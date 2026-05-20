from flask import render_template
from flask import Flask
from flask import request
from flask import url_for
from flask import render_template
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


@app.route("/test")
@app.route("/test/<name>")
def test(name=None):
    return render_template("test.html", person=name)

# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html', person=name)


# url_for returnerer selve strengen til url´en som genereres
# men da den relative etter root (og kun i terminalen, det er ikke noe bruker ser)
# syntaks er url_for(metodenavn, ...argumenter)
with app.test_request_context():
    print(url_for("show_user_profile", username="Karl"))
    print(url_for("show_user_profile", username="Johan"))
