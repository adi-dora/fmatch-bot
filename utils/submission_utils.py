import json

with open("submission.json", "r") as f:
    submission_json = json.load(f)

def dump_verification_json(submission_json):
    # your code here
    with open('submission.json', 'w') as f:
        json.dump(submission_json, f, indent=1)