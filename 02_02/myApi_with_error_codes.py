#######################################################################
# Claudes dom over forrige versjon, myApi.py, som rettes opp i denne versjonen
#######################################################################
# These are the problems:
#
# 1. Errors are returned with status 200. Every error message is sent as a
#    success, so client code can't tell success from failure without reading
#    the text. Use e.g. return jsonify({"error": "..."}), 400 (or 404).
# 2. Plain text responses. Only GET-all returns JSON. GET single returns just
#    the activity string, not the whole object.
# 3. PUT can crash with a 500 error. json.loads, int(item_id) and
#    to_do_item["activity"] run BEFORE the try block, so /tre, a missing
#    "activity" key or bad JSON gives an Internal Server Error. The
#    "except: raise Exception(...)" also turns caught errors into a 500.
# 4. An invalid PUT falls through to the long generic message instead of
#    returning the specific validity_check reason.
# 5. to_do_item_is_valid() can return None. With {} or {"id": 5} the loop
#    never reaches a return, so POST replies "API-request error: None".
# 6. IDs are renumbered on delete. In REST an ID should be stable, so
#    "item 3" must always mean the same item. Tying ID to list position
#    causes this. Better: find items by id (like find_todo) and make new
#    IDs with max(id) + 1.
# 7. Use request.get_json() / request.json instead of json.loads(request.data).
#    Use <int:item_id> in the route so Flask rejects non-numeric IDs for you.
# 8. Unused imports: url_for, escape.
# 9. Small issue: a PUT with the item's current activity is rejected as a
#    duplicate.
#
# What my code does better: it checks the key name, string type, empty
# value, duplicates and single field (the teacher only checks that "task"
# exists), and it has great curl/Postman notes.
# Teacher's code weaknesses: DELETE returns 200 even if the ID doesn't
# exist, no type or empty-value checks, and PUT crashes on a non-object body.

from flask import Flask, request, url_for, jsonify
from markupsafe import escape
import json

app = Flask(__name__)


to_do_list = [
    {"id": 1, "activity": "dra over gulvene"},
    {"id": 2, "activity": "klippe plenen"},
    {"id": 3, "activity": "kjøpe lyspære"},
    {"id": 4, "activity": "spør om presanger til i morgen"},
    {"id": 5, "activity": "gjennomgå masse breakpoints!"},
]

# Hva Copilot og Claude sier om navngivning av routes i Flask:
# In REST, a URL identifies a resource (a thing), not an action. 
# The action is expressed by the HTTP method (GET/POST/PUT/DELETE), 
# not by the URL. 

# Action	        Method	        URL
# Get all items	    GET	            /my-to-do-list
# Create an item	POST	        /my-to-do-list
# Get one item	    GET	            /my-to-do-list/3
# Update one item   PUT (or PATCH)	/my-to-do-list/3
# Delete one item	DELETE	        /my-to-do-list/3

# Så med andre ord, hver gang jeg skal gjøre noe med ett element, bruk /<nummer> i URLen


#######################
# Create an item
#######################

# Slik gjør man POST requesten, denne gang fra en terminal
# Legg merke til at måten jeg skriver funksjonen på under,
# avgjør hvordan objektet jeg skriver inn, altså {"activity": "teste APIet mitt"},
# skal se ut. Det er derfor APIer har dokumentasjon! En bruker har jo ikke tilgang
# til å se disse funksjonene. Brukeren, altså koden, kan bare gjøre kallene.

# Tester
# curl -X POST http://127.0.0.1:5000/my-to-do-list -H "Content-Type: application/json" -d '{"activity": "teste APIet mitt"}' OK
# curl -X POST http://127.0.0.1:5000/my-to-do-list -H "Content-Type: application/json" -d '{"activity": ""}' OK (tom string gjenkjennes)
# curl -X POST http://127.0.0.1:5000/my-to-do-list -H "Content-Type: application/json" -d '{"activity": 1}' > OK (at int ikke er det samme som string gjenkjennes)
# curl -X POST http://127.0.0.1:5000/my-to-do-list -H "Content-Type: application/json" -d '{"activity": True}' > Blir håndtert av exceptions

