import json

def get_secret(name: str):
    with open('.secrets.json', 'r') as f:
        secrets: dict = json.load(f)

    return secrets.get(name, None)

