import sys
sys.path.append('/root/cis2750/A4')
import Physics;


# comparison function to see if values are close
def comp( item, val ):
  if abs( eval(item) - val ) > 0.02:
    print( item, "(", eval(item), ") != ", val );



# Make sure you copy the example DB phylib.db to your working directory

db = Physics.Database();  # open prof's DB

# read the base table
table = db.readTable( 0 );

# look for the cue ball
comp( "table[13].obj.rolling_ball.number", 0 );
comp( "table[13].obj.rolling_ball.pos.x", 677.850 );
comp( "table[13].obj.rolling_ball.pos.y", 2025.0 );
comp( "table[13].obj.rolling_ball.vel.x", 0.0 );
comp( "table[13].obj.rolling_ball.vel.y", -1000.0 );
