to_do_list = [
    {"id": 1, "activity": "dra over gulvene"},
    {"id": 2, "activity": "klippe plenen"},
    {"id": 3, "activity": "kjøpe lyspære"},
    {"id": 4, "activity": "spør om presanger til i morgen"},
    {"id": 5, "activity": "gjennomgå masse breakpoints!"}
]

def item_in_to_do_list(id):
    for item in to_do_list: # Implementasjonen min ender opp på O(n) her
        if item["id"] == id:
            return True, item
    return False, None

print(item_in_to_do_list(2))
print(item_in_to_do_list(2)[0])
print(item_in_to_do_list(2)[1])
print(item_in_to_do_list(10))
# myDict = {1: "noe", 2: "var", 3: "her"}

# try:
#   print(myDict[4])
# except Exception as e:
#   print("Noe gikk galt")
#   print(f"e: {e}")


# # myDict[4] = "i går"
# # myDict.update({5: "med meg"})
# # print(myDict)

# # for key,value in myDict.items():
# #     print(key, value)

# to_do_list = [
#     {"id": 1, "activity": "dra over gulvene"},
#     {"id": 2, "activity": "klippe plenen"},
#     {"id": 3, "activity": "kjøpe bobler"},
#     {"id": 4, "activity": "spør om presanger til i morgen"},
# ]

# print(len(to_do_list))

# for element in range(len(to_do_list):
#   activities = []
#   activities.append()

# myDict = {"activity"}

# for key, value in myDict.items():
#   print(key)
#   print(value)

# tall = 2
# for x in range(tall, 10):
#   print(x)
#   print(tall)
#   print("-------")