# curl -X POST http://127.0.0.1:5000/my-to-do-list -H "Content-Type: application/json" -d '{"activity": "kjøpe bobler"}' æøå så ut til å krasje hele apiet på windows maskin. Fikk følgende feilmelding:
#'utf-8' codec can't decode byte 0xf8 in position 16: invalid start byte. Skjer bare fra git bash pga min datamaskins encoding. Skjer ikke i Powershell.
# charset=utf-8


# En viktig ting å huske på er at det er kode som gjør requests.
# Dette kan være terminalkall, fra Notebooks i Fabric, fra Postman
# eller fra Postman lignende extensions i VS Code.
# Men koden kan også gjøre disse requestene via et user interface. En
# bruker kan trykke på en knapp i user interfacet, som trigger
# en funksjon, og inni den funksjonen ligger et curl kall som over.


@app.route("/my-to-do-list", methods=["POST"])
def create_an_item():
    index = len(to_do_list) + 1
    print(f"request.data er: {request.data}")
    try:
        to_do_item = json.loads(request.data)
        print(to_do_item)
        validity_check = to_do_item_is_valid(to_do_item)

        if validity_check == "Valid":
            to_do_item["id"] = index
            to_do_list.append(to_do_item)
            print("You, or your code, just made a POST request!")
            print(f"To-do-listen etter POST request: {to_do_list}")
            # return "You rock, to-do-list has been updated!" # Gammel return ved suksess
            return jsonify(to_do_item), 200
        
        print(f"To-do-listen etter POST request: {to_do_list}")
        return f"API-request error: {validity_check}"
    
    except Exception as e:
        print(f"Something is incorrect with the API-request. Please check the syntax, and verify that all parameters have the correct data type. Details: {e}")
        return "Something went wrong, to-do-list has not been updated"


#######################
# Retrieve all items
#######################


# Denne kan også gjøres i nettleseren, siden man kan gjøre GET kall i url-feltet. Gå da til denne urlen:
# http://127.0.0.1:5000/my-to-do-list
# For å sjekke med GET kall fra terminal, bruk:
# curl -X GET http://127.0.0.1:5000/my-to-do-list -H "Content-Type: application/json"
@app.route("/my-to-do-list", methods=["GET"])
def retrieve_all_items():
    return jsonify(to_do_list), 200


##########################
# Retrieve a single item (by item number)
##########################

# curl -X GET http://127.0.0.1:5000/my-to-do-list/3 -H "Content-Type: application/json" > bør returnere 'kjøpe lyspære'
# curl -X GET http://127.0.0.1:5000/my-to-do-list/tre -H "Content-Type: application/json" > bør returnere "Please enter an argument that can be converted into a number format ('1' is OK, 'One' is not)"
# curl -X GET http://127.0.0.1:5000/my-to-do-list/-1 -H "Content-Type: application/json" > bør returnere "Please enter a number between 1 and {len(to_do_list)}"
# curl -X GET http://127.0.0.1:5000/my-to-do-list/10 -H "Content-Type: application/json" > bør returnere "Please enter a number between 1 and {len(to_do_list)}"


@app.route('/my-to-do-list/<item_id>', methods=['GET'])
def retrieve_single_item(item_id):
    try:
        index = int(item_id) - 1
        if( (index >= len(to_do_list)) or (index < 0) ):
            return f"Please enter a number between 1 and {len(to_do_list)}"
        return to_do_list[index]["activity"]
    except Exception as e:
        return "Please enter an argument that can be converted into a number format ('1' and 1 is OK, 'One' is not)"


############################
# Update an existing item
#############################

# curl -X PUT http://127.0.0.1:5000/my-to-do-list/2 -H "Content-Type: application/json" -d '{"activity": " lage daimkake"}'
# curl -X PUT http://127.0.0.1:5000/my-to-do-list/2 -H "Content-Type: application/json" -d '{"activity": "stramme fjøringene"}' 

@app.route('/my-to-do-list/<item_id>', methods=['PUT'])
def update_single_item(item_id):
    try:
        to_do_item = json.loads(request.data)
        index = int(item_id) - 1 # python lists starts with index 0

        validity_check = to_do_item_is_valid(to_do_item)
        
        if validity_check == "Valid":
            if index > -1 and index < len(to_do_list):
                activity = to_do_item["activity"]   
                # print("You, or your code, just made a PUT request!")
                to_do_list[index]["activity"] = activity
                print(f"To-do-listen etter PUT request: {to_do_list}")
                # return 
                return jsonify({"Message": "You rock, to-do-list has been updated!", "ToDoItem": to_do_list}), 200
            else:
                return f"You have to have an id value between 1 and {len(to_do_list)}"
        else:
            return jsonify({"Request denied reason": validity_check}), 400
        
    except Exception as e:
        return jsonify({"Boring error message": f"{e}"}), 400



