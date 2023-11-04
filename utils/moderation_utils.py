import json
with open("moderation.json", "r") as f:
    moderation_json = json.load(f)

def dump_moderation_json(moderation_json):
    # your code here
    with open('moderation.json', 'w') as f:
        json.dump(moderation_json, f)