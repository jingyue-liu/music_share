#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following uses the postgresql test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@<IP_OF_POSTGRE_SQL_SERVER>/postgres
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@<IP_OF_POSTGRE_SQL_SERVER>/postgres"
#
# Swap out the URI below with the URI for the database created in part 2
#DATABASEURI = "sqlite:///test.db"
DATABASEURI = "postgresql://jz2793:pvs9w@104.196.175.120/postgres"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


#
# START SQLITE SETUP CODE
#
# after these statements run, you should see a file test.db in your webserver/ directory
# this is a sqlite database that you can query like psql typing in the shell command line:
# 
#     sqlite3 test.db
#
# The following sqlite3 commands may be useful:
# 
#     .tables               -- will list the tables in the database
#     .schema <tablename>   -- print CREATE TABLE statement for table
# 
# The setup code should be deleted once you switch to using the Part 2 postgresql database
#
engine.execute("""DROP TABLE IF EXISTS test;""")
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper');""")
engine.execute("""INSERT INTO test(name) VALUES ('alan turing');""")
engine.execute("""INSERT INTO test(name) VALUES ('ada lovelace');""")
#
# END SQLITE SETUP CODE
#
####### this is for LoggedInUserID   ########
LoggedInUserID = -1

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  global LoggedInUserID
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args


  #########################
  # example of a database query
  #
  #cursor = g.conn.execute("SELECT *")
  #names = []
  #for result in cursor:
  #  names.append(result['name'])  # can also be accessed using result[0]
  #cursor.close()
  ############################
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


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  if LoggedInUserID==-1:
    return render_template("index.html")
  else:
    return redirect('/logged_home')

#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#


@app.route('/logged_home')
def logged_home():
  global LoggedInUserID
  print request.args

  cursor = g.conn.execute("SELECT Name FROM Users WHERE AccountID=%s",(LoggedInUserID,))

  for result in cursor:
    Name=result[0]  # can also be accessed using result[0]
  cursor.close()

  context = dict(NameData = Name)

  return render_template("Logged_home.html",**context)
  
@app.route('/albums')
def albums():
  print request.args

  cursor = g.conn.execute('''
  SELECT AL.AlbumID,AL.Name,AL.Hit_song,AR.Name 
  FROM Albums_Create AL,Artists AR
  WHERE AL.ArtistID=AR.ArtistID
  ''')
  names = []
  for result in cursor:
    names.append([result[0],result[1],result[2],result[3]])
  cursor.close()

  context = dict(data = names)

  return render_template("Albums.html",**context)
  
@app.route('/album_records',methods=['POST'])
def album_records():
  print request.args
  Id = request.form['id']
  cursor = g.conn.execute('''
  SELECT r.RecordID,r.Name,r.Language,r.ReleaseYear,(r.Length/60000-0.5)::int::text||'min'::text||((r.Length-(r.Length/60000-0.5)::int*60000)/1000-0.5)::int::text||'s',r.Style,r.Songwriter
  FROM Records as r,Have as h
  WHERE r.RecordID = h.RecordID and h.AlbumID=%s
  ''',(int(Id),))
  names = []
  for result in cursor:
    names.append([result[0],result[1],result[2],result[3],result[4],result[5],result[6]])  # can also be accessed using result[0]
  cursor.close()
  
  cursor1 = g.conn.execute('''
  SELECT Name
  FROM Albums_Create
  WHERE AlbumID=%s
  ''',(int(Id),))
  AlbumName = ''
  for result in cursor1:
    AlbumName = result[0]
  cursor1.close()

  context = dict(data = names, albumname= AlbumName)
  return render_template("/Album_records.html",**context) 
  
@app.route('/artists')
def artists():
  print request.args

  cursor = g.conn.execute('''
  SELECT ArtistID,Name 
  FROM Artists
  ''')
  names = []
  indexs = []
  for result in cursor:
    names.append([result[0],result[1]])  # can also be accessed using result[0]
  cursor.close()

  context = dict(data = names)
  return render_template("Artists.html",**context)
  
