from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
import sqlite3

conn = sqlite3.connect('speeding.db')
c = conn.cursor()

#DB Logic Class
#CRUD System
class DB():
    #Setting up Database
    def increment(self):
        c.execute("SELECT id FROM speeding ORDER BY id DESC LIMIT 1;")
        rows = c.fetchall()

        for row in rows:
            return row[0] + 1

    #Take in speed limit and speed
    def create(self, speed_limit, speed, isSpeeding):
        new_id = int(self.increment())
        c.execute("INSERT INTO speeding VALUES (" + str(new_id) + ", " +str(speed_limit)+", "+str(speed)+", "+str(isSpeeding)+")")
        #Push changes to DB
        conn.commit()

    def readall(self):
        result_obj = {}
        #{
            #1: {'speed_limit': 100, 'current_speed': 90, 'is_speeding': 0},
            #2: {'speed_limit': 90, 'current_speed': 91, 'is_speeding': 1}
        #}
        c.execute("SELECT * FROM speeding")
        rows = c.fetchall()

        for row in rows:
            result_obj[row[0]] = {'speed_limit': row[1],
                                  'current_speed': row[2],
                                  'is_speeding': row[3]}
        return result_obj

    #Search is the ID we want to find
    def readone(self, search):
        result_obj = {}
        c.execute("SELECT * from speeding WHERE ID = " + str(search))
        rows = c.fetchall()

        for row in rows:
            result_obj[row[0]] = {'speed_limit': row[1],
                                  'current_speed': row[2],
                                  'is_speeding': row[3]}
        return result_obj

    #Search is the ID we want to delete
    def delone(self, search):
        result_obj = {}
        try:
            c.execute("DELETE FROM speeding WHERE ID = " + str(search))
            conn.commit()
            return 'ID #' + str(search) + " Deleted!"
        except:
            return 'Failed while deleting.'

    def replace(self, search, speed_limit, speed, isSpeeding):
        try:
            c.execute("UPDATE speeding SET speed_limit="+str(speed_limit)+", current_speed= "+str(speed)+", is_speeding="+str(isSpeeding)+" WHERE ID = " + str(search))
            conn.commit()
            return 'ID #' + str(search) + " Updated!"
        except:
            return 'Failed while updating.'
        

#Create DB object
my_DB = DB()

#print(my_DB.delone(8))
#print(my_DB.readall())
print(my_DB.replace(9, 999, 1, 0))

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def handleNotFound(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not Found", "utf-8"))

    def getAllPrevious(self):
        try:
            data = my_DB.readall()
            self.send_response(201, data)

            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            
            return str(data)
        except:
            print("Failure.")

    def checkSpeed(self):
        # 1. read bytes from the request body
        length = self.headers['Content-Length']
        body = self.rfile.read(int(length)).decode("utf-8")
        print("request BODY:", body)

        # 2. parse the raw body into usable data
        parsed_body = parse_qs(body)
        print("parsed BODY:", parsed_body)

        # 3. grab the data and use it
        speed = int(parsed_body['speed'][0])
        speed_limit = int(parsed_body['limit'][0])

        #ACUTAL logic
        if(speed > speed_limit):
            print("Very bad!! Law breaker")
            my_DB.create(speed_limit, speed, 1)

        else:
            print("Not speeding")
            my_DB.create(speed_limit, speed, 0)

        # respond to the client
        self.send_response(201)

        self.send_header("Access-Control-Allow-Origin", "*")

        self.end_headers()

    def do_GET(self):
        print("the PATH is:", self.path)

        if self.path == "/previous":
            self.getAllPrevious()
        else:
            self.handleNotFound()

    #If the user is doing a speed check
    def do_POST(self):
        if self.path == "/speed":
            self.checkSpeed()
        else:
            self.handleNotFound()

#Main loop
def run():
  listen = ("127.0.0.1", 8080)
  #Listen using this class
  server = HTTPServer(listen, MyHTTPRequestHandler)

  print("Server ready! Listening...")
  server.serve_forever()

run()
