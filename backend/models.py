from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import enum

db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)

class PositionType(enum.Enum):
    goalkeeper = 1
    defender = 2
    midfielder = 3
    forward = 4





class Team(db.Model):
    """A Phoenix FC team"""

    __tablename__ = "teams"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    name = db.Column(
        db.Text,
        nullable=False
    )


class Season(db.Model):
    """A season of GPSD soccer"""

    __tablename__ = "seasons"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    name = db.Column(
        db.Text,
        nullable=False
    )
    start_date = db.Column(
        db.DateTime
    )
    end_date = db.Column(
        db.DateTime
    )

    @validates('start_date', 'end_date')
    def validate_dates(self, key, value):
        if key == 'start_date':
            if self.end_date and value >= self.end_date:
                raise ValueError("Start date must be before the end date.")
        elif key == 'end_date':
            if self.start_date and value <= self.start_date:
                raise ValueError("End date must be after the start date.")
        return value



class Goal(db.Model):

    __tablename__ = "goals"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    player_id = db.Column(
        db.Integer,
        db.ForeignKey('players.id')
    )
    match_id = db.Column(
        db.Integer,
        db.ForeignKey('matches.id')
    )


class Assist(db.Model):

    __tablename__ = "assists"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    player_id = db.Column(
        db.Integer,
        db.ForeignKey('players.id')
    )
    match_id = db.Column(
        db.Integer,
        db.ForeignKey('matches.id')
    )
    for_goal_id = db.Column(
        db.Integer,
        db.ForeignKey("goals.id")
    )

    for_goal = db.relationship("Goal", backref='assisted_by')

class Appearance(db.Model):

    __tablename__ = "appearances"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    player_id = db.Column(
        db.Integer,
        db.ForeignKey('players.id')
    )
    season_id = db.Column(
        db.Integer,
        db.ForeignKey('seasons.id')
    )

class YellowCards(db.Model):
    """Yellow cards received by Phoenix FC players"""

    __tablename__ = "yellow_cards"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    player_id = db.Column(
        db.Integer,
        db.ForeignKey('players.id')
    )
    match_id = db.Column(
        db.Integer,
        db.ForeignKey('matches.id')
    )

class RedCards(db.Model):
    """Red cards received by Phoenix FC players"""

    __tablename__ = "red_cards"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    player_id = db.Column(
        db.Integer,
        db.ForeignKey('players.id')
    )
    match_id = db.Column(
        db.Integer,
        db.ForeignKey('matches.id')
    )

class Player(db.Model):
    """Player of Phoenix FC"""

    __tablename__ = "players"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    first_name = db.Column(
        db.Text,
        nullable=False
    )
    last_name = db.Column(
        db.Text,
        nullable=False
    )
    position = db.Column(
        db.Enum(PositionType)
    )
    team_id = db.Column(
        db.Integer,
        db.ForeignKey('teams.id'),
        nullable=False
    )

    team = db.relationship("Team", backref="players", foreign_keys=[team_id])
    apps = db.relationship("Appearance", backref="players")
    goals = db.relationship("Goal", backref="players")
    assists = db.relationship("Assist", backref="players")
    yellow_cards = db.relationship("YellowCards", backref="players")
    red_cards = db.relationship("RedCards", backref="players")

class Match(db.Model):
    """A match that is upcoming or previously played"""

    __tablename__ = "matches"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    date = db.Column(
        db.DateTime,
        nullable=False
    )
    venue = db.Column(
        db.Text,
        nullable=False
    )
    season_id = db.Column(
        db.Integer,
        db.ForeignKey('seasons.id'),
        nullable=False
    )
    home_team_id = db.Column(
        db.Integer,
        db.ForeignKey('teams.id'),
        nullable=False
    )
    away_team_id = db.Column(
        db.Integer,
        db.ForeignKey('teams.id'),
        nullable=False
    )

    home_team = db.relationship('Team', 
                                foreign_keys=[home_team_id], 
                                backref=db.backref('home_matches', lazy=True))
    away_team = db.relationship('Team', 
                                foreign_keys=[away_team_id], 
                                backref=db.backref('away_matches', lazy=True))
    season = db.relationship("Season", backref='matches')
    goals = db.relationship("Goal", backref="matches")
    assists = db.relationship("Assist", backref="matches")
    yellow_cards = db.relationship("YellowCards", backref="matches")
    red_cards = db.relationship("RedCards", backref="matches")    