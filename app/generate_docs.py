import json2table
import os
from os import listdir
from os.path import isfile, join
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from lib.teamconfig import *

build_direction = "LEFT_TO_RIGHT"
table_attributes = None ## {"style" : "width:100%"}
mypath = 'teams'
teams = []

team_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for file in team_files:
  data_file = f'{mypath}/{file}'

  input = get_json_file(data_file)
  html_team = json2table.convert(input, 
                         build_direction=build_direction, 
                         table_attributes=table_attributes)

  html_team = """<!DOCTYPE html>
  <html>
  <head>
    <link rel="stylesheet" href="styles/style.css">
  </head>
  <body>""" + html_team + "</body>"

  team_name = (".".join(file.split(".")[:-1]))
  teams.append(team_name)
  with open(f'docs/{team_name}.html', 'w') as f:
      f.truncate()
      f.write(html_team)

  print(f'Docs created in docs/{team_name}.html')
  
html_main = ''
for t in teams:
  html_main += f"""<a href='{t}.html'>{t}</a>\n"""

html_main = """<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="styles/style.css">
</head>
<body>
<h1>Teams</h1>
""" + html_main + "</body>"

with open(f'docs/index.html', 'w') as f:
    f.truncate()
    f.write(html_main)

print(f'Docs created in docs/index.html')