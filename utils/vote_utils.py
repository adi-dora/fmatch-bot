import json
with open("vote.json", "r") as f:
    vote_json = json.load(f)

def dump_vote_json(vote_json):
    # your code here
    with open('vote.json', 'w') as f:
        json.dump(vote_json, f, indent=1)