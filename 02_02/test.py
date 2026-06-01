myDict = {1: "noe", 2: "var", 3: "her"}

# popped = myDict.popitem()
try:
    popped = myDict.pop(0)

    print(myDict)
    print(popped)

    verdier = myDict.values()

    myDict = {i + 1: v for i, v in enumerate(verdier)}
except:
    print("Du kan kun slette et element som faktisk finnes i listen din")

print(myDict)