@app.route('/artists_album',methods=['POST'])
def artists_album():
  print request.args
  Id = request.form['id']
  cursor = g.conn.execute('''
  SELECT AL.AlbumID,AL.Name
  FROM Albums_Create as AL
  WHERE AL.ArtistID = %s
  ''',(int(Id),))
  names = []
  for result in cursor:
    names.append([result[0],result[1]])  # can also be accessed using result[0]
  cursor.close()

  cursor1 = g.conn.execute('''
  SELECT ar.Name
  FROM Artists ar
  WHERE ar.ArtistID = %s
  ''',(int(Id),))
  ArtistName=''
  for result in cursor1:
    ArtistName=result[0]
  cursor1.close()  
  
  cursor2 = g.conn.execute('''
  SELECT ar.Name,s.Gender,s.Nationality,s.Birthdate
  FROM Artists ar LEFT OUTER JOIN Singers s ON ar.ArtistID=s.ArtistID
  WHERE ar.ArtistID = %s
  ''',(int(Id),))
  artistInfo = []
  for result in cursor2:
    artistInfo.append([result[0],result[1],result[2],result[3]])  # can also be accessed using result[0]
  cursor2.close()
  
  context = dict(data = names,artistname=ArtistName,artistinfo=artistInfo)
  return render_template("Artists_album.html",**context)  
  
@app.route('/records')
def records():
  print request.args

  cursor = g.conn.execute("SELECT RecordID,Name FROM Records")
  names = []
  for result in cursor:
    names.append([result[0],result[1]])  # can also be accessed using result[0]
  cursor.close()

  context = dict(data = names)
  return render_template("Records.html",**context)
  

@app.route('/one_record',methods=['POST'])
def one_record():
  global LoggedInUserID
  print request.args
  Id = request.form['id']
  
  cursor0 = g.conn.execute('''
  SELECT r.Name
  FROM Records as r
  WHERE r.RecordID = %s
  ''',(int(Id),))
  Rname = ''
  for result in cursor0:
    Rname=result[0]
  cursor0.close()
  
  cursor = g.conn.execute('''
  SELECT r.RecordID,r.Name,r.Language,r.ReleaseYear,(r.Length/60000-0.5)::int::text||'min'::text||((r.Length-(r.Length/60000-0.5)::int*60000)/1000-0.5)::int::text||'s',r.Style,r.Songwriter
  FROM Records as r
  WHERE r.RecordID = %s
  ''',(int(Id),))
  names = []
  for result in cursor:
    names.append([result[0],result[1],result[2],result[3],result[4],result[5],result[6]])  # can also be accessed using result[0]
  cursor.close()
  cursor1 = g.conn.execute('''
  SELECT u.Name, rev.rate, rev.Comment
  FROM Review_Write_About as rev,Users as u
  WHERE rev.RecordID = %s and rev.AccountID=u.AccountID
  ''',(int(Id),))
  reviews=[]
  for result in cursor1 :
    reviews.append([result[0],result[1],result[2]])
  cursor1.close()
  
  cursor2 = g.conn.execute('''
  SELECT p.Name
  FROM PersonalLists_Save p,Users u
  WHERE p.AccountID=u.AccountID and p.AccountID=%s
  ''',(LoggedInUserID,))
  mylists=[]
  for result in cursor2 :
    mylists.append(result[0])
  cursor2.close()
  
  context = dict(data = names,review =reviews,logined=LoggedInUserID,rname=Rname,rID=int(Id),Mylists=mylists)
  print context
  return render_template("/one_record.html",**context)  
  
@app.route('/add_to_mylist', methods=['POST'])
def add_to_mylist():
  global LoggedInUserID
  if LoggedInUserID==-1:
    return redirect('/')
  mylistname = request.form["MyListName"]
  rId = int(request.form["RID"])
  
  cursor = g.conn.execute('''
  SELECT P.PersonalListID FROM PersonalLists_Save P WHERE P.Name=%s and P.AccountID=%s
  ''',(mylistname,LoggedInUserID))
  PersonalListID=int(cursor.fetchone()[0])
  cursor.close()
  
  cursor1 = g.conn.execute('''
  INSERT INTO Contain (PersonalListID,AccountID,RecordID) VALUES (%s,%s,%s)
  ''',(PersonalListID,LoggedInUserID,rId))
  cursor1.close()
  return redirect("/myshare")

