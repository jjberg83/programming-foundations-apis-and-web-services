# NB: Forskjellen mellom 'request' (Flask) vs 'requests' (library):
# request (brukes her)  — reads incoming requests to YOUR server (built into Flask, server-side)
# requests (brukes i 01_04) — sends outgoing requests TO other APIs  (pip install requests, client-side)

# For å kjøre i git-bash:
# Naviger til rett undermappe (for eksempel 02_02)
# .venv/Scripts/python.exe -m flask --app myApi.py run --debug
# Husk at applikasjonen startes på ny hver gang jeg lagrer, så listen
# vil gå tilbake til utgangspunktet.

from flask import Flask, request, url_for, jsonify
from markupsafe import escape
import json

app = Flask(__name__)


to_do_list = [
    {"id": 1, "activity": "dra over gulvene"},
    {"id": 2, "activity": "klippe plenen"},
    {"id": 3, "activity": "kjøpe lyspære"},
    {"id": 4, "activity": "spør om presanger til i morgen"},
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
    # print(f"request.data er: {request.data}")
    try:
        to_do_item = json.loads(request.data)
        validity_check = to_do_item_is_valid(to_do_item)

        if validity_check == "Valid":
            to_do_item["id"] = index
            to_do_list.append(to_do_item)
            print("You, or your code, just made a POST request!")
            print(f"To-do-listen etter POST request: {to_do_list}")
            return "You rock, to-do-list has been updated!"
        
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
    return jsonify(to_do_list)


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
    to_do_item = json.loads(request.data)
    index = int(item_id) - 1 # python lists starts with index 0
    activity = to_do_item["activity"]
    validity_check = to_do_item_is_valid(to_do_item)
    
    try:
        if validity_check == "Valid":
            if index > -1 and index < len(to_do_list):
                print("You, or your code, just made a PUT request!")
                to_do_list[index]["activity"] = activity
                print(f"To-do-listen etter PUT request: {to_do_list}")
                return "You rock, to-do-list has been updated!"
            else:
                return f"You have to have an id value between 1 and {len(to_do_list)}"
        else: 
            print("##############")
            print(f"validity_check: {validity_check}")
            print("##############")
    except:
        raise Exception("Something is incorrect with the API-request.")

    return "Something is incorrect with the API-request. Please check the syntax, and verify that the json-element only have one element, the id is a number that already exists in the to-do-list, the key is called activity, the activity is a non-empty string and it does not exist in your to-do-list already."



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

def to_do_item_is_valid(to_do_item):
    '''
    Denne hjelpemetoden sjekker at:
    - json-elementet kun inneholder inn ett element
    - nøkkelen kalles "activity"
    - aktiviteten er en streng, og at den ikke er tom
    - aktiviteten ikke finnes fra før i listen
    '''
    
    for key,value in to_do_item.items():
        if key == "id":
            continue
        # Verify that input is in the right format
        if len(to_do_item.items()) != 1:
            return "You can only send in one activity at a time, not more, not less"
        if key != "activity":
            return "The key should be named activity"
        if not isinstance(value, str):
            return "The value of the input should be a string"
        if len(value) < 1:
            return "The value of the input should not be empty"
        
        # Verify that the activity does not exist in the to-do-list already
        for element in to_do_list:
            # print("----------")
            # print(f"element[activity]= {element['activity']}, value= {value}")
            if element["activity"] == value:
                return "Activity already exists in the to-do-list"

        return "Valid"


if __name__ == "__main__":
    app.run()
