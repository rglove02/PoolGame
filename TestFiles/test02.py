import sqlite3;
import sys
sys.path.append('/root/cis2750/A4')
import Physics;


db = Physics.Database(True);  # create fresh database
db.createDB();                # add tables
del( db );

# connect to the database
conn = sqlite3.connect( 'phylib.db' );
cur = conn.cursor();

# retreive master table list and retreive SQL code used to create each table
tables = cur.execute( """SELECT sql FROM sqlite_master WHERE type='table';""" );
tables = [ uniple[0] for uniple in tables.fetchall() ];

table_names = [ 'Ball', 'TTable', 'BallTable', 'Shot', 'TableShot', 'Game', 'Player' ];

# make sure all of the above tables are in the database
try:
  d = { tn: [ table for table in tables if tn in table ][0].upper() for tn in table_names };
except Exception:
  print( "Could not find all required tables\n" );

# look for these keywords in the sql commands that created the tables
test_pairs = [ ('AUTOINCREMENT', 'Ball'),
               ('NOT NULL', 'TTable' ),
               ('FOREIGN KEY', 'BallTable'),
               ('PRIMARY KEY', 'Shot'),
               ('FOREIGN KEY', 'TableShot' ),
               ('AUTOINCREMENT', 'Game' ),
               ('NOT NULL', 'Player' ) ];

for term, table in test_pairs:
  for word in term.split():
    if not word in d[table]:
      print( "No %s in %s" % (term,table) );
