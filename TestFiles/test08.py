import sys
sys.path.append('/root/cis2750/A4')
import Physics;

# create a game
g = Physics.Game( gameName="G1", player1Name="P1", player2Name="P2" );

# retrive gameID=0
g2 = Physics.Game( gameID=0 );

# look for correct attributes in g2
if g2.gameName!="G1":
  print( "Invalid gameName" );


if g2.player1Name!="P1":
  print( "Invalid player1Name" );


if g2.player2Name!="P2":
  print( "Invalid player2Name" );



