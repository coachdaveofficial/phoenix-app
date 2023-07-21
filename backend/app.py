import os

from seed import seed_players
from script import SeasonDataExtractor
from models import connect_db, db
from flask import Flask, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from services import PlayerService

from blueprints.players.players import players_bp

app = Flask(__name__)
app.register_blueprint(players_bp)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://', 1) or 'postgresql:///phoenix-app')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///phoenix-app'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

app.app_context().push()
connect_db(app)
# db.drop_all()
db.create_all()


extractor = SeasonDataExtractor("phoenix-fc-sheets-COPY.json", "Copy of Phoenix Historical Stats")







# extractor.insert_data([{'worksheet': "Spring 2023 Open", "year": "2023", "season": "Spring", "team_type": "Open"}])
# seed_players()

if __name__ == "__app__":
    app.run(debug=True)