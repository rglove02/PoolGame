import os;
import sys
sys.path.append('/root/cis2750/A4')
import Physics;


fp = open( "phylib.db", "w" );
fp.write( "bad db" );
fp.close();

db = Physics.Database(True);  # open database with delete option

if not os.path.exists( "phylib.db" ):  # check if there is a database
    print( "phylib.db not found\n" );


if not os.stat( "phylib.db" ).st_size == 0: # check if it is empty
    print( "phylib.db is not valid database (did you delete old file?)\n" );
   