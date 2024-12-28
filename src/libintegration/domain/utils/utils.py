import json

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def convert_to_json(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, indent=4)
