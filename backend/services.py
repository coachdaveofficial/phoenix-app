from sqlalchemy import func, desc, asc, and_, or_
from models import db, Team, Player, Match, Goal, Assist, Appearance, PositionType, Season, User
from datetime import date, datetime
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class TeamService:
    @staticmethod
    def get_teams(team_name=None):
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
    def create_team(team_name):
        try:
            team = Team(name=team_name)
            db.session.add(team)
            db.session.commit()
            return team
        except IntegrityError:
            db.session.rollback()
            return False, {"message": "Team name you provided is currently in use. Please provide a different team name"}

    @staticmethod
    def update_team_name(team, data):
        '''Accepts Team object and JSON data containing the new team name'''

        # update the player information based on the data provided
        if "name" in data:
            team.name = data["name"]
        else:
            return False, {"message": "Must provide new name. Please try again."}

        # commit the changes to the database
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

    @staticmethod
    def get_team_stats_as_json(team_name):
        team = TeamService.get_team_by_name(team_name)
        
        if not team:
            return None

        prev_match = MatchService.jsonify_match(MatchService.get_most_recent_previous_match_by_team_id(team.id))
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
            most_goals = [PlayerService.jsonify_player(p) for p in most_goals]

        if most_assists is not None:
            most_assists = [PlayerService.jsonify_player(p) for p in most_assists]
            
        if recent_season is not None:
            recent_season = SeasonService.jsonify_season(recent_season)

        return {
            "prev_match": prev_match,
            "upcoming_match": upcoming_match,
            "most_assists": most_assists,
            "most_goals": most_goals,
            "recent_assists": recent_assists,
            "recent_goals": recent_goals,
            "recent_season": recent_season
        }

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
    def get_player_with_most_goals(team_id=None):
        # filter by team_id if provided, else get most goals regardless of team
        if team_id is not None:
            query = (
                Player.query
                .join(Goal, Goal.player_id == Player.id)
                .group_by(Player.id)
                .with_entities(Player.id, func.count(Goal.id).label('goals_count'))
                .order_by(desc(func.count(Goal.id)))
                .filter(Player.team_id == team_id)
            )
            if query.first() == None:
                return None
                
            most_goals_count = query.first().goals_count

            players_with_most_goals = (
                Player.query
                .join(Goal, Goal.player_id == Player.id)
                .group_by(Player.id)
                .having(func.count(Goal.id) == most_goals_count)
                .filter(Player.team_id == team_id)
                .all()
            )
        else:
            query = (
                Player.query
                .join(Goal, Goal.player_id == Player.id)
                .group_by(Player.id)
                .with_entities(Player.id, func.count(Goal.id).label('goals_count'))
                .order_by(desc(func.count(Goal.id)))
            )
            if query.first() == None:
                return None
            
            most_goals_count = query.first().goals_count

            players_with_most_goals = (
                Player.query
                .join(Goal, Goal.player_id == Player.id)
                .group_by(Player.id)
                .having(func.count(Goal.id) == most_goals_count)
                .all()
            )

        return players_with_most_goals

    @staticmethod
    def get_player_with_most_assists(team_id=None):
        # filter by team_id if provided, else get most assists regardless of team
        if team_id is not None:
            query = (
                Player.query
                .join(Assist)
                .group_by(Player.id)
                .with_entities(Player.id, func.count(Assist.id).label('assists_count'))
                .order_by(desc(func.count(Assist.id)))
                .filter(Player.team_id == team_id)
            )
            if query.first() == None:
                return None
            most_assists_count = query.first().assists_count

            players_with_most_assists = (
                Player.query
                .join(Assist)
                .group_by(Player.id)
                .having(func.count(Assist.id) == most_assists_count)
                .filter(Player.team_id == team_id)
                .all()
            )
        else:
            query = (
                Player.query
                .join(Assist)
                .group_by(Player.id)
                .with_entities(Player.id, func.count(Assist.id).label('assists_count'))
                .order_by(desc(func.count(Assist.id)))
            )
            if query.first() == None:
                return None
            most_assists_count = query.first().assists_count

            players_with_most_assists = (
                Player.query
                .join(Assist)
                .group_by(Player.id)
                .having(func.count(Assist.id) == most_assists_count)
                .all()
            )

        return players_with_most_assists

    @staticmethod
    def get_player_with_most_appearances(team_id=None):
        # filter by team_id if provided, else get most appearances regardless of team
        if team_id is not None:
            most_appearances_count = (
                Player.query
                .join(Appearance)
                .group_by(Player.id)
                .with_entities(Player.id, func.count(Appearance.id).label('appearances_count'))
                .order_by(desc(func.count(Appearance.id)))
                .filter(Player.team_id == team_id)
                .first()
                .appearances_count
            )

            players_with_most_appearances = (
                Player.query
                .join(Appearance)
                .group_by(Player.id)
                .having(func.count(Appearance.id) == most_appearances_count)
                .filter(Player.team_id == team_id)
                .all()
            )
        else:
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
    def get_top_goal_scorers_by_season(season_id, team_id=None):
        # Get the season and matches in the season
        season = SeasonService.get_season_by_id(season_id)
        if not season:
            return None

        matches_in_season = MatchService.get_matches_by_season_id(season_id)

        # Build the base query
        query = (
            db.session.query(
                Player,
                Team,
                func.count(Goal.id).label('goals')
            )
            .join(Goal, Goal.player_id == Player.id)
            .join(Player.team)
            .filter(Goal.match_id.in_([match.id for match in matches_in_season]))
            .group_by(Player.id, Team.id)
            .order_by(desc('goals'))
        )

        # Apply team_id filter if provided
        if team_id is not None:
            query = query.filter(Player.team_id == team_id)

        # Execute the query and fetch the results
        top_scorers_query = query.all()

        if not top_scorers_query:
            return {"message": "No goals have been recorded yet for this season", "season": SeasonService.jsonify_season(season)}

        # Find the maximum goals scored
        max_goals = top_scorers_query[0][2]  # Get the goals of the first player

        top_scorers = []

        for player, team, goals in top_scorers_query:
            player_name = f"{player.first_name} {player.last_name}"

            if goals < max_goals:
                break  # No more players with the same number of goals

            top_scorer_stats = {
                "player_name": player_name,
                "season_name": season.name,
                "team_name": team.name,
                "goals": goals,
            }

            top_scorers.append(top_scorer_stats)

        return top_scorers
    
    @staticmethod
    def get_most_assists_by_season(season_id, team_id=None):
        # Get the season and matches in the season
        season = SeasonService.get_season_by_id(season_id)
        if not season:
            return None

        matches_in_season = MatchService.get_matches_by_season_id(season_id)

        # Build the base query
        query = (
            db.session.query(
                Player,
                Team,
                func.count(Assist.id).label('assists_count')
            )
            .join(Assist, Assist.player_id == Player.id)
            .join(Player.team)
            .filter(Assist.match_id.in_([match.id for match in matches_in_season]))
            .group_by(Player.id, Team.id)
            .order_by(desc('assists_count'))
        )
        
        # Apply team_id filter if provided
        if team_id is not None:
            query = query.filter(Player.team_id == team_id)

        # Execute the query and fetch the results
        most_assists_query = query.all()

        if not most_assists_query:
            return {"message": "No assists have been recorded yet for this season", "season": SeasonService.jsonify_season(season)}

        # Find the maximum goals scored
        max_assists = most_assists_query[0][2]  # Get the goals of the first player

        most_assists = []

        for player, team, assists in most_assists_query:
            player_name = f"{player.first_name} {player.last_name}"

            if assists < max_assists:
                break  # No more players with the same number of goals

            most_assists_stats = {
                "player_name": player_name,
                "season_name": season.name,
                "team_name": team.name,
                "assists": assists,
            }

            most_assists.append(most_assists_stats)

        return most_assists



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
        match_score = MatchService.parse_score(match.score)

        return {
            "match_id": match.id,
            "date": match.date,
            "venue": match.venue,
            "season": json_season,
            "home_team": json_home,
            "away_team": json_away,
            "score": match_score,
            "goals": GoalService.jsonify_goal_scorers_and_assisters_by_match_id(match.id)
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
    def parse_score(score_str):
        '''Given a score string of "1:4" will return {'home': '1', 'away': '4', 'forfeit': False}'''
        # Split the score string by ':'
        scores = score_str.split(":")
        
        if len(scores) != 2:
            # Handle invalid score format
            return None

        home_score, away_score = scores
        
        if "forfeit" in away_score:
            # Handle forfeit result
            away_score = away_score.split("forfeit")[0]
            forfeit = True
        else:
            forfeit = False

        return {
            "home": home_score.strip(),
            "away": away_score.strip(),
            "forfeit": forfeit,
        }


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

        match = (Match.query
            .filter(
                or_(Match.home_team_id == team_id, Match.away_team_id == team_id),
                Match.date >= current_date
            )
            .order_by(asc(Match.date))
            .first()
        )
        if not match:
            return None
        return match

    @staticmethod
    def get_most_recent_previous_match_by_team_id(team_id):
        current_date = datetime.now()


        match = (Match.query
            .filter(
                or_(Match.home_team_id == team_id, Match.away_team_id == team_id),
                Match.date < current_date
            )
            .order_by(desc(Match.date))
            .first()
        )
        if not match:
            return None
        return match
   
    @staticmethod
    def get_all_previous_matches_by_team_id(team_id):
        current_date = datetime.now()
        # query for matches with past dates for the specified team
        matches = (Match.query
            .filter(
                or_(Match.home_team_id == team_id, Match.away_team_id == team_id),
                Match.date < current_date
            )
            .order_by(desc(Match.date))
            .all()
        )
        if not matches:
            return None
        return matches

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
    
    @staticmethod
    def get_season_by_name(season_name):
        season = Season.query.filter(func.lower(Season.name).ilike(
            f'%{season_name.lower()}%')).first()
        return season
    
    @staticmethod
    def get_most_recent_season():
        season = Season.query.order_by(desc(Season.end_date)).first()
        return season

class GoalService:
    @staticmethod
    def jsonify_goal_scorers_and_assisters_by_match_id(match_id):
        # Query the goals and assists for the given match
        goals_and_assists = (
            db.session.query(Goal, Assist)
            .filter(Goal.match_id == match_id)
            .join(Assist, Goal.id == Assist.for_goal_id, isouter=True)
            .all()
        )

        # Create lists to store goal scorer and assister data in JSON format
        goal_scorers = []
        assisters = []
        goals = []

        # Iterate through the goals and fetch player data
        for goal, assist in goals_and_assists:
            if not goal: return

            player = goal.players

            if not player: return

            goal = {}

            goal['scorer'] = {
                "player_id": player.id,
                "first_name": player.first_name,
                "last_name": player.last_name,
                "team_id": player.team_id,
                "team_name": player.team.name if player.team else None,
            }

            if not assist: return

            player = assist.players

            if not player: return

            goal['assist'] = {
                "player_id": player.id,
                "first_name": player.first_name,
                "last_name": player.last_name,
                "team_id": player.team_id,
                "team_name": player.team.name if player.team else None,
            }
            goals.append(goal)

        return goals
