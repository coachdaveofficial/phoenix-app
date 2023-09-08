import os

from seed import seed_players, seed_o30, seed_o40
from script import SeasonDataExtractor
from models import connect_db, db, User
from flask import Flask, request, jsonify, session, g
from flask_debugtoolbar import DebugToolbarExtension
from services import PlayerService
from flask_cors import CORS, cross_origin

from blueprints.players.players import players_bp
from blueprints.teams.teams import teams_bp
from blueprints.matches.matches import matches_bp
from blueprints.auth.auth import auth_bp, CURR_USER_KEY

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
app.register_blueprint(players_bp, url_prefix='/api')
app.register_blueprint(teams_bp, url_prefix='/api')
app.register_blueprint(matches_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/')



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
db.drop_all()
db.create_all()

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
        # g.user = db.session(User).get(session[CURR_USER_KEY])

    else:
        g.user = None

    print(g.user)

extractor = SeasonDataExtractor("phoenix-fc-sheets-COPY.json", "Copy of Phoenix Historical Stats")




seed_o30()
seed_players()
seed_o40()

extractor.insert_data([{'worksheet': "Spring 2023 Open", "year": "2023", "season": "Spring", "team_type": "Open"}])
extractor.insert_data([{'worksheet': "Winter 2023 Open", "year": "2023", "season": "Winter", "team_type": "Open"}])
extractor.insert_data([{'worksheet': "Spring 2023 O30", "year": "2023", "season": "Spring", "team_type": "O30"}])
extractor.insert_data([{'worksheet': "Spring 2023 O40", "year": "2023", "season": "Spring", "team_type": "O40"}])
extractor.insert_data([{'worksheet': "Winter 2023 O40", "year": "2023", "season": "Winter", "team_type": "O40"}])


if __name__ == "__main__":
    app.run(debug=True, port=8080)