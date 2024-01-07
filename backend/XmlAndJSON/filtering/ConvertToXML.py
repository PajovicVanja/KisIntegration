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

def convert_players_to_xml(json_file_path, xml_file_path):
    with open(json_file_path, "r") as file:
        players = json.load(file)

    root = ET.Element("players")

    for player in players:
        player_element = ET.SubElement(root, "player")
        for key, value in player.items():
            attribute = ET.SubElement(player_element, key)
            attribute.text = str(value)

    readable(root)
    tree = ET.ElementTree(root)
    tree.write(xml_file_path, encoding="utf-8", xml_declaration=True)

def convert_teams_to_xml(json_file_path, xml_file_path):
    with open(json_file_path, "r") as file:
        teams = json.load(file)

    root = ET.Element("teams")

    for team in teams:
        team_element = ET.SubElement(root, "team")
        for key, value in team.items():
            attribute = ET.SubElement(team_element, key)
            attribute.text = str(value)

    readable(root)
    tree = ET.ElementTree(root)
    tree.write(xml_file_path, encoding="utf-8", xml_declaration=True)
