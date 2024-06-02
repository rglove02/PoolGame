import sys
sys.path.append('/root/cis2750/A4')
import Physics;


def comp( item, val ):
  if abs( eval(item) - val ) > 0.02:
    print( item, "(", eval(item), ") != ", val );


# make sure to copy instructor's db

db = Physics.Database();

table = db.readTable( 4 );

comp( "table[13].obj.rolling_ball.number", 0 );
comp( "table[13].obj.rolling_ball.pos.x", 681.314 );
comp( "table[13].obj.rolling_ball.pos.y", 731.73 );
comp( "table[13].obj.rolling_ball.vel.x", 30.34 );
comp( "table[13].obj.rolling_ball.vel.y", 18.02 );

