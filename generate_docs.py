import json2table
import json
from json2html import *

def get_json_file(file_name):
    """This function loads the given json available"""
    with open(file_name, 'r') as file:
        schema = json.load(file)
    return schema

data_file = 'teams.json'
input = get_json_file(data_file)
print(json2html.convert(json = input))