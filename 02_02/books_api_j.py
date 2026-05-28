# NB: Forskjellen mellom 'request' (Flask) vs 'requests' (library):
# request (brukes her)  — reads incoming requests to YOUR server (built into Flask, server-side)
# requests (brukes i 01_04) — sends outgoing requests TO other APIs  (pip install requests, client-side)
from flask import render_template, Flask, request, url_for, redirect, session
from markupsafe import escape

app = Flask(__name__)

to_do_list = {"1": "dra over gulvene", "2": "rydde boden"}


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


@app.route("/create_item", methods=["POST"])
def create_item():
    print(f"request: {request}")
    print(f"request.args: {request.args}")
    print(f"request.form: {request.form}")
    print(f"to_do_list: {to_do_list}")
    if request.method == "POST":
        itemname = request.form["itemname"]
        print(itemname)
        if itemname in to_do_list.values():
            print(f"Status dict: {to_do_list}")
            message = f"{itemname} finnes allerede i to-do listen din !!!"
        else:
            to_do_list_index = len(to_do_list) + 1
            to_do_list[f"{to_do_list_index}"] = itemname
            print(f"Status dict: {to_do_list}")
            message = f"{itemname} er lagt til i to-do listen din !!!"
        return render_template("login-form.html", items=to_do_list, message=message)


@app.route("/read_item", methods=["POST"])
def read_item():
    print(f"request: {request}")
    print(f"request.args: {request.args}")
    print(f"request.form: {request.form}")
    print(f"to_do_list: {to_do_list}")
    if request.method == "POST":
        itemname = request.form["itemname"]
        print(itemname)
        if itemname in to_do_list.values():
            print(f"Status dict: {to_do_list}")
            return f"<h1>Elementet finnes og er: {itemname}</h1>"
        else:
            to_do_list_index = len(to_do_list) + 1
            to_do_list[f"{to_do_list_index}"] = itemname
            print(f"Status dict: {to_do_list}")
            return f"<h1>{itemname} er lagt til i to-do listen din !!!</h1>"


# Set a secret key for encrypting session data
app.secret_key = "my_secret_key"

# dictionary to store user and password
users = {"kunal": "1234", "user2": "password2"}


@app.route("/")
def hello_world():
    message = ""
    return render_template("login-form.html", items=to_do_list, message=message)


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


@app.route("/login-form")
def login_form():
    return render_template("login-form.html", items=to_do_list)


# url_for returnerer selve strengen til url´en som genereres
# men da den relative etter root (og kun i terminalen, det er ikke noe bruker ser)
# syntaks er url_for(metodenavn, ...argumenter)
with app.test_request_context():
    print(url_for("show_user_profile", username="Karl"))
    print(url_for("show_user_profile", username="Johan"))


# For handling get request form we can get
# the form inputs value by using args attribute.
# this values after submitting you will see in the urls.
# e.g http://127.0.0.1:5000/handle_get?username=kunal&password=1234
# this exploits our credentials so that's
# why developers prefer POST request.
@app.route("/handle_get", methods=["GET"])
def handle_get():
    print(f"request: {request}")
    print(f"request.args: {request.args}")
    print(f"request.form: {request.form}")
    print(f"users: {users}")
    if request.method == "GET":
        username = request.args["username"]
        password = request.args["password"]
        print(username, password)
        if username in users and users[username] == password:
            return f"<h1>Welcome {username} !!!</h1>"
        else:
            return "<h1>invalid credentials!</h1>"
    else:
        return render_template("login.html")


# For handling post request form we can get the form
# inputs value by using POST attribute.
# this values after submitting you will never see in the urls.
@app.route("/handle_post", methods=["POST"])
def handle_post():
    print(f"request: {request}")
    print(f"request.args: {request.args}")
    print(f"request.form: {request.form}")
    print(f"users: {users}")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username, password)
        if username in users and users[username] == password:
            return f"<h1>Welcome {username} !!!</h1>"
        else:
            return "<h1>invalid credentials!</h1>"
    else:
        return render_template("login.html")


if __name__ == "__main__":
    app.run()
