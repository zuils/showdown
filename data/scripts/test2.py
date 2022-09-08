import re
import json
import requests
data = requests.get("https://raw.githubusercontent.com/zuils/pokemon-showdown/master/data/mods/gen2/moves.ts").text

# Remove comments
data = re.sub(r" +//.+", "", data)

# get rid of beginning Typescript object definitions
data = data.split("= {")
assert len(data) == 2, f"expecting data to have length=2: {[i[:50] for i in data]}"
data = "{" + data[1]

# Get rid of tabs
data = data.replace("\t", " ")

# double newlines are unnecessary
while "\n\n" in data:
    data = data.replace("\n\n", "\n")

# get rid of commas on the final attribute of objects. These aren't valid JSON
data = re.sub(r",\n( *)([\}\]])", r"\n\1\2", data)

# add double-quotes to keys that do not have them
data = re.sub(r"([\w\d]+): ", r'"\1": ', data)

# Correct double-quoted text inside double-quoted text
data = re.sub(r': ""(.*)":(.*)",', r': "\1:\2",', data)

# Replace single quotes with double quotes
data = data.replace("\'", "\"")

# remove semicolon at end of file
data = data.replace("};", "}")



with open("data/mods/gen2_move_mods.json", "w") as f:
    f.write(data)