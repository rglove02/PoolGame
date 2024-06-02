import phylib;
import os;
import sqlite3;
import math;

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH; 
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;

# add more here
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";

#CONSTANT FOR a3
FRAME_INTERVAL = 0.01

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;

################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;

    # add an svg method here
    def svg(self):
        #add values for the string
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" id="ball%d"/>\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y,BALL_RADIUS,BALL_COLOURS[self.obj.still_ball.number],self.obj.still_ball.number)


################################################################################
class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number, position (x,y) velocity and acceleration as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;

    # add an svg method here
    def svg(self):
        
        #add values for the string
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" id="ball%d"/>\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y,BALL_RADIUS,BALL_COLOURS[self.obj.rolling_ball.number], self.obj.rolling_ball.number)

################################################################################
class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires hole position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a Hole class
        self.__class__ = Hole;

    # add an svg method here
    def svg(self):

        #add values for the string
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)

################################################################################
class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, y ):
        """
        Constructor function. Requires cushion y value as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y );
      
        # this converts the phylib_object into a HCushion class
        self.__class__ = HCushion;

    # add an svg method here
    def svg(self):
        #declare y variable
        y = self.obj.hcushion.y

        # check to see if appropriate values 
        if y == 0:
            y = -25
        #add values for the string
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (y)


################################################################################
class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, x ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0 );
      
        # this converts the phylib_object into a VCushion class
        self.__class__ = VCushion;

    # add an svg method here
    def svg(self):
        #declare x varaible
        x = self.obj.vcushion.x

         # check to see if appropriate values 
        if x == 0:
            x = -25
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (x)

################################################################################

class Table(phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        #add the header to the string
        content = HEADER

        #add the return values of each object of svg method to the string
        for obj in self:
            # makes sure that it is an object
            if obj is not None:
                try:
                    # adds the object to the string
                    content += obj.svg()
                except Exception as e:
                    print(f"Error in {obj.__class__.__name__}: {e}")

        # add the footer to the string
        content += FOOTER

        return content
    
    #A3 FUNC GIVEN
    def roll( self, t ):

        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );

                # add ball to table
                new += new_ball;

            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                        Coordinate( ball.obj.still_ball.pos.x,
                                        ball.obj.still_ball.pos.y ) );
                
                # add ball to table
                new += new_ball;
        
        # return table
        return new;

    def cueBall(self, table, xvel, yvel):

        #goes through table to find the ball
        for obj in table:

            #checks to see if it is a ball and it its number is 0
            if isinstance(obj, StillBall) and getattr(obj, 'type', None) == 0:
                ball = obj
                break

        #set type of cue.ball to phylib.ROLLING_BALL
        cuePos = ball.obj.still_ball.pos
        ball.obj.rolling_ball.type = phylib.ROLLING_BALL

        ball.obj.rolling_ball.number = 0
        ball.obj.rolling_ball.pos = cuePos

        ball.obj.rolling_ball.vel.x = xvel
        ball.obj.rolling_ball.vel.y = yvel

        #recalculate acc
        rbSpeed = math.sqrt(xvel * xvel + yvel * yvel)

        #check the speed to set acc
        if rbSpeed > VEL_EPSILON:
            xacc = ((xvel * -1.0) / rbSpeed) * DRAG
            yacc = ((yvel * -1.0) / rbSpeed) * DRAG

        #update acc for ball
        ball.obj.rolling_ball.acc.x = xacc
        ball.obj.rolling_ball.acc.y = yacc

        return ball


######################################################################################
#create database class
class Database():

    #initalizes class Database
    def __init__( self, reset=False ):
        self.db_file = "phylib.db"

        if reset and os.path.exists(self.db_file):
            os.remove(self.db_file)

        # create database file if it doesn't exist and connect to it
        conn = sqlite3.connect(self.db_file);

    #creates the tables if not already
    def createDB(self):

        #open connection and set variable for cursor
        self.conn = sqlite3.connect(self.db_file);
        cur = self.conn.cursor();

        cur.execute( """CREATE TABLE IF NOT EXISTS Ball (
                   BALLID     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                   BALLNO   INTEGER NOT NULL,
                   XPOS     FLOAT NOT NULL,
                   YPOS     FLOAT NOT NULL,
                   XVEL    FLOAT,
                   YVEL     FLOAT);""" );

        cur.execute( """CREATE TABLE IF NOT EXISTS TTable(
                        TABLEID     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        TIME        FLOAT NOT NULL);""" );

        cur.execute( """CREATE TABLE IF NOT EXISTS BallTable(
                        BALLID INTEGER NOT NULL,
                        TABLEID INTEGER NOT NULL,
                        FOREIGN KEY(BALLID) REFERENCES Ball,
                        FOREIGN KEY(TABLEID) REFERENCES TTable);""" );

        cur.execute( """CREATE TABLE IF NOT EXISTS Shot(
                        SHOTID       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        PLAYERID     INTEGER NOT NULL,
                        GAMEID       INTEGER NOT NULL,
                        FOREIGN KEY(PLAYERID) REFERENCES Player,
                        FOREIGN KEY(GAMEID) REFERENCES Game);""" );

        cur.execute( """CREATE TABLE IF NOT EXISTS TableShot(
                        TABLEID INTEGER NOT NULL,
                        SHOTID INTEGER NOT NULL,
                        FOREIGN KEY(TABLEID) REFERENCES TTable,
                        FOREIGN KEY(SHOTID) REFERENCES Shot);""" );

        cur.execute( """CREATE TABLE IF NOT EXISTS Game(
                        GAMEID       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        GAMENAME     VARCHAR(64) NOT NULL)""");

        cur.execute( """CREATE TABLE IF NOT EXISTS Player(
                        PLAYERID   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        GAMEID INTEGER NOT NULL,
                        PLAYERNAME     VARCHAR(64) NOT NULL,
                        FOREIGN KEY(GAMEID) REFERENCES Game(GAMEID))""" );
        
        #close cur and commit
        cur.close();
        self.conn.commit();

    #use to build the table class in Python to return it
    def readTable(self, tableID):

        #open connection and set variable for cursor
        self.conn = sqlite3.connect(self.db_file);
        cur = self.conn.cursor();
        
        #create table object to populate
        tableObj = Table()

        #get the time from TTable
        cur.execute("""SELECT TTable.TIME
                    FROM TTable
                    WHERE TTable.TABLEID = '{}'""".format(tableID +1))
    
        time = cur.fetchone()

        if time is None:
            cur.close()
            return None
        else:
            tableObj.time = time[0]

        # get all balls that have same tableid as  ttable
        # get all the balls w the ids fround in balltable
        # makes sure table idis right
        cur.execute("""SELECT * 
                    FROM Ball
                    JOIN BallTable ON Ball.BALLID  = BallTable.BALLID
                    JOIN TTable ON BallTable.TABLEID = TTable.TABLEID
                    WHERE TTable.TABLEID = '{}';""".format(tableID +1))

        ballInfo = cur.fetchall()

        #makes sure that there are balls in table obj with their id
        #If TABLEID does not exist in the BallTable table
        if len(ballInfo) <= 0:
            return None

        # #loop though and build ball object --> depending on what kind
        for i in range(0,len(ballInfo)):

            num = ballInfo[i][1]
            xpos = ballInfo[i][2]
            ypos = ballInfo[i][3]
            xvel = ballInfo[i][4]
            yvel = ballInfo[i][5]

            try:
                #check to see if have velocity
                if xvel is None and yvel is None:
                    
                    sbPos = Coordinate(float(xpos), float(ypos))
                    sb = StillBall(int(num), sbPos)

                    tableObj += sb

                else:
                    #calculate the acceleration
                    rbPos = Coordinate(xpos,ypos)
                    
                    # Handle None values for velocity
                    if xvel is None:
                        xvel = 0.0
                    if yvel is None:
                        yvel = 0.0

                    rbVel = Coordinate(float(xvel), float(yvel))
                    rbAcc = Coordinate(0.0,0.0)
                    rbSpeed = math.sqrt(xvel*xvel + yvel*yvel);

                    if (rbSpeed > VEL_EPSILON):
                        rbAcc.x = ((rbVel.x * -1.0) / rbSpeed) * DRAG
                        rbAcc.y = ((rbVel.y * -1.0) / rbSpeed) * DRAG

                    rb = RollingBall(int(num), rbPos, rbVel, rbAcc)

                    tableObj += rb

            except Exception as e:
                print(f"Error processing ball data at index {i}: {e}")
                continue

        #close cur and commit
        cur.close();
        self.conn.commit();

        return tableObj
        

    def writeTable(self, table):

        if table is None:
            return None

        #open connection and set variable for cursor
        self.conn = sqlite3.connect(self.db_file);
        cur = self.conn.cursor();

        #store table in TTable --> time and get table ID back
        cur.execute("""INSERT INTO TTable(TIME)
                     VALUES ('{}')""".format(float(table.time)))
        
        tableID = cur.lastrowid

        #loop
        for obj in table:

            #check class
            if isinstance(obj, StillBall):

                #store in BALL table
                cur.execute("""INSERT INTO Ball (BALLNO, XPOS, YPOS)
                            VALUES ('{}','{}','{}')""".format(obj.obj.still_ball.number, obj.obj.still_ball.pos.x, obj.obj.still_ball.pos.y))
                
            elif isinstance(obj, RollingBall):
                #store in BALL table
                cur.execute("""INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                            VALUES ('{}','{}','{}','{}','{}')""".format(obj.obj.rolling_ball.number, obj.obj.rolling_ball.pos.x, obj.obj.rolling_ball.pos.y, obj.obj.rolling_ball.vel.x, obj.obj.rolling_ball.vel.y))
            else:
                continue

            #get ball id
            ballID = cur.lastrowid

            #use ballid and tableid and stoRe in BALLTABLE
            cur.execute("""INSERT INTO BallTable (BALLID, TABLEID)
                        VALUES ('{}','{}')""".format(ballID,tableID))
            
        #close cur and commit
        cur.close();
        self.conn.commit();
        
        #return the autoincremented TABLEID value minus 1 
        return tableID-1
        
    #close and commit all connections
    def close(self):
       self.conn.commit();
       self.conn.close();

    def newShot(self,cur, playerName, gameName):

        #find playerid and gameid based on playerName
        self.cur.execute("""SELECT GAMEID
                        FROM Game
                        WHERE GAMENAME == '{}'""".format(gameName))

        gameID = self.cur.fetchone()

        self.cur.execute("""SELECT PLAYERID
                        FROM Player
                        WHERE PLAYERNAME == '{}' AND GAMEID == '{}'""".format(playerName, gameID))

        playerID = self.cur.fetchone()

        #input it in TableShot
        self.cur.execute("""INSERT INTO Shot (PLAYERID, GAMEID)
                            VALUES ('{}','{}')""".format(playerID, gameID))
       
        shotID = self.cur.lastrowid

        return shotID
    
    

########################################################################################
#create game class
class Game():
    gameID = 0
    gameName = '\0'
    player1Name = '\0'
    player2Name = '\0'

    def __init__( self, gameID=None, gameName=None, player1Name=None,
    player2Name=None ):
        self.conn = sqlite3.connect("phylib.db");
        self.cur = self.conn.cursor();

        #check to see if called right way
        if gameID != None and gameName == None and player1Name == None and player2Name == None:
            self.gameID = gameID + 1

            #retreive the values of gameName, player1Name, and player2Name
            self.getGame(self.gameID)
            self.conn.commit()

        elif gameID == None and isinstance(player1Name,str) and isinstance(player2Name,str):
            self.player1Name = player1Name;
            self.player2Name = player2Name;
            self.gameName = gameName;
            
            #add info to tables
            self.setGame()
            self.conn.commit()

        else:
            raise Exception(TypeError)
            
    def getGame(self,gameID):
        
       #retreive the values of gameName, player1Name, and player2Name from the Game and Player tables
       #Player 1 shall be the player with the lower PLAYERID
        self.cur.execute("""SELECT GAMENAME
                            FROM Game
                            WHERE GAMEID == '{}'""".format(gameID+1))
        
        name = self.cur.fetchone()
        self.gameName = name[0]

        #get the player names to put as parameters in order of the id
        self.cur.execute("""SELECT PLAYERNAME
                            FROM Player
                            WHERE GAMEID == '{}'
                            ORDER BY PLAYERID ASC""".format(gameID+1))
        
        playerName = self.cur.fetchall()

        self.player1Name = playerName[0][0]
        self.player2Name = playerName[1][0]

    def setGame(self):
        # row shall be added to the Game table and two new rows to the Player table to record the
        # gameName, the player1Name, and the player2Name. The player1Name shall be added to the
        # Player table first (so that it gets the lower PLAYERID)
        self.cur.execute("""INSERT INTO Game (GAMENAME)
                            VALUES ('{}')""".format(self.gameName))

        gameID = self.cur.lastrowid
        
        self.cur.execute("""INSERT INTO Player (GAMEID, PLAYERNAME)
                            VALUES ('{}','{}')""".format(gameID, self.player1Name))
        
        self.cur.execute("""INSERT INTO Player (GAMEID, PLAYERNAME)
                            VALUES ('{}','{}')""".format(gameID, self.player2Name))


    #add new entry to SHOT
    def shoot( self, gameName, playerName, table, xvel, yvel ):

        #get shotID and put info in SHOT table
        shotID = Database.newShot(self, self.cur, playerName, gameName)

        #find obj of cue ball that is in Table class
        cueBall = Table.cueBall(self, self.cur, shotID, xvel, yvel)

        #repeatedly call the segment method from A2 until it returns None. 
        table = Table.segment(self)
        while table is not None:

            #get before time, call segment and get after time
            beforeTime = table.time
            table = Table.segment(self)
            afterTime = table.time
            
            #determine the length of the segment (in seconds)
            #subtract the time at the beginning of the segment from the time at the end of the segment.
            #Divide by FRAME_INTERVAL and round it down to the nearest integer. 
            lengthSec = floor((beforeTime - afterTime)/FRAME_INTERVAL)

            # initialize newTable
            newTable = None 

            # loops over those integers
            for i in lengthSec:
                timeFrame = i * FRAME_INTERVAL
                newTable = phylib.phylib_roll(newTable, table, timeFrame)
                newTable.time = beforeTime + timeFrame

                #Save the table using writeTable
                Database.writeTable(newTable)

            table = newTable

    