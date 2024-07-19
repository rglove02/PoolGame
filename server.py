import os
import Physics
import sqlite3

from http.server import HTTPServer, BaseHTTPRequestHandler

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl

import sys # used to get argv
import cgi # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future

import json  # Import the json module
import random
import re

class MyHandler( BaseHTTPRequestHandler ):

  currentValue = 0
  game = None
  db = None
  player1Name = None
  player2Name = None
  table = None

  def do_GET(self):
    MyHandler.currentValue = 0

    #parse the URL to get the path and form data
    parsed  = urlparse( self.path )
    # or parsed.path in ['/pool.html']

    #check to see if it is requesting the shoot
    if parsed.path in ['/shoot.html'] or parsed.path in ['/pool.html']:

      #retreive the HTML file
      try: fp = open( '.'+self.path )
      except FileNotFoundError:
        #generate 404 for nonexistent file
        self.send_response( 404 )
        self.end_headers()
        self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )
        return
  
      content = fp.read()

      #sends header and footer
      self.send_response(200)
      self.send_header( "Content-type", "text/html" )
      self.send_header( "Content-length", len( content ) )
      self.end_headers()

      #send it to the broswer
      self.wfile.write( bytes( content, "utf-8" ) )
      fp.close()

    #checks to see if it ends with svg
    elif parsed.path.startswith("/table-") and parsed.path.endswith(".svg"):

      #retreive the file
      try: fp = open( '.'+self.path )
      except FileNotFoundError:
        #generate 404 for nonexistent file
        self.send_response( 404 )
        self.end_headers()
        self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )
        return
  
      content = fp.read()

      #sends header and footer
      self.send_response(200)
      self.send_header( "Content-type", "image/svg+xml" )
      self.send_header("Content-length", len(content)) 
      self.end_headers()

      #send it to the broswer
      self.wfile.write(bytes( content, "utf-8" ))
      fp.close()
      
    elif parsed.path in ['/script.js'] or parsed.path in ['/style.css']:

      #retrieve the file
      try: fp = open( '.'+self.path )
      except FileNotFoundError:
        #generate 404 for nonexistent file
        self.send_response( 404 )
        self.end_headers()
        self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )
        return
  
      content = fp.read()
      
      #generate the headers
      self.send_response( 200 ) # OK
      self.send_header( "Content-type", "" )
      self.send_header( "Content-length", len( content ) )
      self.end_headers()

      #send it to the broswer
      self.wfile.write( bytes( content, "utf-8" ) )
      fp.close()

    else:
        #generate 404 for GET requests that aren't the 3 files above
        self.send_response( 404 )
        self.end_headers()
        self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )

  #handle post request
  def do_POST(self):

    MyHandler.currentValue = 0

    #parse the URL to get the path
    parsed  = urlparse( self.path )

    if parsed.path in ['/sendNames']:

      content_length = int(self.headers['Content-Length'])
      post_data = self.rfile.read(content_length)

      try:
        data = json.loads(post_data.decode())

        MyHandler.gameName = data['game']
        MyHandler.player1Name = data['player1']
        MyHandler.player2Name = data['player2']

        print(f"Player 1: {MyHandler.player1Name}, Player 2: {MyHandler.player2Name}")

        game = Physics.Game(None, MyHandler.gameName, MyHandler.player1Name, MyHandler.player2Name)
        print("Game created")

        table = Physics.Table()
        print("Table initialized")
      
        # Add balls to the table with the 8 ball in the center
        table += Physics.StillBall(0, Physics.Coordinate(675, 2025))  # Cue ball (not part of the rack)
        table += Physics.StillBall(1, Physics.Coordinate(675, 675))  # Top of the triangle

        table += Physics.StillBall(2, Physics.Coordinate(740, 625))
        table += Physics.StillBall(3, Physics.Coordinate(610, 625))

        table += Physics.StillBall(4, Physics.Coordinate(800, 575))
        table += Physics.StillBall(8, Physics.Coordinate(675, 575)) # 8 ball in the center
        table += Physics.StillBall(5, Physics.Coordinate(550, 575))
        
        table += Physics.StillBall(6, Physics.Coordinate(860, 525))
        table += Physics.StillBall(7, Physics.Coordinate(740, 525))  
        table += Physics.StillBall(9, Physics.Coordinate(610, 525))
        table += Physics.StillBall(10, Physics.Coordinate(480, 525))

        table += Physics.StillBall(11, Physics.Coordinate(920, 475))
        table += Physics.StillBall(12, Physics.Coordinate(800, 475))
        table += Physics.StillBall(13, Physics.Coordinate(675, 475))  
        table += Physics.StillBall(14, Physics.Coordinate(550, 475))
        table += Physics.StillBall(15, Physics.Coordinate(425, 475))

        #add blls to table
        ballData = [
          (0, 675, 2025),  # Cue ball (not part of the rack)
          (1, 675, 675),  
          (2, 740, 625), (3, 610, 625),
          (4, 800, 575), (8, 675, 575), (5, 550, 575),
          (6, 860, 525), (7, 740, 525), (9, 610, 525), (10, 480, 525),
          (11, 920, 475), (12, 800, 475), (13, 675, 475), (14, 550, 475), (15, 425, 475)
        ]

        # #add balls to database
        # MyHandler.db = Physics.Database()
        
        # #open connection and set variable for cursor
        # MyHandler.db.conn = sqlite3.connect(self.db_file)
        # cur = MyHandler.db.conn.cursor()

        # #insert ball data into the database
        # for ball_no, xpos, ypos in ball_data:
        #   cur.execute("""INSERT INTO Ball (BALLNO, XPOS, YPOS) VALUES (?, ?, ?)""", (ball_no, xpos, ypos))

        # #Commit and close
        # conn.commit()
        # conn.close()

        #delete svg in current dir
        for file in os.listdir('.'):
          if file.endswith('.svg') and file.startswith('table'):
              os.remove(file)

        #opening the files
        while table is not None:
          # Pads with zero if i is less than 10
          filename = "table-{:03}.svg".format(MyHandler.currentValue)  
          with open(f"table-{MyHandler.currentValue}.svg", "w") as fp:

            # read the file that came in the form and write it to local dir
            fp.write(table.svg())
            table = table.segment()
            MyHandler.currentValue+=1

        #sort the files in current dir so they ar in right order
        files_list = []
        for file in os.listdir('.'):
          if file.endswith('.svg') and file.startswith('table'):
              files_list.append(file)

        #deal with the player names
        #open pool.html nd replace for the svg
        with open('pool.html', 'r') as file:
            content = file.read()

        #adds each svg image to the webpage
        for files in files_list:
          if files.endswith('.svg') and files.startswith('table'):
            content = content.replace('{{files}}', files)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))

      except json.JSONDecodeError:
        self.send_response(400)
        self.send_header("Content-type", "application/json")
        set_cors_headers(self)
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Invalid JSON data in the request!"}).encode())

    elif parsed.path in ['/process-shot']:

      content_length = int(self.headers['Content-Length'])
      post_data = self.rfile.read(content_length)

      #tatake out values rom form
      data = json.loads(post_data.decode('utf-8'))
      xvel = data['xvel']
      yvel = data['yvel']
      currentPlayer = data['current']

      # tableIDList = Physics.Game.shoot(MyHandler.gameName, currentPlayer, table, xvel, yvel )
      tableIDList = Physics.Game.shoot(MyHandler.gameName, currentPlayer, table, xvel, yvel )
      tableSVG = []
      for idNum in tableIDList:
        table = db.readTable(idNum)
        tableSVG.append(table.svg())

      self.send_response(200)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
      self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
        
      return tableSVG

    else:
      #send saying it did not work
      self.send_response( 404 )
      self.end_headers()
      self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )
      self.wfile.write("Ok")
    
if __name__ == "__main__":
  try:
    httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler)
    print("Server listening on port: ", int(sys.argv[1]))
    httpd.serve_forever()
  except Exception as e:
    print("Error:", e)