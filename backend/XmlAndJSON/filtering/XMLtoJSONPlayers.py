import xml.etree.ElementTree as ET
import json

#Loading and parsing the XML file
tree = ET.parse('players.xml')
root = tree.getroot()

#List to store filtered players
filtered_players = []

#Iteration
for player in root.findall('player'):
    position = player.find('position').text
    if position and 'C' in position:
        player_data = {
            'id': int(player.find('id').text),
            'first_name': player.find('first_name').text,
            'height_feet': player.find('height_feet').text,
            'height_inches': player.find('height_inches').text,
            'last_name': player.find('last_name').text,
            'position': position,
            'weight_pounds': player.find('weight_pounds').text,
            'teamID': int(player.find('teamID').text)
        }
        filtered_players.append(player_data)

        print(player_data)


#Saving players to JSON file
with open('filtered_players.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_players, f, ensure_ascii=False, indent=4)