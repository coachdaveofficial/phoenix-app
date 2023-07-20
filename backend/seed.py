from models import db, PositionType, Player
from services import TeamService


def seed_players():
    open_team = TeamService.get_team_by_name("Phoenix FC Open")
    
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
        player = Player(**player_data)
        db.session.add(player)

    db.session.commit()
