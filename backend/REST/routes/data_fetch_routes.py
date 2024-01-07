import os
import json
from flask import jsonify, abort
from flask import send_from_directory

from Parser.parser import scrape_nba_stats
from XmlAndJSON.fetching.fetchPlayers import fetch_all_players_data
from XmlAndJSON.fetching.fetchTeams import fetch_all_teams_data
from XmlAndJSON.filtering.ConvertToXML import convert_teams_to_xml, convert_players_to_xml


def setup_data_fetch_routes(app):
    @app.route('/api/fetch_players', methods=['GET'])
    def api_fetch_players():
        try:
            players_data = fetch_all_players_data("https://balldontlie.io/api/v1/players")

            # Construct the path to the players_data.json file relative to this script
            current_dir = os.path.dirname(__file__)  # Gets the directory where this script resides
            file_path = os.path.join(current_dir, '..', '..', 'XmlAndJSON', 'data', 'players_data.json')

            # Create directories if they don't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save to a file
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(players_data, file, ensure_ascii=False, indent=4)

            return jsonify(players_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/fetch_teams', methods=['GET'])
    def api_fetch_teams():
        try:
            teams_data = fetch_all_teams_data("https://balldontlie.io/api/v1/teams")

            # Construct the path to the teams.json file relative to this script
            current_dir = os.path.dirname(__file__)  # Gets the directory where this script resides
            file_path = os.path.join(current_dir, '..', '..', 'XmlAndJSON', 'data', 'teams.json')

            # Create directories if they don't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save to a file
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(teams_data, file, ensure_ascii=False, indent=4)

            return jsonify(teams_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/to_xml/players', methods=['GET'])
    def api_to_xml_players():
        try:
            # Construct the path to the JSON and XML files relative to this script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            json_file_path = os.path.join(current_dir, '..', '..', 'XmlAndJSON', 'data', 'players_data.json')
            xml_file_path = os.path.join(current_dir, '..', '..', 'XmlAndJSON', 'data', 'players.xml')

            # Convert JSON to XML
            convert_players_to_xml(json_file_path, xml_file_path)

            # Read the XML file and return its content
            with open(xml_file_path, 'r', encoding='utf-8') as file:
                xml_content = file.read()
            return jsonify({"xml_content": xml_content})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/to_xml/teams', methods=['GET'])
    def api_to_xml_teams():
        try:
            # Adjust the path to go up two levels before accessing XmlAndJSON
            current_dir = os.path.dirname(os.path.abspath(__file__))
            json_file_path = os.path.join(current_dir, '..', '..', 'XmlAndJSON', 'data', 'teams.json')
            xml_file_path = os.path.join(current_dir, '..', '..', 'XmlAndJSON', 'data', 'teams.xml')

            # Ensure the directory for the XML file exists
            os.makedirs(os.path.dirname(xml_file_path), exist_ok=True)

            # Convert JSON to XML using the provided function
            convert_teams_to_xml(json_file_path, xml_file_path)

            # Return the XML file content
            with open(xml_file_path, 'r', encoding='utf-8') as file:
                xml_content = file.read()
            return jsonify({"xml_content": xml_content})
        except Exception as e:
            return jsonify({"error": str(e)}), 500



    @app.route('/api/download/<filename>', methods=['GET'])
    def download_file(filename):
        directory = 'C:/Users/Vanja/Desktop/KisFrontend/backend/XmlAndJSON/data'
        try:
            return send_from_directory(directory, filename, as_attachment=True)
        except FileNotFoundError:
            abort(404)

    #Route for filtering players
    @app.route('/api/players_by_team/<int:team_id>', methods=['GET'])
    def get_players_by_team(team_id):
        try:
            # Define the path to the players_data.json file
            players_file_path = 'C:/Users/Vanja/Desktop/KisFrontend/backend/XmlAndJSON/data/players_data.json'

            # Check if the file exists
            if not os.path.exists(players_file_path):
                return jsonify({"error": "Players data file not found"}), 404

            # Read the file
            with open(players_file_path, 'r', encoding='utf-8') as file:
                players_data = json.load(file)

            # Filter players by teamID
            filtered_players = [player for player in players_data if player.get('teamID') == team_id]
            return jsonify(filtered_players)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/top50', methods=['GET'])
    def get_nba_stats():
        json_file_path = r'C:\Users\Vanja\Desktop\KisFrontend\backend\XmlAndJSON\data\top50players.json'
        data = scrape_nba_stats()
        if data:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

            # Save to JSON file, will overwrite if it exists
            with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False, indent=4)

            return jsonify(data)
        else:
            return jsonify({'error': 'Stats could not be retrieved'}), 500

