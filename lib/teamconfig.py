import json
import jsonschema
from jsonschema import validate

def get_json_file(file_name):
    """This function loads the given json available"""
    with open(file_name, 'r') as file:
        schema = json.load(file)
    return schema

def validate_schema(json_data, json_schema):

    try:
        validate(instance=json_data, schema=json_schema)
        print('Schema validation passed.')
    except jsonschema.exceptions.ValidationError as err:
        print(f"Unexpected {err}, {type(err)}")
        raise