import gspread
import re
from datetime import datetime
from models import db, Player, Team, Match, Goal, Assist, PositionType, Season
from sqlalchemy import func

class SeasonDataExtractor:
    def __init__(self, service_account_file, sheet_name):
        self.sa = gspread.service_account(filename=service_account_file)
        self.sh = self.sa.open(sheet_name)

    def get_team_name(self, team_name, team_type):
        team_name_lower = team_name.lower()
        team_type = team_type.lower()

        if 'phoenix fc' in team_name_lower:
            if team_type == 'open':
                return 'Phoenix FC Open'
            elif team_type == 'o30':
                return 'Phoenix FC O30'
            elif team_type == 'o40':
                return 'Phoenix FC O40'

        return team_name

    def extract_season_data(self, data):

        header_patterns = [['GAME#', 'Date', 'Time', 'Home', 'MR', 'Away', 'Location'], ['GAME#', 'EDIT', 'Date', 'Time', 'Home', '', 'Away'], ['GAME#', 'Date', 'Time', 'Home', '', 'Away', 'Location']]

        # Initialize an empty list to store the season data
        season = []

        # Initialize a dictionary to store the current game data
        current_game = {}

        previous_row_empty = False

        # Find the index where game info starts
        header_index = None
        for idx, row in enumerate(data):

            if row in header_patterns:
                header_index = idx
                break

            
        # Iterate through the rows in the data, starting from the row after the header_pattern
        for row in data[header_index + 1:]:

            # Check if the row is empty or does not have the expected number of elements
            if not row or len(row) < 2:
                if previous_row_empty:
                    break
                else:
                    previous_row_empty = True
                continue

            # If any element in the row is empty, break the loop only if two consecutive rows are empty
            if not any(row):
                if previous_row_empty:
                    break
                else:
                    previous_row_empty = True
            else:
                previous_row_empty = False

             # Check if the first cell (GAME#) contains numbers
            if str(row[0]).isdigit():
                # If a new game is encountered and the current game dictionary is not empty,
                # append the current_game dictionary to the season list
                if current_game:
                    season.append(current_game.copy())

                # Create a new dictionary for the current game
                current_game = {
                    'game_id': row[0],
                    'date': row[1],
                    'time': row[2],
                    'home': row[3],
                    'score': row[4],
                    'away': row[5],
                    'location': row[6],
                    'goals': []  # Initialize an empty list to store goal information for the current game
                }
            else:
                # If the row does not start with a number (e.g., it contains goal information)
                # Extract goal scorer and assisted-by information using regular expressions
                goal_scorers = []
                assisted_by = ''
                for item in row:
                    if item:
                        # looking for Name (g), Name (G), Name (a), Name (A), Name(g, pk)
                        match = re.search(r'(\w+)\s+\((g|G|a|A|g, pk)\)', item)
                        if match:
                            player_name = match.group(1)
                            event_type = match.group(2)
                            if event_type.lower() == 'g':
                                goal_scorers.append(player_name)
                            elif event_type.lower() == 'a':
                                assisted_by = player_name

                # Add the goal information to the current game dictionary
                for goal_scorer in goal_scorers:
                    if not current_game:
                        break
                    current_game['goals'].append({
                        'goal_scorer': goal_scorer,
                        'assisted_by': assisted_by
                    })

        # After the loop ends, check if there is any remaining data in the current_game dictionary
        # and if so, append it to the season list
        if current_game:
            season.append(current_game.copy())

        return season

    def insert_data(self, data_list):
        for data in data_list:
            year = data['year']
            season_name = data['season']
            team_type = data['team_type']
            worksheet = self.sh.worksheet(data['worksheet'])
            worksheet_cells = worksheet.get("A1:G100")
            worksheet_data = self.extract_season_data(worksheet_cells)

            for game in worksheet_data:

                # Parse the date and set the year
                date_str = game['date'] + ' ' + year
                time_str = game['time']
                match_datetime = datetime.strptime(date_str + ' ' + time_str, '%a %b %d %Y %I:%M %p')

                            
                # Create or get home and away teams
                home_team_name = game['home']
                away_team_name = game['away']

                if home_team_name.startswith('Phoenix FC'):
                    home_team_name = self.get_team_name(home_team_name, team_type)

                if away_team_name.startswith('Phoenix FC'):
                    away_team_name = self.get_team_name(away_team_name, team_type)

                home_team = Team.query.filter_by(name=home_team_name).first()
                if not home_team:
                    home_team = Team(name=home_team_name)
                    db.session.add(home_team)

                away_team = Team.query.filter_by(name=away_team_name).first()
                if not away_team:
                    away_team = Team(name=away_team_name)
                    db.session.add(away_team)

                db.session.commit()

                phoenix_id = home_team.id if home_team_name.startswith("Phoenix") else away_team.id

                 # Check if the match already exists in the database by matching the date, venue, and team IDs
                existing_match = Match.query.filter(
                    Match.date == match_datetime,
                    Match.venue == game['location'],
                    Match.home_team_id == home_team.id,
                    Match.away_team_id == away_team.id
                ).first()

                if existing_match:
                    print(f"Match already exists: {existing_match.id}")
                    continue

                
                season = Season.query.filter_by(name=f'{season_name} {year}').first()
                if not season:
                    season = Season(name=f'{season_name} {year}', start_date=match_datetime)
                    db.session.add(season)
                db.session.commit()  
                if season.start_date < match_datetime:  
                    season.end_date = match_datetime
                    db.session.commit()
                # Create a match
                match = Match(
                    date=match_datetime,
                    venue=game['location'],
                    season_id=season.id,
                    home_team_id=home_team.id,
                    away_team_id=away_team.id,
                    score=game['score']
                )
                db.session.add(match)
                db.session.commit()


                # Create players and their goals/assists
                for goal_data in game['goals']:
                    goal_scorer_name = goal_data['goal_scorer']
                    assisted_by_name = goal_data['assisted_by']
                    print('scorer', goal_scorer_name)
                    print('assist', assisted_by_name)
                    print('match', match.id)

                    # Convert both the goal_scorer_name and the column values to lowercase for case-insensitive matching
                    goal_scorer_name_lower = goal_scorer_name.lower()

                    goal_scorer = (
                        Player.query
                        .filter(func.lower(Player.first_name).ilike(goal_scorer_name_lower) |
                                func.lower(Player.last_name).ilike(goal_scorer_name_lower))
                        .filter(Player.team_id == phoenix_id)
                        .first()
                    )
                    if not goal_scorer:

                        goal_scorer = Player(first_name=goal_scorer_name, last_name='', position=PositionType.forward, team_id=phoenix_id)
                        db.session.add(goal_scorer)
                        db.session.commit()

                    # Convert both the assisted_by_name and the column values to lowercase for case-insensitive matching
                    assisted_by_name_lower = assisted_by_name.lower()

                    assisted_by = (
                        Player.query
                        .filter(func.lower(Player.first_name).ilike(assisted_by_name_lower) |
                                func.lower(Player.last_name).ilike(assisted_by_name_lower))
                        .filter(Player.team_id == phoenix_id)
                        .first()
                    )
                    if not assisted_by:
                        if assisted_by_name:
                            assisted_by = Player(first_name=assisted_by_name, last_name='', position=PositionType.forward, team_id=phoenix_id)
                            db.session.add(assisted_by)
                            db.session.commit()

                    # Create the goal
                    goal = Goal(player_id=goal_scorer.id, match_id=match.id)
                    db.session.add(goal)
                    db.session.commit()

                    # Create the assist if applicable
                    if assisted_by_name:
                        assist = Assist(player_id=assisted_by.id, match_id=match.id, for_goal_id=goal.id)
                        db.session.add(assist)
                        db.session.commit()

        print("Data insertion successful!")


    
   

