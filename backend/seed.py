from models import db, PositionType, Player
from services import TeamService, PlayerService




def seed_players():
    open_team = TeamService.get_team_by_name("Phoenix FC Open")
    if not open_team:
         open_team = TeamService.create_team("Phoenix FC Open")
    
    players_data = [
        {'first_name': 'David', 'last_name': 'Falson', 'position': PositionType.midfielder, 'team_id': open_team.id},
        {'first_name': 'Michael', 'last_name': 'Smolinsky', 'position': PositionType.defender, 'team_id': open_team.id},
        {'first_name': 'Danny', 'last_name': 'Escalante', 'position': PositionType.midfielder, 'team_id': open_team.id},
        {'first_name': 'Benjamin', 'last_name': 'Haefs', 'position': PositionType.midfielder, 'team_id': open_team.id},
        {'first_name': 'Alex', 'last_name': 'Hilario', 'position': PositionType.defender, 'team_id': open_team.id},
        {'first_name': 'Timothy', 'last_name': 'Knowlton', 'position': PositionType.midfielder, 'team_id': open_team.id},
        {'first_name': 'Oscar', 'last_name': 'Munguia', 'position': PositionType.goalkeeper, 'team_id': open_team.id},
        {'first_name': 'Trey', 'last_name': 'Petersonwood', 'position': PositionType.midfielder, 'team_id': open_team.id},
        {'first_name': 'Benjamin', 'last_name': 'Ross', 'position': PositionType.defender, 'team_id': open_team.id},
        {'first_name': 'Trevor', 'last_name': 'Snodgrass', 'position': PositionType.forward, 'team_id': open_team.id},
        {'first_name': 'Zach', 'last_name': 'Sortino', 'position': PositionType.midfielder, 'team_id': open_team.id},
        {'first_name': 'Hakim', 'last_name': 'Hussein', 'position': PositionType.forward, 'team_id': open_team.id},
        {'first_name': 'Jay', 'last_name': 'Reyes', 'position': PositionType.midfielder, 'team_id': open_team.id},
        {'first_name': 'Kawika', 'last_name': 'Jacang', 'position': PositionType.midfielder, 'team_id': open_team.id},
        {'first_name': 'Evrim', 'last_name': 'Icoz', 'position': PositionType.midfielder, 'team_id': open_team.id},
        {'first_name': 'James', 'last_name': 'King', 'position': PositionType.forward, 'team_id': open_team.id},
        {'first_name': 'Kyle', 'last_name': 'Stubblefield', 'position': PositionType.midfielder, 'team_id': open_team.id},
        {'first_name': 'Saad', 'last_name': 'Imrani', 'position': PositionType.midfielder, 'team_id': open_team.id},
        {'first_name': 'Jordan', 'last_name': 'Steiner', 'position': PositionType.midfielder, 'team_id': open_team.id},
        {'first_name': 'Evan', 'last_name': 'Seach', 'position': PositionType.midfielder, 'team_id': open_team.id},
        {'first_name': 'Jacob', 'last_name': 'Shell', 'position': PositionType.midfielder, 'team_id': open_team.id},
        {'first_name': 'Anthony', 'last_name': 'Fruit', 'position': PositionType.midfielder, 'team_id': open_team.id}
    ]

    for player_data in players_data:
        existing_player = PlayerService.get_player_by_full_name(player_data['first_name'], player_data['last_name'])

        if existing_player:
            # Player already exists, update their information if needed
            existing_player.position = player_data['position']
        else:
            # Player does not exist, create a new player
            player = Player(**player_data)
            db.session.add(player)

    db.session.commit()

def seed_o30():
        over30_team = TeamService.get_team_by_name("Phoenix FC O30")
        if not over30_team:
            over30_team = TeamService.create_team("Phoenix FC O30")
        
        full_names = [
                    'Brian Peschka',
                    'Eric Bell',
                    'Alek Vante',
                    'Ian Royer',
                    'Justin Warber',
                    'Alex McVay',
                    'Dane Moore',
                    'Mike Driggs',
                    'Erin Bricker',
                    'Matt Gregor',
                    'Quinn Kuranz',
                    'Nabil Zerizef',
                    'Brian Krieger',
                    'Brian Lowe',
                    'Jack Carroll',
                    'Cole Mahaffey',
                    'Alex Zamora',
                    'Raul Granados',
                    'Eric Perez',
                    'Matt Benes',
                    'Joe Bennis',
                    'Sam Masters'
                ]


        over30_team_id = over30_team.id

        # Create the player data list
        players_data = []

        for full_name in full_names:
            first_name, last_name = full_name.split(' ')
            player = {
                'first_name': first_name,
                'last_name': last_name,
                'position': PositionType.midfielder,
                'team_id': over30_team_id,
            }
            players_data.append(player)
        
        for player_data in players_data:
            existing_player = PlayerService.get_player_by_full_name(player_data['first_name'], player_data['last_name'])

            if existing_player:
                # Player already exists, update their information if needed
                existing_player.position = player_data['position']
            else:
                # Player does not exist, create a new player
                player = Player(**player_data)
                db.session.add(player)

        db.session.commit()

def seed_o40():
        over40_team = TeamService.get_team_by_name("Phoenix FC O40")
        if not over40_team:
             over40_team = TeamService.create_team("Phoenix FC O40")            
        
        full_names = [
                    'Mike Khavul',
                    'Jay Henke',
                    'Tim Gerke',
                    'Vlad Panof',
                    'David Marmor',
                    'Joe Romaker',
                    'Nate Foster',
                    'Mike Driggs',
                    'Don Mitchell',
                    'Dave King',
                    'Brian Shaffer',
                    'Quinn Kuranz',
                    'Shawn Dimke',
                    'Jeremy Kern',
                    'Brian Karasti',
                    'David Pugh',
                    'Robert Delgado',
                    'Gary Ploski',
                    'Vaidas Zievys',
                    'Elon Kaiserman',
                    'Paul Leslie',
                    'Helen Philpot'
                ]


        over40_team_id = over40_team.id

        # Create the player data list
        players_data = []

        for full_name in full_names:
            first_name, last_name = full_name.split(' ')
            player = {
                'first_name': first_name,
                'last_name': last_name,
                'position': PositionType.midfielder,
                'team_id': over40_team_id,
            }
            players_data.append(player)
        
        for player_data in players_data:
            existing_player = PlayerService.get_player_by_full_name(player_data['first_name'], player_data['last_name'])

            if existing_player:
                # Player already exists, update their information if needed
                existing_player.position = player_data['position']
            else:
                # Player does not exist, create a new player
                player = Player(**player_data)
                db.session.add(player)
        
        db.session.commit()