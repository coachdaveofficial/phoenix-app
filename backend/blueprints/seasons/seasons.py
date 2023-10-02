from flask import Blueprint, jsonify, make_response, request
from services import SeasonService
from models import PositionType
from blueprints.auth.auth import login_required

seasons_bp = Blueprint("seasons", __name__)

@seasons_bp.route("/seasons/recent", methods=["GET"])
def most_recent_season():
    recent_season = SeasonService.get_most_recent_season()

    return make_response(SeasonService.jsonify_season(recent_season), 200)

