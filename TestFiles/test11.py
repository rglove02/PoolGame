import sys
sys.path.append('/root/cis2750/A4')
import Physics;

def comp( item, val ):
  if abs( eval(item) - val ) > 10.0:
    print( item, "(", eval(item), ") != ", val );


# open DB from test09.py
db = Physics.Database();

# load frame 100
t = db.readTable( 100 );

# check y-position of cue ball
comp( "t[13].obj.rolling_ball.pos.y", 1600.0 );


