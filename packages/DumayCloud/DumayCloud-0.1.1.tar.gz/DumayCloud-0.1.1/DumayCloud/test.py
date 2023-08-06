import json
with open("users.json") as file:
	j = json.load(file)
	print(j)