@app.route('/add_review', methods=['POST'])
def add_review():
  global LoggedInUserID
  if LoggedInUserID==-1:
    return redirect('/')
  cursor1 = g.conn.execute('''
  SELECT MAX(re.ReviewID) 
  FROM Review_Write_About as re
  WHERE re.AccountID=%s
  ''',(LoggedInUserID,))
  ReviewID=1
  for result in cursor1 :
    if result[0]!=None:
      ReviewID=int(result[0])+1
  cursor1.close()
  print ReviewID
  Index = request.form['Index']
  Rate = request.form['Rate']
  Comment = request.form['Comment']
  print Index,Rate,Comment
  g.conn.execute('''
  INSERT INTO  Review_Write_About (ReviewID,Rate,Comment,AccountID,RecordID) VALUES (%s,%s,%s,%s,%s)
  ''',(int(ReviewID),int(Rate),str(Comment),LoggedInUserID,Index));
  return "Thanks for your valuable review~\n\nNow you can either go back and refresh the record information or go to Myshare to check your own review! Also don't foget to check all the reviews written by all the users in the Review page~"

@app.route('/deleteOneReview', methods=['POST'])
def deleteOneReview():
  print request.args
  reviewID = request.form['reviewId']
  cursor = g.conn.execute('''
  DELETE FROM Review_Write_About WHERE ReviewID = %s
  ''',(int(reviewID),))
  cursor.close()

  return redirect("/myshare")  
  
@app.route('/reviews')
def reviews():
  print request.args

  cursor = g.conn.execute('''
  SELECT r.Name, u.Name, rev.rate, rev.Comment 
  FROM Review_Write_About as rev,Users as u,Records as r
  WHERE u.AccountID=rev.AccountID and rev.RecordID=r.RecordID
  ''')
  names = []
  for result in cursor:
    names.append([result[0],result[1],result[2],result[3]])  # can also be accessed using result[0]
  cursor.close()

  context = dict(data = names)
  return render_template("Reviews.html",**context)
  
@app.route('/users')
def users():
  print request.args

  cursor = g.conn.execute("SELECT AccountID,Name,Gender FROM Users")
  names = []
  for result in cursor:
    names.append([result[0],result[1],result[2]]) 
  cursor.close()

  context = dict(data = names)
  return render_template("Users.html",**context)
  
@app.route('/toplist')
def toplist():
  print request.args

  cursor = g.conn.execute('''
  select a2.rank,a2.name as Record,a1.name as Artist, a2.recordid
  from
  (select p.recordid, a.name 
  from perform p join artists a 
  on p.artistid=a.artistid) AS a1,
  (select r.recordid,r.name,i.rank
  from include i,toplists t,records r 
  where r.recordid=i.recordid and i.toplistid=t.toplistid) AS a2
  where a1.recordid=a2.recordid
  Order By a2.rank;
  ''')
  names = []
  for result in cursor:
    names.append([result[0],result[1],result[2],result[3]])  # can also be accessed using result[0]
  cursor.close()

  context = dict(data = names)
  return render_template("Toplists.html",**context)
  

