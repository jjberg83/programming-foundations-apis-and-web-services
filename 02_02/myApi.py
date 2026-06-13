# NB: Forskjellen mellom 'request' (Flask) vs 'requests' (library):
# request (brukes her)  — reads incoming requests to YOUR server (built into Flask, server-side)
# requests (brukes i 01_04) — sends outgoing requests TO other APIs  (pip install requests, client-side)
from flask import Flask, request, url_for, jsonify
from markupsafe import escape
import json

app = Flask(__name__)


to_do_list = [
    {"id": 1, "activity": "dra over gulvene"},
    {"id": 2, "activity": "klippe plenen"},
    {"id": 3, "activity": "kjøpe bobler"},
    {"id": 4, "activity": "spør om presanger til i morgen"},
]


# Helper functions (don´t repeat yourself - twice)
# Functions here are used twice in the main route functions


def insert_to_do_item(to_do_item, index=None):
    if not index:
        index = len(to_do_list) + 1
        to_do_list[index] = to_do_item
    else:
        to_do_list[index] = to_do_item


# Main rourte functions


@app.route("/create_item", methods=["POST"])
def create_item():
    if request.method == "POST":
        itemname = request.form["itemname"]
        if itemname in to_do_list.values():
            message = f"{itemname} finnes allerede i to-do listen din !!!"
        elif len(itemname) == 0:
            message = "Du må skrive noe - blanke to-do items teller ikke."
        else:
            # Lager hjelpefunksjon - siden vi bruker funksjonaliteten igjen i update_item
            insert_to_do_item(itemname)
            message = f"{itemname} er lagt til i to-do listen din !!!"
        return render_template("login-form.html", items=to_do_list, message=message)


@app.route("/my_to_do_list", methods=["GET"])
def read_all():
    # return to_do_list
    return jsonify(to_do_list)


# Slik gjør man POST requesten, denne gang fra en terminal
# Legg merke til at måten jeg skriver funksjonen på under,
# avgjør hvordan objektet jeg skriver inn, altså {"activity": "teste APIet mitt"},
# skal se ut. Det er derfor APIer har dokumentasjon! En bruker har jo ikke tilgang
# til å se disse funksjonene. Brukeren, altså koden, kan bare gjøre kallene.

# curl -X POST http://127.0.0.1:5000/my_to_do_list \
#  -H "Content-Type: application/json" \
#  -d '{"activity": "teste APIet mitt"}'

# En viktig ting å huske på er at det er kode som gjør requests.
# Dette kan være terminalkall, fra Notebooks i Fabric, fra Postman
# eller fra Postman lignende extensions i VS Code.
# Men koden kan også gjøre disse requestene via et user interface. En
# bruker kan trykke på en knapp i user interfacet, som trigger
# en funksjon, og inni den funksjonen ligger et curl kall som over.


@app.route("/my_to_do_list", methods=["POST"])
def add_to_do_item():
    index = len(to_do_list) + 1
    print(f"request.data er: {request.data}")
    to_do_item = json.loads(request.data)
    print(f"to_do_item: {to_do_item}")
    if not to_do_item_is_valid(to_do_item):
        return jsonify({"error": "Invalid to-do-item properties."}), 400
    to_do_item["id"] = index
    to_do_list.append(to_do_item)
    print(to_do_item)
    print("You, or your code, just made a POST request!")
    return "You rock, to-do-list has been updated!"


# Denne hjelpemetoden sjekker bare at objektet vi sender inn har
# en nøkkel som kalles "activity"
def to_do_item_is_valid(to_do_item):
    print(f"to_do_item.keys(): {to_do_item.keys()}")
    for key in to_do_item.keys():
        print(f"key: {key}")
        if key != "activity":
            return False
    return True


@app.route("/read_item", methods=["GET"])
def read_item():
    if request.method == "GET":
        try:
            itemnumber = int(request.form["itemnumber"])
            if itemnumber in to_do_list:
                message = f"Element nr. {itemnumber} finnes og har verdien: {to_do_list[itemnumber]}"
            else:
                message = f"Element nr. {itemnumber} finnes ikke i gjøremålslisten din"
        except:
            message = f"Husk å skrive inn et tall - prøv igjen!"
        return render_template("login-form.html", items=to_do_list, message=message)


@app.route("/update_item", methods=["POST"])
def update_item():
    if request.method == "POST":
        try:
            itemnumber = int(request.form["itemnumber"])
            newvalue = request.form["newvalue"]
            if itemnumber in to_do_list:
                old_value = to_do_list[itemnumber]
                insert_to_do_item(newvalue, itemnumber)
                message = f"Element nr. {itemnumber} finnes, gammel verdi: {old_value}, ny verdi: {to_do_list[itemnumber]}"
            else:
                message = f"Element nr. {itemnumber} finnes ikke i gjøremålslisten din"
        except:
            message = f"Husk å skrive inn et tall - prøv igjen!"
        return render_template("login-form.html", items=to_do_list, message=message)


@app.route("/delete_item", methods=["POST"])
def delete_item():
    if request.method == "POST":
        try:
            itemnumber = int(request.form["itemnumber"])
            if itemnumber in to_do_list:
                old_value = to_do_list.pop(itemnumber)
                to_do_list_values = list(to_do_list.values())
                to_do_list.clear()
                print(to_do_list_values)
                print(to_do_list)
                to_do_list.update({i + 1: v for i, v in enumerate(to_do_list_values)})
                print(to_do_list)
                message = f"Element nr. {itemnumber}: {old_value} er slettet"
            else:
                message = f"Element nr. {itemnumber} finnes ikke i gjøremålslisten din"
        except:
            message = f"Husk å skrive inn et tall - prøv igjen!"
        return render_template("login-form.html", items=to_do_list, message=message)


@app.route("/")
def hello_world():
    return """Welcome to this amazing API! <br/>
    Start using it by entering different things into the url."""


@app.route("/my-to-do-list")
def read_to_do_list():
    return "<p>Another result</p>"


@app.route("/hello")
def hello():
    name = request.args.get("name", "Flask")
    age = request.args.get("age", "forever young")
    print(f"name {name}")
    print(f"age {age}")
    if name and age:
        # return f"Hello, {escape(name)}!"
        return f"Hello {name}, you are {age}!"
        # /hello?name=<script>alert("bad")</script>
        # argumentet over vil bli håndtert av escape
        # Håndteres automatisk av jinja, men her bruker man jo ikke jinja

        # Legger jeg inn dette som url:
        # http://127.0.0.1:5000/hello?name=victoria&&location=stavanger
        # Blir output:
        # Hello victoria, you are forever young!
        # Mao: age får default verdi, og location, som ikke er definert i funksjonen, blir ignorert


# Her er en annen måte å gjøre det samme på (med variable rules)
# Jeg kan i tillegg legge til variabler, som ovenfor
# Variabler som ikke er definert blir også her ignorert
@app.route("/user/<username>")
def show_user_profile(username):
    age = request.args.get("age", "forever young")
    # show the user profile for that user
    return f"Hello {escape(username)}, you are {age}"
    # http://127.0.0.1:5000/user/oscar?age=17&location=stavanger gir Hello oscar, you are 17
    # http://127.0.0.1:5000/user/oscar?location=stavanger gir Hello oscar, you are forever young


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
