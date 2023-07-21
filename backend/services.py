
from models import db, Team, Player, Match, Goal, Assist, Appearance, PositionType

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
    def jsonify_player(p):
        position_mapping = {
            PositionType.forward: "forward",
            PositionType.midfielder: "midfielder",
            PositionType.defender: "defender",
            PositionType.goalkeeper: "goalkeeper",
        }
        return {
                "id": p.id,
                "player_name": f'{p.first_name} {p.last_name}',
                "position": position_mapping.get(p.position),
                "team": p.team.name,
                "appearances": len([app for app in p.apps]),
                "goals": len([g for g in p.goals]),
                "assists": len([a for a in p.assists]),
                "yellow_cards": len([y for y in p.yellow_cards]),
                "red_cards": len([r for r in p.red_cards]),
             }
    @staticmethod
    def create_player_from_json(json_data):
        # Extract data from JSON
        first_name = json_data.get('first_name')
        last_name = json_data.get('last_name')
        position_str = json_data.get('position')
        team_id = json_data.get('team_id')


        if not first_name or not last_name or not position_str or not team_id:
            raise ValueError("Missing required fields")

        # Convert the position string to the PositionType enum
        position = getattr(PositionType, position_str.lower(), None)
        if not position:
            raise ValueError("Invalid position")
        
        existing_player = PlayerService.get_player_by_full_name(first_name=first_name, last_name=last_name)
        if existing_player:
            raise ValueError("Player by that name already exists")


        player = Player(
            first_name=first_name,
            last_name=last_name,
            position=position,
            team_id=team_id
        )

        db.session.add(player)
        db.session.commit()

        return player

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
    
    @staticmethod
    def get_player_by_full_name(first_name, last_name):
        player = Player.query.filter_by(first_name=first_name, last_name=last_name).first()
            
        if not player:
            return None
        
        return player


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