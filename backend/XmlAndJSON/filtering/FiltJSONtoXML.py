import json
import xml.etree.ElementTree as ET


def readable(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            readable(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
with open('filtered_players.json', 'r') as f:
    filtered_players = json.load(f)

#Creating the root of the XML file
root = ET.Element('players')

#Iteration
for player in filtered_players:
    player_el = ET.SubElement(root, 'player')

    for key, value in player.items():
        ET.SubElement(player_el, key).text = str(value)

readable(root)

#Savint to XML file
tree = ET.ElementTree(root)
tree.write('filtered_players.xml')