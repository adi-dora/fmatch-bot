import json

with open("verification.json", "r") as f:
    verification_json = json.load(f)

def dump_verification_json(verification_json):
    # your code here
    with open('verification.json', 'w') as f:
        json.dump(verification_json, f, indent=1)