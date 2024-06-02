import sys
sys.path.append('/root/cis2750/A4')
import Physics;


def comp( item, val ):
  if abs( eval(item) - val ) > 0.02:
    print( item, "(", eval(item), ") != ", val );
   
# delete old database
os.remove( 'phylib.db' );

# create table
table = Physics.Table();

# create 1 ball
pos = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0,
                Physics.TABLE_WIDTH / 2.0,
                );

sb = Physics.StillBall( 1, pos );

# add ball to table
table += sb;

# create database and tables
db = Physics.Database();
db.createDB();

# write table to db
db.writeTable( table );

# close DB
db.close();

# re-open db
db = Physics.Database();

# recover the table
table = db.readTable( 0 );

# look for the StillBall on the table
if table[10].__class__ != Physics.StillBall:
    print( "StillBall not found in database file." );
