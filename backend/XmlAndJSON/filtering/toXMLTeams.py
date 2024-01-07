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
# Load Teams Data
with open("../fetching/teams.json", "r") as file:
    teams = json.load(file)

# Root Element
root = ET.Element("teams")

# Loop through each team
for team in teams:
    team_element = ET.SubElement(root, "team")

    # Add team attributes
    for key, value in team.items():
        attribute = ET.SubElement(team_element, key)
        attribute.text = str(value)

readable(root)

# Create the XML tree and write to file
tree = ET.ElementTree(root)
tree.write("teams.xml", encoding="utf-8", xml_declaration=True)
