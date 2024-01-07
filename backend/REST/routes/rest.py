import json
import os

from flask import Flask, jsonify, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teams.db'
db = SQLAlchemy(app)

def read_json(filename):
    if not os.path.exists(filename):
        return []  # Return an empty list if the file doesn't exist
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def get_next_id(players):
    if not players:
        return 1
    max_id = max(player['id'] for player in players)
    return max_id + 1

# The path to your JSON file
PLAYERS_FILE_PATH = 'C:/Users/Vanja/Desktop/KisFrontend/backend/XmlAndJSON/data/players_data.json'
TEAMS_FILE_PATH = 'C:/Users/Vanja/Desktop/KisFrontend/backend/XmlAndJSON/data/teams.json'

def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def write_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def get_next_id(players):
    if not players:
        return 1
    max_id = max(player['id'] for player in players)
    return max_id + 1

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String(3), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    conference = db.Column(db.String(50), nullable=False)
    division = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    height_feet = db.Column(db.Integer)
    height_inches = db.Column(db.Integer)
    last_name = db.Column(db.String(50))
    position = db.Column(db.String(10))
    weight_pounds = db.Column(db.Integer)
    teamID = db.Column(db.Integer, db.ForeignKey('team.id'))

    team = relationship('Team', backref='players')



with app.app_context():
    db.create_all()

@app.route('/teams', methods=['GET'])
def get_teams():
    # Read the current teams from the JSON file
    teams = read_json(TEAMS_FILE_PATH)

    # Return the list of teams
    return jsonify(teams)



@app.route('/teams', methods=['POST'])
def create_team():
    if not request.json or "full_name" not in request.json:
        abort(400)

    teams = read_json(TEAMS_FILE_PATH)
    next_id = get_next_id(teams)

    new_team_data = {
        'id': next_id,
        'abbreviation': request.json.get('abbreviation', ''),
        'city': request.json.get('city', ''),
        'conference': request.json.get('conference', ''),
        'division': request.json.get('division', ''),
        'full_name': request.json['full_name'],
        'name': request.json.get('name', '')
    }

    teams.append(new_team_data)
    write_json(TEAMS_FILE_PATH, teams)

    return jsonify(new_team_data), 201



@app.route('/teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
    teams = read_json(TEAMS_FILE_PATH)
    team = next((t for t in teams if t['id'] == team_id), None)

    if not team:
        abort(404, description="Team not found")

    return jsonify(team)



@app.route('/teams/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    if not request.json:
        abort(400)

    teams = read_json(TEAMS_FILE_PATH)
    team = next((t for t in teams if t['id'] == team_id), None)

    if not team:
        abort(404, description="Team not found")

    team.update({
        'abbreviation': request.json.get('abbreviation', team['abbreviation']),
        'city': request.json.get('city', team['city']),
        'conference': request.json.get('conference', team['conference']),
        'division': request.json.get('division', team['division']),
        'full_name': request.json.get('full_name', team['full_name']),
        'name': request.json.get('name', team['name'])
    })

    write_json(TEAMS_FILE_PATH, teams)

    return jsonify(team)



@app.route('/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    teams = read_json(TEAMS_FILE_PATH)
    teams = [t for t in teams if t['id'] != team_id]
    write_json(TEAMS_FILE_PATH, teams)

    return '', 204


# Player endpoints
@app.route('/players', methods=['GET'])
def get_players():
    # Read the current players from the JSON file
    players = read_json(PLAYERS_FILE_PATH)

    # Return the list of players
    return jsonify(players)


@app.route('/players', methods=['POST'])
def create_player():
    if not request.json:
        abort(400)

    players = read_json(PLAYERS_FILE_PATH)
    next_id = get_next_id(players)

    new_player_data = {
        'id': next_id,
        'first_name': request.json.get('first_name', ''),
        'last_name': request.json.get('last_name', ''),
        'height_feet': request.json.get('height_feet'),
        'height_inches': request.json.get('height_inches'),
        'position': request.json.get('position', ''),
        'weight_pounds': request.json.get('weight_pounds'),
        'teamID': request.json.get('teamID')
    }

    players.append(new_player_data)
    write_json(PLAYERS_FILE_PATH, players)

    return jsonify(new_player_data), 201
@app.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    # Read the current players from the JSON file
    players = read_json(PLAYERS_FILE_PATH)

    # Find the player with the matching ID
    player = next((p for p in players if p['id'] == player_id), None)

    # If the player doesn't exist, return a 404 error
    if not player:
        abort(404, description="Player not found")

    # Return the player data
    return jsonify(player)

@app.route('/players/<int:player_id>', methods=['PUT'])
def update_player(player_id):
    if not request.json:
        abort(400)

    players = read_json(PLAYERS_FILE_PATH)
    player = next((p for p in players if p['id'] == player_id), None)

    if not player:
        abort(404, description="Player not found")

    player.update({
        'first_name': request.json.get('first_name', player['first_name']),
        'last_name': request.json.get('last_name', player['last_name']),
        'height_feet': request.json.get('height_feet', player['height_feet']),
        'height_inches': request.json.get('height_inches', player['height_inches']),
        'position': request.json.get('position', player['position']),
        'weight_pounds': request.json.get('weight_pounds', player['weight_pounds']),
        'teamID': request.json.get('teamID', player['teamID'])
    })

    write_json(PLAYERS_FILE_PATH, players)

    return jsonify(player)

@app.route('/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    players = read_json(PLAYERS_FILE_PATH)
    players = [p for p in players if p['id'] != player_id]
    write_json(PLAYERS_FILE_PATH, players)

    return '', 204


@app.route('/')
def index():
    return render_template('index.html')

from data_fetch_routes import setup_data_fetch_routes
setup_data_fetch_routes(app)

if __name__ == '__main__':
    app.run(debug=True)


