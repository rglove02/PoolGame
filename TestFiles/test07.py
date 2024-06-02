import os;
import sys
sys.path.append('/root/cis2750/A4')
import Physics;

# delete any old database from last run
os.remove( 'phylib.db' );

# create new database with tables
db = Physics.Database();
db.createDB();
db.close();

# create game object
g = Physics.Game( gameName="G1", player1Name="P1", player2Name="P2" );

# look for correct attributes in the object
if g.gameName!="G1":
  print( "Invalid gameName" );


if g.player1Name!="P1":
  print( "Invalid player1Name" );


if g.player2Name!="P2":
  print( "Invalid player2Name" );

