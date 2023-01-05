import json

def dictionary_to_json(json_file, data_dictionary):
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    
    json_data.update(data_dictionary)

    with open(json_file, 'w') as f:
        json.dump(json_data, f)