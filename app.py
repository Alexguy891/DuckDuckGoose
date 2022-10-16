import json
from flask import request
from flask import Flask, render_template

app = Flask(__name__)
import psycopg2

conn = psycopg2.connect("postgresql://theDucks:vJD1ufdJRASpMJypuopW7Q@free-tier11.gcp-us-east1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dkenthackenough-2373")

def executeStmt(stmt):
  with conn.cursor() as cur:
    cur.execute(stmt)
    res = cur.fetchall()
    conn.commit()
  return res

@app.route('/')
def index():
  return render_template('./index.html')
@app.route('/rooms.html')
def room():
  rooms = executeStmt("select r.room_name, b.build_name from room r, building b;")
  jsonStr = json.dumps(rooms)
  return render_template('./rooms.html', rooms = jsonStr)
@app.route('/permissions.html')
def permissions():
  permissions = executeStmt("select * from permission")
  jsonStr = json.dumps(permissions)
  return render_template('./permissions.html', permissions = jsonStr)
@app.route('/students.html')
def students():
  persons = executeStmt("select * from person")
  jsonStr = json.dumps(persons)
  return render_template('./students.html', persons = jsonStr)
@app.route('/room_logs.html')
def room_logs():
  columnVal = request.args.get('columnVal', None)
  roomLogs = executeStmt("select r.room_name, p.firstname, p.lastname, p.email, s.time from scan s, room r, person p where r.room_name = '" + columnVal + "' and r.room_id = s.room_id and s.person_id = p.person_id");
  jsonStr = json.dumps(roomLogs, indent=4, sort_keys=True, default=str)
  return render_template('./room_logs.html', roomLogs = jsonStr)
@app.route('/person_logs.html')
def person_logs():
  columnVal = request.args.get('columnVal', None)
  personLogs = executeStmt("select p.person_id, p.firstname, p.lastname, p.email, s.* from scan s, person p where p.person_id = " + columnVal + " and p.person_id = s.person_id");
  jsonStr = json.dumps(personLogs, indent=4, sort_keys=True, default=str)
  return render_template('./person_logs.html', personLogs = jsonStr)

if __name__ == "__main__":
  app.run(debug=True);
