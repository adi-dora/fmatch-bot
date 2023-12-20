import json
with open("match.json", "r") as f:
    match_json = json.load(f)

def dump_match_json(match_json):
    # your code here
    with open('match.json', 'w') as f:
        json.dump(match_json, f, indent=1)