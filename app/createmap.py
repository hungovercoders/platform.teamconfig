import networkx as nx
import matplotlib.pyplot as plt
import json
import os
from os import listdir
from os.path import isfile, join
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
mypath = 'teams'

G = nx.Graph()

team_names = []

team_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for file in team_files:
  data_file = f'{mypath}/{file}'
  f = open(data_file)
  data = json.load(f)
  name = data["overview"]["name"]
  team_names.append(name)
  teams_working_with = data["overview"]["teams_working_with"]
  team_members = data["members"]

  G.add_node(name)
  for team_work_with in teams_working_with:
    G.add_edge(name, team_work_with)
  for team_member in team_members:
    G.add_edge(name, team_member['name'])

color_map = ['green' if node in team_names else 'orange' for node in G]
subax1 = plt.subplot(121)

nx.draw_networkx(G,pos=nx.kamada_kawai_layout(G), node_color=color_map, with_labels=True)

plt.savefig("docs/teamgraph.png") 
plt.show() 