#########################
# Delete an item
#########################

# curl -X DELETE http://127.0.0.1:5000/my-to-do-list/2 -H "Content-Type: application/json"

@app.route('/my-to-do-list/<item_number>', methods=['DELETE'])
def delete_single_item(item_number):
    try:
        item_number = int(item_number)
    except:
        return f"You have to insert a number after the last slash in the url. /1 is OK, /one is not"
    
    if item_number > 0 and item_number <= len(to_do_list):
        index = item_number - 1
        for x in range(index, len(to_do_list)):
            if x == index:
                to_do_list.pop(x)
                continue
            to_do_list[x-1]["id"] = x # x-1 since one element has been deleted
        return "Item has been deleted from to-do-list"
            
    else:
        return f"This item does not exist in the to-do-list"

# Helper functions (don´t repeat yourself - twice)
# Functions here are used twice in the main route functions

# For funksjonen under måtte jeg velge om APIet mitt skulle være en såkalt "tolerant reader"
# Mao: når klienten gjør en request mot APIet, skal jeg godta forskjellige varianter, så lenge
# de også inneholder en nøkkel kalt "activity", som for eksempel:
# {
#     "1": 1,
#     "activity": "rive papir"
# }
# Fordelen med å være tolerant er hvis man har veldig mange klienter som bruker APIet over tid
# Hvis en klient må skifte noe i systemet sitt, som gjør at de får 1eren ovenfor, godtar
# vårt API det. I tillegg kan det bli såkalt bakover-kompatibelt. 
# Ulempene er følgende:
# 1 - It can't leak junk into your data. You could handle it by allowing, but filtering out extra fields,
#     ,but you have to write extra logic for it. A simple, strict check at the beginning instead,
#      stops "1": 1 before it gets stored, so it fixes that bug by design.
# 2 - Typos go unnoticed. With {"activty": "x", "activity": "y"} the client never 
#     finds out it misspelled a field.
# 3 - Clients get misleading results. With PUT /my-to-do-list/2 and a body of 
#     {"id": 7, "activity": "x"}, you return 200 and the client thinks it 
#     changed the id. It didn't.

# Jeg endte derfor opp med å ikke la APIet mitt være en "tolerant reader"

def to_do_item_is_valid(to_do_item):
    '''
    Denne hjelpemetoden sjekker at:
    - json-elementet inneholder iallefall en nøkkel kalt activity
    - aktiviteten er en streng, og at den ikke er tom
    - aktiviteten ikke finnes fra før i listen
    '''
    
    for key,value in to_do_item.items():
        if not "activity" in to_do_item:
            return "There should be at least one key in the request called 'activity'"
        if key != "activity":
            continue
        if not isinstance(value, str):
            return "The value of the input should be a string"
        if len(value) < 1:
            return "The value of the input should not be empty"
        
        # Verify that the activity does not exist in the to-do-list already
        for element in to_do_list:
            if element["activity"] == value:
                return "Activity already exists in the to-do-list"

        return "Valid"


if __name__ == "__main__":
    app.run()

# For å teste APIet med Postman online, gjør følgende.
# Kjør applikasjon, men ikke i debug mode. 
# Gå til Ports (ved siden av Terminal), skriv 5000 i Port feltet.
# Trykk Enter, og logg inn med Github.
# Høyreklikk adressen jeg får i Forwarded Address, velg Port visibility > Public
# Når jeg er ferdig med å teste, skru denne tilbake igjen til Private
# Gå til Postman og kopier Forwarded Address. Legg til /my-to-do-list bak adressen
# Skal jeg bruke POST, klikk Body > raw i postman og legg inn {"activity": "min aktivitet"}
# Når jeg er ferdig, husk å skru Port visibility tilbake til Private
# Høyreklikk der jeg skrev 5000 i Port feltet, og skru av Port forwarding




