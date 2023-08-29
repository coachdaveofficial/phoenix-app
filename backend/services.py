from sqlalchemy import func, desc, asc
from models import db, Team, Player, Match, Goal, Assist, Appearance, PositionType, Season, User
from datetime import date, datetime
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class TeamService:
    @staticmethod
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

    @staticmethod
    def get_team_by_id(team_id):
        team = Team.query.get(team_id)
        if not team:
            return False
        return team

    @staticmethod
    def get_team_by_name(team_name):
        # Perform a case-insensitive search using ilike
        team = Team.query.filter(func.lower(Team.name).ilike(
            f'%{team_name.lower()}%')).first()
        return team

    @staticmethod
    def jsonify_team(team):
        return {
            "id": team.id,
            "name": team.name,
            "players": [PlayerService.jsonify_player(p) for p in team.players],
        }

    @staticmethod
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

    @staticmethod
    def delete_team(team):
        try:
            db.session.delete(team)
            db.session.commit()
            return True, {"message": "Team deleted successfully"}
        except Exception as e:
            db.session.rollback()
            return False, {"message": "Failed to delete team"}


class PlayerService:

    @staticmethod
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

        existing_player = PlayerService.get_player_by_full_name(
            first_name=first_name, last_name=last_name)
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
    def get_multiple_players_by_id(player_ids):
        '''player_ids is a list of player_id values'''
        return Player.query.filter(Player.id.in_(player_ids)).all()

    @staticmethod
    def get_player_by_full_name(first_name, last_name):
        player = Player.query.filter_by(
            first_name=first_name, last_name=last_name).first()

        if not player:
            return None

        return player

    @staticmethod
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

    @staticmethod
    def delete_player(player):
        try:
            db.session.delete(player)
            db.session.commit()
            return True, {"message": "Player deleted successfully"}
        except Exception as e:
            db.session.rollback()
            return False, {"message": "Failed to delete player"}

    @staticmethod
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
            query = query.join(Player.team).filter(
                Team.name.ilike(f'%{team}%'))

        return query.all()

    @staticmethod
    def get_player_with_most_goals():

        most_goals_count = (
            Player.query
            .join(Goal)
            .group_by(Player.id)
            .with_entities(Player.id, func.count(Goal.id).label('goals_count'))
            .order_by(desc(func.count(Goal.id)))
            .first()
            .goals_count
        )

        players_with_most_goals = (
            Player.query
            .join(Goal)
            .group_by(Player.id)
            .having(func.count(Goal.id) == most_goals_count)
            .all()
        )
        return players_with_most_goals

    @staticmethod
    def get_player_with_most_assists():
        most_assists_count = (
            Player.query
            .join(Assist)
            .group_by(Player.id)
            .with_entities(Player.id, func.count(Assist.id).label('assists_count'))
            .order_by(desc(func.count(Assist.id)))
            .first()
            .assists_count
        )

        players_with_most_assists = (
            Player.query
            .join(Assist)
            .group_by(Player.id)
            .having(func.count(Assist.id) == most_assists_count)
            .all()
        )
        return players_with_most_assists

    @staticmethod
    def get_player_with_most_appearances():
        most_appearances_count = (
            Player.query
            .join(Appearance)
            .group_by(Player.id)
            .with_entities(Player.id, func.count(Appearance.id).label('appearances_count'))
            .order_by(desc(func.count(Appearance.id)))
            .first()
            .appearances_count
        )

        players_with_most_appearances = (
            Player.query
            .join(Appearance)
            .group_by(Player.id)
            .having(func.count(Appearance.id) == most_appearances_count)
            .all()
        )
        return players_with_most_appearances

    @staticmethod
    def get_player_stats_by_season(player_id, season_id):
        player = Player.query.get(player_id)
        if not player:
            return None

        season = SeasonService.get_season_by_id(season_id)
        if not season:
            return None

        matches_in_season = MatchService.get_matches_by_season_id(season_id)

        goals = Goal.query.filter(Goal.player_id == player_id, Goal.match_id.in_(
            [match.id for match in matches_in_season])).count()
        assists = Assist.query.filter(Assist.player_id == player_id, Assist.match_id.in_(
            [match.id for match in matches_in_season])).count()
        appearances = Appearance.query.filter(Appearance.player_id == player_id, Appearance.match_id.in_([
                                              match.id for match in matches_in_season])).count()

        player_stats = {
            "player_name": f"{player.first_name} {player.last_name}",
            "season_name": season.name,
            "goals": goals,
            "assists": assists,
            "appearances": appearances,
        }

        return player_stats

    @staticmethod
    def add_goal_for_player(player_id, match_id, assisted_by_id):
        # Get the player and match objects
        player = PlayerService.get_player_by_id(player_id)
        match = MatchService.get_match_by_id(match_id)
        assister = PlayerService.get_player_by_id(assisted_by_id)

        if not player or not match:
            return None

        # Create a new Goal instance
        goal = Goal(player_id=player_id, match_id=match_id)

        # Update the player's goals and the match's goals
        player.goals.append(goal)
        match.goals.append(goal)

        db.session.add(goal)
        db.session.commit()

        if assister:
            assist = Assist(player_id=player_id,
                            match_id=match_id, for_goal_id=goal.id)
            db.session.add(assist)
            db.session.commit()

        return goal

    @staticmethod
    def add_appearance_for_player(player_id, match_id, season_id):
        # Get the player and match objects
        player = PlayerService.get_player_by_id(player_id)
        season = SeasonService.get_season_by_id(season_id)
        match = MatchService.get_match_by_id(match_id)

        if not player or not season or not match:
            return None

        # Create a new Appearance instance
        app = Appearance(player_id=player_id,
                         match_id=match_id, season_id=season_id)

        # Update the player's appearances
        player.apps.append(app)

        db.session.add(app)
        db.session.commit()

        return app


