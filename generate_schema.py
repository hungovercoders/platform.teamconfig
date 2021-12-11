from genson import SchemaBuilder
import json


def get_schema(file_name):
    """This function loads the given schema available"""
    with open(file_name, 'r') as file:
        schema = json.load(file)
    return schema

json_schema = get_schema('teams.json')
builder = SchemaBuilder()
builder.add_schema(json_schema)

print(builder.to_schema())

