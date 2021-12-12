import json
import jsonschema
from jsonschema import validate
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from lib.teamconfig import *

# Must be schema valid

data_file = 'teams.json'
schema_file = 'teams.schema.json'
json_schema = get_json_file(schema_file)
json_data = get_json_file(data_file)
validate_schema(json_data=json_data,json_schema=json_schema)

# Must have a PO, Scrum Master and Technical Lead

# Must not have more than 8 members

# Must have at least 4 members

# Team members must only be in one team