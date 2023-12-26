import json
with open("levels.json", "r") as f:
    level_json = json.load(f)

def dump_level_json(level_json):
    # your code here
    with open('levels.json', 'w') as f:
        json.dump(level_json, f, indent=1)