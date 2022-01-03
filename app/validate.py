import json
import jsonschema
from jsonschema import validate
import os
from os import listdir
from os.path import isfile, join
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from lib.teamconfig import *

# Must be schema valid
schema_file = 'teams/schema/team.schema.json'
json_schema = get_json_file(schema_file)
mypath = 'teams'
teams = []

team_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for file in team_files:
  data_file = f'{mypath}/{file}'
  json_data = get_json_file(data_file)
  print(f"Validating {file}...")
  validate_schema(json_data=json_data,json_schema=json_schema)
  print(f"Validated {file}.")

# TODO - Must have a PO, Scrum Master and Technical Lead

# TODO - Team members must only be in one team

print("Schema validation passed")