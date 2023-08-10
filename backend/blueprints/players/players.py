from flask import Blueprint, jsonify, make_response, request
from services import PlayerService
from models import PositionType

players_bp = Blueprint("players", __name__)


@players_bp.route("/players/", methods=["GET", "POST"])
def players():

    if request.method == "GET":
        # if terms are provided in query string, filter results
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        position = request.args.get('position')
        team = request.args.get('team')

        # If an incorrect position is provided it will throw an error since position type is an enum, try/except block will catch this error
        try:
            filtered_players = PlayerService.filter_players(
                first_name=first_name,
                last_name=last_name,
                position=position,
                team=team
            )
        except Exception as e:
            return make_response({"message": "No results, please check your search query and try again"}, 400)

        result = []
        for p in filtered_players:
            result.append(PlayerService.jsonify_player(p))
        # This if else block is to provide a clearer response if a search doesn't produce any results (for example, searching for a name that does not exist in the database)
        if len(result):
            return make_response(jsonify(result), 200)
        else:
            return make_response({"message": "No results, please check your search query and try again"}, 400)

    elif request.method == 'POST':
        player_data = request.get_json()
        player = PlayerService.create_player_from_json(player_data)
        json_player = PlayerService.jsonify_player(player)
        return make_response(jsonify(json_player), 201)


@players_bp.route("/players/<int:id>/", methods=["GET"])
def get_player(id):

    player = PlayerService.get_player_by_id(id)
    if not player:
        return jsonify({"message": "Player not found"}), 404

    return make_response(jsonify(PlayerService.json_player(player)), 200)


@players_bp.route("/players/<int:id>/", methods=["PUT", "DELETE"])
def update_or_delete_player(id):

    player = PlayerService.get_player_by_id(id)
    if not player:
        return jsonify({"message": "Player not found"}), 404

    if request.method == "PUT":

        data = request.get_json()

        if not data:
            return jsonify({"message": "Invalid data provided"}), 400

        success, response = PlayerService.update_player(player, data)

        if success:
            return jsonify(response), 200
        else:
            return jsonify(response), 500

    elif request.method == "DELETE":

        success, response = PlayerService.delete_player(player)

        if success:
            return jsonify(response), 200
        else:
            return jsonify(response), 500


@players_bp.route("/players/mostgoals/", methods=["GET"])
def get_top_goalscorer():
    top_scorers = PlayerService.get_player_with_most_goals()
    json_players = []
    # if multiple players with same amount of goals, return them all
    if type(top_scorers) is list:
        for scorer in top_scorers:
            json_players.append(PlayerService.jsonify_player(scorer))

        return make_response(jsonify(json_players), 200)

    return make_response(jsonify(PlayerService.jsonify_player(top_scorers)), 200)


@players_bp.route("/players/mostassists/", methods=["GET"])
def get_most_assists():
    most_assists = PlayerService.get_player_with_most_assists()
    json_players = []
    # if multiple players with same amount of assists, return them all
    if type(most_assists) is list:
        for player in most_assists:
            json_players.append(PlayerService.jsonify_player(player))

        return make_response(jsonify(json_players), 200)

    return make_response(jsonify(PlayerService.jsonify_player(most_assists)), 200)


@players_bp.route("/players/mostapps/", methods=["GET"])
def get_most_apps():

    most_apps = PlayerService.get_player_with_most_appearances()
    json_players = []
    # if multiple players with same amount of appearances, return them all
    if type(most_apps) is list:
        for player in most_apps:
            json_players.append(PlayerService.jsonify_player(player))

        return make_response(jsonify(json_players), 200)

    return make_response(jsonify(PlayerService.jsonify_player(most_apps)), 200)
