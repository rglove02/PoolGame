import math;
import sys
sys.path.append('/root/cis2750/A4')
import Physics;

def comp( item, val ):
  if abs( eval(item) - val ) > 0.02:
    print( item, "(", eval(item), ") != ", val );



# create table with 4 balls - just like A3Test1.py

table = Physics.Table();

# 1 ball
pos = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0,
                Physics.TABLE_WIDTH / 2.0,
                );

sb = Physics.StillBall( 1, pos );
table += sb;

# 2 ball
pos = Physics.Coordinate(
                Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0,
                Physics.TABLE_WIDTH/2.0 -
                math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                );
sb = Physics.StillBall( 2, pos );
table += sb;

# 3 ball
pos = Physics.Coordinate(
                Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0,
                Physics.TABLE_WIDTH/2.0 -
                math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0),
                );
sb = Physics.StillBall( 3, pos );
table += sb;

# cue ball also still
pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0,
                          Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
sb  = Physics.StillBall( 0, pos );

table += sb;

# open and create fresh DB
db = Physics.Database( True );
db.createDB();
db.close();
del( db );

# create a game
game = Physics.Game( gameName="Game 01", player1Name="Stefan", player2Name="Efren Reyes" );

# take a shot - slower than in Test1
game.shoot( "Game 01", "Stefan", table, 0.0, -500.0 );

# open the DB
db = Physics.Database();
# read frame 0
t = db.readTable( 0 );
# check y position of rolling ball
comp( "t[13].obj.rolling_ball.pos.y", 2025.0 );

