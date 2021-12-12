import json2table
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from lib.teamconfig import *

data_file = 'teams.json'
input = get_json_file(data_file)

build_direction = "LEFT_TO_RIGHT"
table_attributes = None ## {"style" : "width:100%"}
html = json2table.convert(input, 
                         build_direction=build_direction, 
                         table_attributes=table_attributes)

html = """<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="docs.css">
</head>
<body>""" + html + "</body>"

with open('docs/docs.html', 'w') as f:
    f.truncate()
    f.write(html)

print('Docs created in docs/docs.html')