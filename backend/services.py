
from models import db, Team, Player, Match, Goal, Assist, Appearance

class TeamService:
    @staticmethod
    def get_all_teams():
        return Team.query.all()

    @staticmethod
    def get_team_by_id(team_id):
        return Team.query.get(team_id)
    
    @staticmethod
    def get_team_by_name(team_name):
        return Team.query.filter_by(name=team_name).first()


class PlayerService:
    @staticmethod
    def get_all_players():
        return Player.query.all()

    @staticmethod
    def get_player_by_id(player_id):
        return Player.query.get(player_id)

    @staticmethod
    def get_goals_by_player_id(player_id):
        return Goal.query.filter_by(player_id=player_id).all()

    @staticmethod
    def get_assists_by_player_id(player_id):
        return Assist.query.filter_by(player_id=player_id).all()

    @staticmethod
    def get_appearances_by_player_id(player_id):
        return Appearance.query.filter_by(player_id=player_id).all()


class MatchService:
    @staticmethod
    def get_all_matches():
        return Match.query.all()

    @staticmethod
    def get_match_by_id(match_id):
        return Match.query.get(match_id)

    @staticmethod
    def get_goals_by_match_id(match_id):
        return Goal.query.filter_by(match_id=match_id).all()

    @staticmethod
    def get_assists_by_match_id(match_id):
        return Assist.query.filter_by(match_id=match_id).all()
    
    @staticmethod
    def get_match_score(match):
        """Calculate and return the score for the given match. Returns [home_team_score, away_team_score]"""
        home_team_score = sum(goal.points for goal in match.goals if goal.team_id == match.home_team_id)
        away_team_score = sum(goal.points for goal in match.goals if goal.team_id == match.away_team_id)
        return home_team_score, away_team_score



class GoalService:
    @staticmethod
    def get_all_goals():
        return Goal.query.all()


class AssistService:
    @staticmethod
    def get_all_assists():
        return Assist.query.all()


class AppearanceService:
    @staticmethod
    def get_all_appearances():
        return Appearance.query.all()