@app.route('/myshare')
def myshare():
  global LoggedInUserID
  print request.args
  UID = LoggedInUserID
  #personallists
  cursor = g.conn.execute('''
  SELECT P.PersonalListID,P.Name,R.RecordID,R.Name
  FROM PersonalLists_Save as P,Users as U,Contain as C,Records as R
  WHERE U.AccountID = P.AccountID and U.AccountID=%s and C.PersonalListID=P.PersonalListID and C.AccountID=U.AccountID and C.RecordID=R.RecordID
  ORDER BY P.PersonalListID
  ''',(UID,))
  names = []
  for result in cursor:
    names.append([result[0],result[1],result[2],result[3]]) 
  cursor.close()
  #reviews
  cursor1 = g.conn.execute('''
  SELECT rev.ReviewID,r.Name, u.Name, rev.rate, rev.Comment 
  FROM Review_Write_About as rev,Users as u,Records as r
  WHERE u.AccountID=%s and u.AccountID=rev.AccountID and rev.RecordID=r.RecordID
  ''',(UID,))
  names1 = []
  for result in cursor1:
    names1.append([result[0],result[1],result[2],result[3],result[4]]) 
  cursor1.close()
  print names1
  context = dict(data = names,data1=names1)
  return render_template("/Myshare.html",**context) 
  
@app.route('/oneshare',methods=['POST'])
def oneshare():
  print request.args
  UID = request.form['UserID']
  #personallists
  cursor = g.conn.execute('''
  SELECT P.PersonalListID,P.Name,R.RecordID,R.Name
  FROM PersonalLists_Save as P,Users as U,Contain as C,Records as R
  WHERE U.AccountID = P.AccountID and U.AccountID=%s and C.PersonalListID=P.PersonalListID and C.AccountID=U.AccountID and C.RecordID=R.RecordID
  ORDER BY P.PersonalListID
  ''',(UID,))
  names = []
  for result in cursor:
    names.append([result[0],result[1],result[2],result[3]]) 
  cursor.close()
  #reviews
  cursor1 = g.conn.execute('''
  SELECT r.Name, u.Name, rev.rate, rev.Comment 
  FROM Review_Write_About as rev,Users as u,Records as r
  WHERE u.AccountID=%s and u.AccountID=rev.AccountID and rev.RecordID=r.RecordID
  ''',(UID,))
  names1 = []
  for result in cursor1:
    names1.append([result[0],result[1],result[2],result[3]]) 
  cursor1.close()
  print names1
  context = dict(data = names,data1=names1)
  return render_template("/Oneshare.html",**context) 

@app.route('/test')
def test():
  print request.args

  cursor = g.conn.execute("SELECT * FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()

  context = dict(data = names)
  return render_template("test.html",**context)

# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  print name
  cmd = 'INSERT INTO test(name) VALUES (:name1)';
  g.conn.execute(text(cmd), name1 = name);
  return redirect('/test')
  
@app.route('/test_extend', methods=['POST'])
def test_extend():
  Id = request.form['id']
  print Id
  cursor = g.conn.execute("SELECT * FROM test where id=%s",(str(Id),))
  names = []
  for result in cursor:
    names.append([result[0],result[1]])  # can also be accessed using result[0]
  cursor.close()
  
  context = dict(data = names)
  return render_template("test_extend.html",**context)

@app.route('/login', methods=['POST'])
def login():
	global LoggedInUserID
	UserID = request.form['UserID']
	Password = request.form['Password']
	print "ID:"+str(UserID)+"--","Password:"+str(Password)
	#eg: 1,fhgjhu
	cursor = g.conn.execute('''
	SELECT Password
	FROM Users
	WHERE AccountID = %s
	''',(UserID,))
	for result in cursor:
	  if Password == result[0]:
	    LoggedInUserID = int(UserID)
	return redirect('/')
	
@app.route('/logoff', methods=['POST'])
def logoff():
	global LoggedInUserID
	LoggedInUserID = -1
	return redirect('/')

@app.route('/signup', methods=['POST'])
def signup():
	Name = request.form['Name']
	Password = request.form['Password']
	cursor = g.conn.execute('''SELECT MAX(AccountID) FROM Users''')
	for result in cursor:
		UserID = result[0]+1
	cursor.close()
	g.conn.execute('''
	INSERT INTO Users (AccountID, Name, Password) VALUES (%s,%s,%s)
	''',(int(UserID),str(Name),str(Password)))
	return 'Thanks for signing up~\n\nYour UserID is: ' + str(UserID) + '.\n\nNow you can go to homepage and login~' + render_template("test.html")
	

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
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
