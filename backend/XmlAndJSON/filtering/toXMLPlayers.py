# Load Players Data
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

with open("../fetching/players_data.json", "r") as file:
    players = json.load(file)

# Root Element
root = ET.Element("players")

# Loop through each player
for player in players:
    player_element = ET.SubElement(root, "player")

    # Add player attributes
    for key, value in player.items():
        attribute = ET.SubElement(player_element, key)
        attribute.text = str(value)

readable(root)

# Create the XML tree and write to file
tree = ET.ElementTree(root)
tree.write("players.xml", encoding="utf-8", xml_declaration=True)