class MatchService:

    @staticmethod
    def jsonify_match(match):
        json_season = SeasonService.jsonify_season(match.season)
        json_home = TeamService.jsonify_team(match.home_team)
        json_away = TeamService.jsonify_team(match.away_team)
        home_score, away_score = MatchService.get_match_score(match)

        return {
            "match_id": match.id,
            "date": match.date,
            "venue": match.venue,
            "season": json_season,
            "home_team": json_home,
            "away_team": json_away,
            "score": {"home": home_score, "away": away_score}


        }

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
        home_team_score = 0
        away_team_score = 0
        for goal in match.goals:
            if goal.team_id == match.home_team_id:
                home_team_score += 1
            if goal.team_id == match.away_team_id:
                away_team_score += 1
        # home_team_score = sum(goal for goal in match.goals if goal.team_id == match.home_team_id)
        # away_team_score = sum(goal for goal in match.goals if goal.team_id == match.away_team_id)
        return home_team_score, away_team_score

    @staticmethod
    def get_matches_by_season_id(season_id):
        return Match.query.filter_by(season_id=season_id).all()

    @staticmethod
    def get_matches_by_day(day):
        '''day is a datetime.date object'''
        return Match.query.filter(Match.date == day).all()

    @staticmethod
    def get_next_upcoming_match_by_team_id(team_id):
        current_date = datetime.now()

        # query for matches with future dates for the specified team
        upcoming_match = Match.query.filter(
            (Match.home_team_id == team_id or Match.away_team_id == team_id)
        ).order_by(asc(Match.date)).first()

        if current_date > upcoming_match.date:
            return None

        return upcoming_match

    @staticmethod
    def get_most_recent_previous_match_by_team_id(team_id):
        current_date = datetime.now()

        # query for matches with past dates for the specified team
        previous_match = Match.query.filter(
            (Match.home_team_id == team_id or Match.away_team_id == team_id)
        ).order_by(desc(Match.date)).first()

        if current_date < previous_match.date:
            return None

        return previous_match


class UserService:
    """Services for getting user info"""

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        try:
            user = User(
                username=username,
                email=email,
                password=hashed_pwd
            )

            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            return None

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = User.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False


class SeasonService:
    """Services for getting season info"""

    @staticmethod
    def jsonify_season(season):
        return {
            "season_id": season.id,
            "name": season.name,
            "start_date": season.start_date,
            "end_date": season.end_date
        }

    @staticmethod
    def get_season_by_id(season_id):
        season = Season.query.get(season_id)

        if not season:
            return None
        return season
