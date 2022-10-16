import json
from flask import request
from flask import Flask, render_template

app = Flask(__name__)
import psycopg2

conn = psycopg2.connect("postgresql://theDucks:vJD1ufdJRASpMJypuopW7Q@free-tier11.gcp-us-east1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dkenthackenough-2373")

def insertScan(roomID, personID):
  stmt = """insert into Scan(scan_id = (
    select max(scan_id) from Scan) + 1, 
    time = NOW(),
    room_id = (select room_id from Room where room_id = """ + roomID + """),
    person_id = (select person_id from Person where person_id = """ + personID + """));"""

  return executeStmt(stmt);

def getPermission(personID):
  stmt = "select s.person_id, p.* from Person s, Permission p where s.perm_id = p.perm_id and s.person_id = " + personID + ";"
  
  return executeStmt(stmt)

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
  rooms = executeStmt("select * from room;")
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

if __name__ == "__main__":
  app.run(debug=True);
