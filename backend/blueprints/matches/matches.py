from flask import Blueprint, jsonify, make_response, request, redirect, flash, g
from services import MatchService
from blueprints.auth.auth import login_required

matches_bp = Blueprint("matches", __name__)

@matches_bp.route('/matches/<int:team_id>/upcoming/', methods=["GET"])
def get_upcoming_match(team_id):
    upcoming = MatchService.get_next_upcoming_match_by_team_id(team_id)
    if not upcoming:
        return jsonify({"message": "No upcoming matches for this team"}), 404
    return make_response(MatchService.jsonify_match(upcoming), 200)

@matches_bp.route('/matches/<int:team_id>/previous/', methods=["GET"])
def get_previous_match(team_id):
    previous = MatchService.get_most_recent_previous_match_by_team_id(team_id)
    if not previous:
        return jsonify({"message": "No previous matches for this team"}), 404
    return make_response(MatchService.jsonify_match(previous), 200)

@matches_bp.route('/matches/<int:team_id>/previous/all', methods=["GET"])
def get_previous_match_list(team_id):
    previous_matches = MatchService.get_all_previous_matches_by_team_id(team_id)
    if not previous_matches:
        return jsonify({"message": "No previous matches for this team"}), 404
    match_list = [MatchService.jsonify_match(match) for match in previous_matches]
    return make_response(match_list, 200)