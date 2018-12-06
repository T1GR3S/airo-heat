import sqlite3
import sys

if len(sys.argv) > 1:
    if sys.argv[1] == "-h" or sys.argv[1] =="--help":
        print ('''
        Usage: databaseWigle.py <inputDB> <outputDB>
        \t inputDB: Database de entrada SQLite3 (Wigle)
        \t outputDB: Database de salida SQLite3
        ''')
        sys.exit(0) 

if len(sys.argv) < 3:
    print ('databaseWigle.py <inputDB> <outputDB>')
    sys.exit(2)

output_db = sqlite3.connect(sys.argv[2])
output_db.text_factory = str

cursor = output_db.cursor()

try:

    #TABLES CREATION
    #Table AP
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AP
        (
        bssid TEXT NOT NULL,
        ssid TEXT,
        manuf TEXT,
        channel int,
        frequency TEXT,
        carrier TEXT,
        encryption TEXT,
        packetsTotal int,
        lat_t REAL,
        lon_t REAL,
        CONSTRAINT Key1 PRIMARY KEY (bssid)
        );
    ''')

    #Table SeenAp
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SeenAp
        (
        bssid TEXT NOT NULL,
        time datetime NOT NULL,
        tool TEXT,
        signal_rssi int,        
        lat REAL,
        lon REAL,
        alt REAL,
        bsstimestamp timestamp,
        CONSTRAINT Key3 PRIMARY KEY (time,bssid),
        CONSTRAINT SeenAp FOREIGN KEY (bssid) REFERENCES AP (bssid)
        );
    ''')

    #Table Client
    cursor.execute('''
	    CREATE TABLE IF NOT EXISTS Client
        (   
        mac TEXT NOT NULL,
        ssid TEXT,
        manuf TEXT,
        type TEXT,
        packetsTotal int,
        device TEXT,
        CONSTRAINT Key1 PRIMARY KEY (mac)
        );
    ''')
    
    #Table SeenClient
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SeenClient
        (
        mac TEXT NOT NULL,
        time datetime NOT NULL,
        tool TEXT,
        signal_rssi int,
        lat REAL,
        lon REAL,
        alt REAL,
        CONSTRAINT Key3 PRIMARY KEY (time,mac),
        CONSTRAINT Seen FOREIGN KEY (mac) REFERENCES Client (mac)
        );
    ''')

    #Table Connected
    cursor.execute('''
	    CREATE TABLE IF NOT EXISTS Connected
        (
        bssid TEXT NOT NULL,
        mac TEXT NOT NULL,
        CONSTRAINT Key4 PRIMARY KEY (bssid,mac),
        CONSTRAINT Relationship2 FOREIGN KEY (bssid) REFERENCES AP (bssid),
        CONSTRAINT Relationship3 FOREIGN KEY (mac) REFERENCES Client (mac)
        );
	''')

    #Table Probe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Probe
        (
        mac TEXT NOT NULL,
        ssid TEXT NOT NULL,
        time datetime,
        CONSTRAINT Key5 PRIMARY KEY (mac,ssid),
        CONSTRAINT ProbesSent FOREIGN KEY (mac) REFERENCES Client (mac)
        );
	''')

    output_db.commit()    
except sqlite3.IntegrityError:
    print('Record already exists')


print(sqlite3.version)

#Attach inputDB
try:
    cursor.execute('ATTACH DATABASE "' + sys.argv[1] + '" as inputDB')
    
except sqlite3.Error:
    print('Error attaching inputDB')

#TABLES INSERTION
#Table AP
cursor.execute(''' 
    INSERT INTO AP 
    SELECT bssid, ssid, ' ' as manuf, ' ' as channel, frequency, ' ' as carrier, capabilities as encryption, ' ' as packetsTotal, ' ' as lat_t, ' ' as lon_t  
    FROM inputDB.network 
    WHERE type="W";
''')

#Table SeenAP
cursor. execute(''' INSERT INTO SeenAp
    WITH clean_location AS (
        SELECT * 
        FROM inputDB.location 
        WHERE (bssid, time) IN (
            SELECT bssid, time FROM inputDB.location GROUP BY bssid, time HAVING COUNT(*) = 1 
            )
    ) 
    SELECT bssid, time/1000, 'wigle' as tool, level as signal_rssi, lat, lon, altitude as alt, '' as bsstimestamp 
    FROM clean_location 
    WHERE time!= 0 AND bssid IN (
        SELECT bssid from inputDB.network where type="W"
    );
''')#time to seconds and time !=0

#Table Client
cursor.execute(''' INSERT INTO Client
    SELECT bssid as mac, ssid, ' ' as manuf, type, ' ' as packetsTotal, capabilities as device 
    FROM inputDB.network 
    WHERE type="B" OR type = "E";
''')

#Table SeenClient
cursor. execute(''' INSERT INTO SeenClient
    WITH clean_location AS (
        SELECT * 
        FROM inputDB.location 
        WHERE (bssid, time) IN (
            SELECT bssid, time FROM inputDB.location GROUP BY bssid, time HAVING COUNT(*) = 1 
            )
    ) 
    SELECT bssid as mac, time/1000, 'wigle' as tool, level as signal_rssi, lat, lon, altitude as alt 
    FROM clean_location 
    WHERE time!= 0 AND bssid IN (
        SELECT bssid from inputDB.network where type="B" OR type = "E"
    );
''') #time to seconds and time !=0
output_db.commit() 
output_db.close()

