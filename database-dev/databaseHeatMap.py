import xml.etree.ElementTree
import sqlite3
import sys

if len(sys.argv) > 1:
    if sys.argv[1] == "-h" or sys.argv[1] =="--help":
        print '''
        Usage: databaseHeatMap.py <outputDB> <inputKismet>
        \t outputDB: Database de salida SQLite3
        \t inputAP: Fichero de kismet con los ap  y gps (formato .gpsxml)
        '''
        sys.exit(0)


if len(sys.argv) < 3:
    print 'databaseHeatMap.py <outputDB> <inputKismet>'
    sys.exit(2)

db = sqlite3.connect(sys.argv[1])
# Get a cursor object
cursor = db.cursor()

try:
    cursor.execute('''

CREATE TABLE IF NOT EXISTS AP
(
  bssid TEXT NOT NULL,
  manuf TEXT,
  lat REAL,
  lon REAL,
  CONSTRAINT Key1 PRIMARY KEY (bssid)
)
''')

    cursor.execute('''
CREATE TABLE IF NOT EXISTS SeenAp
(
  bssid TEXT NOT NULL,
  essid TEXT,
  time datetime NOT NULL,
  channel int,
  freqmhz TEXT,
  maxseenrate REAL,
  carrier TEXT,
  encoding TEXT,
  packetsLLC int,
  packetsData int,
  packetsCrypt int,
  packetsTotal int,
  packetsFragments int,
  packetsRetries int,
  signal_dbm int,
  noise_dbm int,
  signal_rssi int,
  noise_rssi int,
  lat REAL,
  lon REAL,
  alt REAL,
  spd REAL,
  bsstimestamp timestamp,
  cdp_device TEXT,
  cdp_portid TEXT,
  CONSTRAINT Key3 PRIMARY KEY (time,bssid),
  CONSTRAINT SeenAp FOREIGN KEY (bssid) REFERENCES AP (bssid)
);
''')
    cursor.execute('''
	CREATE TABLE IF NOT EXISTS Client
(
  mac TEXT NOT NULL,
  manuf TEXT,
  type TEXT,
  CONSTRAINT Key1 PRIMARY KEY (mac)
)
	''')
    cursor.execute('''
	CREATE TABLE IF NOT EXISTS SeenClient
(
  mac TEXT NOT NULL,
  time datetime NOT NULL,
  channel int,
  maxseenrate REAL,
  carrier TEXT,
  encoding TEXT,
  packetsLLC int,
  packetsData int,
  packetsCrypt int,
  packetsTotal int,
  packetsFragments int,
  packetsRetries int,
  signal_dbm int,
  noise_dbm int,
  signal_rssi int,
  noise_rssi int,
  lat REAL,
  lon REAL,
  alt REAL,
  spd REAL,
  CONSTRAINT Key3 PRIMARY KEY (time,mac),
  CONSTRAINT Seen FOREIGN KEY (mac) REFERENCES Client (mac)
);
	''')
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
    cursor.execute('''
	CREATE TABLE IF NOT EXISTS Probe
(
  mac TEXT NOT NULL,
  ssid TEXT NOT NULL,
  max_rate REAL,
  packets int,
  CONSTRAINT Key5 PRIMARY KEY (mac,ssid),
  CONSTRAINT Relationship6 FOREIGN KEY (mac) REFERENCES Client (mac)
);
	''')
except:
    print('Record already exists')
db.commit()

e = xml.etree.ElementTree.parse(sys.argv[2]).getroot()

for atype in e.findall('gps-point'):
    bssid = atype.get('bssid')
    source = atype.get('source')
    timesec = atype.get('time-sec')
    timeusec = atype.get('time-usec')
    alt = atype.get('alt')
    lat = atype.get('lat')
    lon = atype.get('lon')
    signal_dbm = atype.get('signal_dbm')
    #eliminamos mac error y mac falsa de kismet
    if bssid != "00:00:00:00:00:00" and bssid != "GP:SD:TR:AC:KL:OG":
        print(bssid)
        try:
            cursor.execute('''INSERT INTO AP VALUES(?,?,?,?)''',
                           (bssid, 'unknow', 0, 0))
        except sqlite3.IntegrityError:
            print('Record already exists')

        try:
            cursor.execute('''INSERT INTO SeenAP (bssid, essid, time, signal_dbm, signal_rssi, lat, lon) VALUES(?,?,?,?,?,?,?)''',
                           (bssid, '', timesec, signal_dbm, signal_dbm, lat, lon))
        except sqlite3.IntegrityError:
            print('Record already exists')

db.commit()
