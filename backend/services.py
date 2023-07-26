from sqlalchemy import func, desc
from models import db, Team, Player, Match, Goal, Assist, Appearance, PositionType
from datetime import date

class TeamService:
    @classmethod
    def get_all_teams(team_name=None):
        # Get all teams or filter by name if provided

        team_name_mapping = {
            "open": "Phoenix FC Open",
            "o30": "Phoenix FC O30",
            "o40": "Phoenix FC O40",
            "over 30": "Phoenix FC O30",
            "over 40": "Phoenix FC O40",
        }

        # Check if the provided team_name matches any variation in the mapping
        if team_name and team_name.lower() in team_name_mapping:
            team_name = team_name_mapping[team_name.lower()]

        if team_name:
            # Retrieve a single team if team_name is provided
            teams = [TeamService.get_team_by_name(team_name)]
        else:
            # Retrieve all teams when team_name is not provided
            teams = Team.query.all()

        # If search yields no results
        if None in teams:
            return False

        # Convert teams to JSON format
        return [TeamService.jsonify_team(team) for team in teams]

    @classmethod
    def get_team_by_id(team_id):
        team = Team.query.get(team_id)
        if not team:
            return False
        return team
    
    @classmethod
    def get_team_by_name(team_name):
        # Perform a case-insensitive search using ilike
        team = Team.query.filter(func.lower(Team.name).ilike(f'%{team_name.lower()}%')).first()
        return team
            
    @classmethod
    def jsonify_team(team):
        return {
            "id": team.id,
            "name": team.name,
            "players": [PlayerService.jsonify_player(p) for p in team.players],
        }

    @classmethod
    def update_team_name(team, data):
        '''Accepts Team object and JSON data containing the new team name'''
                
         # Update the player information based on the data provided
        if "name" in data:
            team.name = data["name"]
        else:
            return False, {"message": "Must provide new name. Please try again."}

        # Commit the changes to the database
        try:
            db.session.commit()
            return True, {"message": "Team name updated successfully"}

        except Exception as e:
            db.session.rollback()
            return False, {"message": "Failed to update team name"}

    @classmethod
    def delete_team(team):
        try:
            db.session.delete(team)
            db.session.commit()
            return True, {"message": "Team deleted successfully"}
        except Exception as e:
            db.session.rollback()
            return False, {"message": "Failed to delete team"}
class PlayerService:

    @classmethod
    def jsonify_player(p):
        '''Turn Player object into a JSON format'''
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
    @classmethod
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

    @classmethod
    def get_all_players():
        return Player.query.all()

    @classmethod
    def get_player_by_id(player_id):
        return Player.query.get(player_id)

    @classmethod
    def get_multiple_players_by_id(player_ids):
        '''player_ids is a list of player_id values'''
        return Player.query.filter(Player.id.in_(player_ids)).all()
    
    @classmethod
    def get_player_by_full_name(first_name, last_name):
        player = Player.query.filter_by(first_name=first_name, last_name=last_name).first()
            
        if not player:
            return None
        
        return player

    @classmethod
    def update_player(player, data):
        '''Accepts Player object and JSON data for the fields that will be updated such as first_name, last_name, position, etc.'''
                
         # Update the player information based on the data provided
        if "first_name" in data:
            player.first_name = data["first_name"]

        if "last_name" in data:
            player.last_name = data["last_name"]

        if "position" in data:
            # Convert position string to the corresponding Enum value
            position_str = data["position"]
            position_enum = getattr(PositionType, position_str, None)

            if not position_enum:
                return False, {"message": "Invalid position value"}

            player.position = position_enum

        if "team_id" in data:
            player.team_id = data["team_id"]

        # Commit the changes to the database
        try:
            db.session.commit()
            return True, {"message": "Player information updated successfully"}

        except Exception as e:
            db.session.rollback()
            return False, {"message": "Failed to update player information"}

    @classmethod
    def delete_player(player):
        try:
            db.session.delete(player)
            db.session.commit()
            return True, {"message": "Player deleted successfully"}
        except Exception as e:
            db.session.rollback()
            return False, {"message": "Failed to delete player"}

    @classmethod
    def filter_players(first_name=None, last_name=None, position=None, team=None):
        query = Player.query

        if first_name:
            query = query.filter(Player.first_name.ilike(f'%{first_name}%'))

        if last_name:
            query = query.filter(Player.last_name.ilike(f'%{last_name}%'))

        if position:
            position_enum = PositionType[position]
            query = query.filter(Player.position == position_enum)

        if team:
            query = query.join(Player.team).filter(Team.name.ilike(f'%{team}%'))

        return query.all()

    @classmethod
    def get_player_with_most_goals():
        player_with_most_goals = (
            Player.query
            .join(Goal)
            .group_by(Player.id)
            .order_by(desc(Goal.id))  # Sort in descending order based on number of goals
            .first()
        )
        return player_with_most_goals
    
    @classmethod
    def get_player_with_most_assists():
        player_with_most_assists = (
            Player.query
            .join(Assist)
            .group_by(Player.id)
            .order_by(desc(Assist.id))  # Sort in descending order based on number of assists
            .first()
        )
        return player_with_most_assists
    
    @classmethod
    def get_player_with_most_appearances():
        player_with_most_appearances = (
            Player.query
            .join(Appearance)
            .group_by(Player.id)
            .order_by(desc(Appearance.id))  # Sort in descending order based on number of appearances
            .first()
        )
        return player_with_most_appearances
class MatchService:
    @classmethod
    def get_all_matches():
        return Match.query.all()

    @classmethod
    def get_match_by_id(match_id):
        return Match.query.get(match_id)

    @classmethod
    def get_goals_by_match_id(match_id):
        return Goal.query.filter_by(match_id=match_id).all()

    @classmethod
    def get_assists_by_match_id(match_id):
        return Assist.query.filter_by(match_id=match_id).all()
    
    @classmethod
    def get_match_score(match):
        """Calculate and return the score for the given match. Returns [home_team_score, away_team_score]"""
        home_team_score = sum(goal.points for goal in match.goals if goal.team_id == match.home_team_id)
        away_team_score = sum(goal.points for goal in match.goals if goal.team_id == match.away_team_id)
        return home_team_score, away_team_score

    @classmethod
    def get_matches_by_season(season_id):
        return Match.query.filter_by(season_id=season_id).all()
    
    @classmethod
    def get_matches_by_day(day):
        '''day is a datetime.date object'''
        return Match.query.filter(Match.date == day).all()
