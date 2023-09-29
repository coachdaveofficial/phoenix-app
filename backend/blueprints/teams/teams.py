from flask import Blueprint, jsonify, make_response, request
from services import TeamService, MatchService, PlayerService, SeasonService
from models import PositionType
from blueprints.auth.auth import login_required

teams_bp = Blueprint("teams", __name__)

@teams_bp.route("/teams/", methods=["GET"])
def teams():
    name = request.args.get("name")

    if name:
        teams_list = TeamService.get_teams(name)
    else:
        teams_list = TeamService.get_teams()

    if not teams_list:
        return make_response(jsonify({"message": "Team(s) not found."}), 404)
    
    result = []
    for t in teams_list:
        result.append(t)

    return make_response(jsonify(result), 200)

@teams_bp.route("/teams/<int:team_id>", methods=["GET"])
def get_team(team_id):
    team = TeamService.get_team_by_id(team_id)

    try: 
        return make_response(jsonify(TeamService.jsonify_team(team)), 200)
    except Exception as e:
        return make_response(jsonify({"message": "Team not found."}), 404)

        
@teams_bp.route("/teams/<int:team_id>", methods=["DELETE", "PUT"])
@login_required
def update_or_delete_team(team_id):
    team = TeamService.get_team_by_id(team_id)
    if not team:
        return jsonify({"message": "Team not found"}), 404
    
    if request.method == "PUT":

        data = request.get_json()

        if not data:
            return jsonify({"message": "Invalid data provided"}), 400

        success, response = TeamService.update_team_name(team, data)

        if success:
            return jsonify(response), 200
        else:
            return jsonify(response), 500
    
    elif request.method == "DELETE":

        success, response = TeamService.delete_team(team)

        if success:
            return jsonify(response), 200
        else:
            return jsonify(response), 500
        

@teams_bp.route("/teams/stats/", methods=["GET"])
def get_team_stats():
    team_name = request.args.get('team_name')
    if team_name:
        team_stats = TeamService.get_team_stats_as_json(team_name)
        if not team_stats:
            return make_response({"message": "Could not find team, please check the provided team name and try again"}, 400)
        
        return make_response(team_stats, 200)
    
    open_stats = TeamService.get_team_stats_as_json("open")
    thirty_stats = TeamService.get_team_stats_as_json("o30")
    forty_stats = TeamService.get_team_stats_as_json("o40")

    return make_response({"openStats": open_stats, "overThirtyStats": thirty_stats, "overFortyStats": forty_stats}, 200)
    
    