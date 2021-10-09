import json

gamelist = []

with open("config.json") as json_file:
    gamelist = json.load(json_file)


print(gamelist[1]["LOCATION"])
