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

def get_nodes():
  data_file = 'teams/schema/team.schema.json'
  f = open(data_file)
  data = json.load(f)

  teams = data['$defs']['teamname_list']['enum']
  team_members = data['$defs']['teammember_list']['enum']
  products = data['$defs']['product']['properties']['name']['enum']
  events = data['$defs']['event_list']['enum']

  return teams, team_members, products, events

def create_map():

  G_people = nx.Graph()
  G_events = nx.Graph()

  teams, team_members, products, events = get_nodes()

  for i in teams:
    G_people.add_node(i,type="team")
    G_events.add_node(i,type="team")
  for i in team_members:
    G_people.add_node(i,type="team_member")
  for i in products:
    G_events.add_node(i,type="product")
  for i in events:
    G_events.add_node(i,type="event")

  team_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
  for file in team_files:
    data_file = f'{mypath}/{file}'
    f = open(data_file)
    data = json.load(f)
    name = data["overview"]["name"]
    teams.append(name)
    teams_working_with = data["overview"]["teams_working_with"]
    team_members = data["members"]
    team_products = data["products"]

    for team_work_with in teams_working_with:
      G_people.add_edge(name, team_work_with)
    for team_member in team_members:
      G_people.add_edge(name, team_member['name'])
    for team_product in team_products:
      product_name = team_product['name']
      G_events.add_edge(name, product_name)
      product_events = team_product['events']
      for product_event in product_events:
        G_events.add_edge(product_name, product_event)

  # ##https://towardsdatascience.com/customizing-networkx-graphs-f80b4e69bedf
  color_map_people = ['green' if node in teams else 'blue' for node in G_people]
  color_map_events = ['orange' if node in events else 'purple' if node in products else 'green' for node in G_events]
  nx.draw_networkx(G_people,pos=nx.kamada_kawai_layout(G_people),node_color = color_map_people, with_labels=True, node_size=1000)
  plt.savefig("docs/teamgraph.png") 
  plt.show() 
  nx.draw_networkx(G_events,pos=nx.kamada_kawai_layout(G_events),node_color = color_map_events, with_labels=True, node_size=1000) 
  plt.savefig("docs/eventgraph.png") 
  plt.show() 
create_map()

