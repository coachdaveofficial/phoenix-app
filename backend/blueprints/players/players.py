from functools import wraps
from flask import Blueprint, jsonify, make_response, request, redirect, flash, g
from services import PlayerService, TeamService, SeasonService
from models import PositionType
from blueprints.auth.auth import login_required

players_bp = Blueprint("players", __name__)


@players_bp.route("/players/", methods=["GET"])
def players():

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
    # This if else block is to provide a clearer response if a search doesn't produce any results 
    # (for example, searching for a name that does not exist in the database could result in an empty list)
    if len(result):
        return make_response(jsonify(result), 200)
    else:
        return make_response({"message": "No results, please check your search query and try again"}, 400)

    

@players_bp.route('/players/', methods=["POST"])
@login_required
def add_player():

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
@login_required
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
    team_name = request.args.get('team_name')
    recent = request.args.get('recent')
    recent_season = None

    if recent:
        recent_season = SeasonService.get_most_recent_season()
    
    if team_name:
        team = TeamService.get_teams(team_name=team_name)
        team_id = team[0]['id'] if team else None
    else:
        team_id = None

    if recent_season:
        top_scorers = PlayerService.get_top_goal_scorers_by_season(recent_season.id, team_id)
        return make_response(jsonify({"data":(top_scorers), "season": SeasonService.jsonify_season(recent_season)}))
    else:
        top_scorers = PlayerService.get_player_with_most_goals(team_id=team_id)
    
    json_players = []
    # if multiple players with same amount of goals, return them all
    if type(top_scorers) is list:
        for scorer in top_scorers:
            json_players.append(PlayerService.jsonify_player(scorer))

        return make_response(jsonify(json_players), 200)

    return make_response(jsonify(PlayerService.jsonify_player(top_scorers)), 200)


@players_bp.route("/players/mostassists/", methods=["GET"])
def get_most_assists():
    team_name = request.args.get('team_name')
    recent = request.args.get('recent')
    recent_season = None

    if recent:
        recent_season = SeasonService.get_most_recent_season()
    
    if team_name:
        team = TeamService.get_teams(team_name=team_name)
        team_id = team[0]['id'] if team else None
    else:
        team_id = None

    if recent_season:
        most_assists = PlayerService.get_most_assists_by_season(recent_season.id, team_id)
        return make_response(jsonify({"data":(most_assists), "season": SeasonService.jsonify_season(recent_season)}))
    else:
        most_assists = PlayerService.get_player_with_most_assists(team_id=team_id)

    
    json_players = []
    # if multiple players with same amount of goals, return them all
    if type(most_assists) is list:
        for assister in most_assists:
            json_players.append(PlayerService.jsonify_player(assister))

        return make_response(jsonify(json_players), 200)

    return make_response(jsonify(PlayerService.jsonify_player(most_assists)), 200)


@players_bp.route("/players/mostapps/", methods=["GET"])
def get_most_apps():
    team_name = request.args.get('team_name') or ''
    team = TeamService.get_team_by_name(team_name)
    if team is not None:
        most_apps = PlayerService.get_player_with_most_appearances(team.id)
    else:
        most_apps = PlayerService.get_player_with_most_appearances()
    json_players = []
    # if multiple players with same amount of appearances, return them all
    if type(most_apps) is list:
        for player in most_apps:
            json_players.append(PlayerService.jsonify_player(player))

        return make_response(jsonify(json_players), 200)

    return make_response(jsonify(PlayerService.jsonify_player(most_apps)), 200)

@players_bp.route("/players/<int:player_id>/season/<int:season_id>", methods=["GET"])
def get_player_stats_by_season(player_id, season_id):
    player_stats = PlayerService.get_player_stats_by_season(player_id, season_id)
    if not player_stats:
        return jsonify({"message": "Error finding player stats. Please provide valid player ID and season ID"}), 404
    
    return make_response(jsonify(player_stats), 200)

@players_bp.route("/players/<int:player_id>/goal", methods=["POST"])
@login_required
def add_goal_for_player(player_id):
    goal_data = request.get_json()
    match_id = goal_data.get("match_id")
    assisted_by_id = goal_data.get("assisted_by_id")

    goal = PlayerService.add_goal_for_player(player_id, match_id, assisted_by_id)
    
    if not goal:
        return make_response({"message": "Error adding goal, please review your data submission and try again"}, 400)
    
    return make_response({"message": "Goal successfully added"}, 201)

@players_bp.route("/players/<int:player_id>/app", methods=["POST"])
@login_required
def add_appearance_for_player(player_id):
    goal_data = request.get_json()
    match_id = goal_data.get("match_id")
    season_id = goal_data.get("season_id")

    

    app = PlayerService.add_appearance_for_player(player_id, match_id, season_id)
    
    if not app:
        return make_response({"message": "Error adding appearance, please review your data submission and try again"}, 400)
    
    return make_response({"message": "Appearance successfully added"}, 201)

    