import json
import jsonschema
from jsonschema import validate


def get_json_file(file_name):
    """This function loads the given json available"""
    with open(file_name, 'r') as file:
        schema = json.load(file)
    return schema

json_schema = get_json_file('teams.schema.json')
json_data = get_json_file('teams.json')

validate(instance=json_data, schema=json_schema)