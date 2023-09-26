from flask import Blueprint, jsonify, make_response, request
from services import TeamService, MatchService, PlayerService, SeasonService

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/teamdata/", methods=["GET"])
def get_team_data():
    team_name = request.args.get('team_name')

    team = TeamService.get_team_by_name(team_name)
    if not team:
        return make_response({"message": "Could not find team, please check the provided team name and try again"}, 400)
    
    
    prev_match = MatchService.jsonify_match(MatchService.get_most_recent_previous_match_by_team_id(team.id))
    # upcoming match will be None if no upcoming match data available
    upcoming_match = MatchService.get_next_upcoming_match_by_team_id(team.id)
    try:
        upcoming_match = MatchService.jsonify_match(upcoming_match)
    except AttributeError:
        upcoming_match = None

    most_goals = PlayerService.get_player_with_most_goals(team.id)
    most_assists = PlayerService.get_player_with_most_assists(team.id)
    recent_season = SeasonService.get_most_recent_season()
    recent_goals = PlayerService.get_top_goal_scorers_by_season(recent_season.id, team.id)
    recent_assists = PlayerService.get_most_assists_by_season(recent_season.id, team.id)
    if most_goals is not None:
        most_goals_list = [PlayerService.jsonify_player(p) for p in most_goals]
    else:
        most_goals_list = None
    if most_assists is not None:
        most_assists_list = [PlayerService.jsonify_player(p) for p in most_assists]
    else: 
        most_assists_list = None
    if recent_season is not None:
        recent_season = SeasonService.jsonify_season(recent_season)

    return make_response({
        "prev_match": prev_match,
        "upcoming_match": upcoming_match,
        "most_assists": most_assists_list,
        "most_goals": most_goals_list,
        "recent_assists": recent_assists,
        "recent_goals": recent_goals,
        "recent_season": recent_season
    }, 200)