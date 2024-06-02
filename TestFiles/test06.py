import sys
sys.path.append('/root/cis2750/A4')
import Physics;


def comp( item, val ):
  if abs( eval(item) - val ) > 0.02:
    print( item, "(", eval(item), ") != ", val );

# remove DB
os.remove( 'phylib.db' );

# create table with 1 still ball and 1 rolling ball
table = Physics.Table();

# 1 ball
pos = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0,
                Physics.TABLE_WIDTH / 2.0,
                );

sb = Physics.StillBall( 1, pos );
table += sb;

# rolling ball
pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0,
                          Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
vel = Physics.Coordinate( 0.0, -1000.0 );
acc = Physics.Coordinate( 0.0, 150.0 );
rb  = Physics.RollingBall( 0, pos, vel, acc );

table += rb;

# create DB and tables
db = Physics.Database();
db.createDB();

# add table object to DB
db.writeTable( table );
db.close();

# re-open DB and retreive table
db = Physics.Database();
table = db.readTable( 0 );

# confirm Rolling Ball
if table[11].__class__ != Physics.RollingBall:
    print( "RollingBall not found in database file." );
