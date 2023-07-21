from flask import Blueprint, jsonify, make_response, request
from services import PlayerService
from models import PositionType

players_bp = Blueprint("players", __name__)




@players_bp.route("/players/", methods=["GET", "POST"])
def players():
    if request.method == "GET":
        player_list = PlayerService.get_all_players()
        result = []

        for p in player_list:
            result.append(PlayerService.jsonify_player(p))

        return make_response(jsonify(result), 200)

    elif request.method == 'POST':
        player_data = request.get_json()
        player = PlayerService.create_player_from_json(player_data)
        json_player = PlayerService.jsonify_player(player)
        return make_response(jsonify(json_player), 201)
    



@players_bp.route("/players/<int:id>/", methods=["GET", "POST", "PUT"])
def get_player(id):

    if request.method == 'GET':
        player = PlayerService.get_player_by_id(id)
        return make_response(jsonify(PlayerService.json_player(player)), 200)
    
    