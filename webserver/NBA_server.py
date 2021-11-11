#!/usr/bin/env python

"""
Columbia's COMS W4111.003 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
import pandas as pd
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@35.196.73.133/proj1part2
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.152.219/proj1part2"
#
DATABASEURI = "postgresql://yh3290:0989@35.196.73.133/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
# #
# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def teams():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT name, Year_Founded, Head_Coach, State, City, Capacity, arena_name FROM team, arena \
    WHERE team.Arena_ID = arena.Arena_ID AND team.name != 'Free_Player'")
  Tnames = []
  Year_f = []
  Coach = []
  State = []
  City = []
  Capacity = []
  Arena_Name = []
  for result in cursor:
    Tnames.append(result[0])  # can also be accessed using result[0]
    Year_f.append(result[1])
    Coach.append(result[2])
    State.append(result[3])
    City.append(result[4])
    Capacity.append(result[5])
    Arena_Name.append(result[6])

  # names = pd.DataFrame(names, columns=['Team_ID', 'Tname', 'Year_Founded','Head_Coach','Arena_ID'])
  cursor.close()

  cursor_player = g.conn.execute("SELECT first_name, last_name, date_birth FROM player WHERE first_name IS NOT NULL\
    AND last_name IS NOT NULL")
  pname = []
  for result in cursor_player:
    pname.append(result[0]+' '+result[1])  # can also be accessed using result[0]

  # names = pd.DataFrame(names, columns=['Team_ID', 'Tname', 'Year_Founded','Head_Coach','Arena_ID'])
  cursor_player.close()
  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(Tnames = Tnames, Year_f = Year_f, Coach = Coach, \
    State = State, City = City, Capacity = Capacity, Arena_Name = Arena_Name, pname = pname)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("NBA.html", **context)

@app.route('/team')
def team_info():
  tname = request.args.get('tname')
  team_info_cursor = g.conn.execute(text("SELECT * FROM team T, arena A WHERE T.Arena_ID = A.Arena_ID AND name = :tname"), {"tname": tname})
  one_player_cursor = g.conn.execute(text("SELECT * FROM team T, Player P WHERE T.team_ID = P.team_ID AND name = :tname ORDER BY career_pts DESC NULLS LAST"), {"tname": tname})
  tid = 0
  tname = ''
  year_founded = 0
  head_coach = ''
  aid = ''
  state = ''
  city = ''
  capacity = 0
  aname = ''
  for result in team_info_cursor:
    tid = result[0]
    tname = result[1]
    year_founded = result[2]
    head_coach = result[3]
    aid = result[4]
    state = result[6]
    city = result[7]
    capacity = result[8]
    aname = result[9]
  team_info_cursor.close()

  one_player = []
  for result in one_player_cursor:
    one_player.append([result[6], result[7], result[11], result[12], result[14], result[17]])
  team_info = dict(tid = tid, tname = tname, year_founded = year_founded, head_coach = head_coach,\
    aid = aid, state = state, city = city, capacity = capacity, aname = aname, one_player = one_player)
  return render_template("team.html", **team_info)


#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#

@app.route('/game_details')
def game_info():
  gid = request.args.get('gid')
  one_player_cursor = g.conn.execute(text("SELECT Pr.first_name, Pr.last_name, MIN, PTS, AST, REB, Pr.Team_ID FROM game G, Plays Ps, Player Pr \
    WHERE G.Game_ID = Ps.Game_ID AND Pr.Player_ID = Ps.Player_ID AND G.game_id = :gid ORDER BY PTS DESC NULLS LAST"), {"gid": gid})
  game_cursor = g.conn.execute(text("SELECT Game_ID, T1.name as hteam, T2.name as ateam, home_team_score, \
                                        away_team_score, year, T1.team_ID, T2.team_ID FROM Game G, team T1, team T2  \
                                        WHERE G.home_team_ID = T1.team_ID and G.away_team_ID = T2.team_ID AND G.game_ID = :gid"),\
                                    {"gid": gid})
  one_player = []
  for result in one_player_cursor:
    one_player.append([result[0], result[1], result[2], result[3], result[4], result[5], result[6]]) # gid, hteam, ateam, hscore, ascore, year
  one_player_cursor.close()
  
  one_game = []
  for result in game_cursor:
    one_game = [result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7]]
  game_cursor.close()
  info = dict(one_player = one_player, one_game = one_game)
  return render_template("game_details.html", **info)

@app.route('/player', methods = ['GET'])
def player():
  return render_template("player.html")

@app.route('/player', methods = ['POST'])
def player_profile():
  last_name = request.form['lname']
  if last_name != '':
    if last_name[0].islower():
      last_name = last_name[0].upper() + last_name[1:].lower()
  first_name = request.form['fname']
  if first_name != '':
    if first_name[0].islower():
      first_name = first_name[0].upper() + first_name[1:].lower()
  cursor_player = g.conn.execute(text("SELECT * FROM player WHERE last_name = :lname and first_name = :fname"),\
    {"lname":last_name, "fname":first_name})
  cursor_player_avg = g.conn.execute(text("SELECT AVG(height), AVG(weight), AVG(CAREER_PTS), AVG(CAREER_AST), AVG(CAREER_REB) FROM Player"))
  cursor_player_max = g.conn.execute(text("SELECT MAX(height), MAX(weight), MAX(CAREER_PTS), MAX(CAREER_AST), MAX(CAREER_REB) FROM Player"))
  player_fname = ''
  player_lname = ''
  player_dob = ''
  player_height = ''
  player_weight = ''
  player_jersey = ''
  player_pos = ''
  player_pts = ''
  player_ast = ''
  player_reb = ''
  player_star = ''
  for result in cursor_player:
      player_fname = str(result[1])
      player_lname = str(result[2])
      player_dob=result[3]
      player_height=result[4]
      player_weight=result[5]
      player_jersey=result[6]
      player_pos=str(result[7])
      player_pts=result[9]
      player_ast=result[10]
      player_reb=result[11]
      player_star=result[12]
  cursor_player.close()
  for result in cursor_player_avg:
    avg_height = float(result[0])
    avg_weight = float(result[1])
    avg_pts = float(result[2])
    avg_ast = float(result[3])
    avg_reb = float(result[4])
  cursor_player_avg.close()
  for result in cursor_player_max:
    max_height = float(result[0])
    max_weight = float(result[1])
    max_pts = float(result[2])
    max_ast = float(result[3])
    max_reb = float(result[4])
  cursor_player_max.close()
  player_profile = dict(player_fname = player_fname,player_lname = player_lname, player_dob = player_dob, player_height = player_height, player_weight = player_weight,\
    player_jersey = player_jersey, player_pos = player_pos, player_pts = player_pts, player_ast = player_ast,\
      player_reb = player_reb,player_star = player_star, avg_height=avg_height, avg_weight=avg_weight, avg_pts=avg_pts, avg_ast = avg_ast, avg_reb = avg_reb,\
        max_height = max_height, max_weight= max_weight, max_pts=max_pts, max_ast=max_ast, max_reb= max_reb, query = True)
  return render_template("player.html", **player_profile)

@app.route('/game', methods = ['GET'])
def game():
  return render_template("game.html")

@app.route('/game', methods = ['POST'])
def game_profile():
  year = request.form['year']
  hteam = request.form['hteam']
  ateam = request.form['ateam']
  trick = False
  if year == '' or hteam == '' or ateam == '':
    trick = True
    game_profile = dict(trick = trick)
    return render_template("game.html", **game_profile)
  cursor_game = g.conn.execute(text("SELECT Game_ID, Home_Team_Win, year, T1.name as hteam, T2.name as ateam, home_team_score, \
                                        away_team_score FROM Game G, team T1, team T2  \
                                        WHERE G.home_team_ID = T1.team_ID and G.away_team_ID = T2.team_ID and T1.name = :hteam\
                                        and T2.name = :ateam and year = :year"),\
    {"year":year, "hteam":hteam, "ateam":ateam})
  one_game = []
  # Game_ID = []
  # winner = []
  # season = []
  # hteam = []
  # ateam = []
  # home_team_score = []
  # away_team_score = []
  noReturn = False
  for result in cursor_game:
    Game_ID = result[0]
    hteam = result[3]
    ateam = result[4]
    if result[1]:
      winner = hteam
    else:
      winner = ateam
    season = result[2]
    home_team_score = result[5]
    away_team_score = result[6]
    one_game.append([Game_ID, season, hteam, ateam, winner, home_team_score, away_team_score])
  cursor_game.close()
  # print(one_game)
  if one_game == []:
    noReturn = True
  # game_profile = dict(Game_ID = Game_ID, winner = winner, season = season, hteam = hteam, ateam = ateam, home_team_score = home_team_score, away_team_score = away_team_score)
  game_profile = dict(one_game = one_game, query = True, noReturn = noReturn)
  return render_template("game.html", **game_profile)


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
