import sys
sys.path.append('/root/cis2750/A4')
import Physics;

def comp( item, val ):
  if abs( eval(item) - val ) > 10.0:
    print( item, "(", eval(item), ") != ", val );


# open DB from test09
db = Physics.Database();

# load frame 200
t = db.readTable( 200 );

# check y-position
comp( "t[13].obj.rolling_ball.pos.y", 1325.0 );


