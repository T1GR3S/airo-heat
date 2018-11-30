import csv
import xml.etree.ElementTree
import sqlite3
import sys


if len(sys.argv) < 4:
    print 'databaseHeatMapAircrack.py <outputDB> <inputAP> <inputClient>'
    sys.exit(2)

db = sqlite3.connect(sys.argv[1])
db.text_factory = str

cursor = db.cursor()

try:
    cursor.execute('''
        CREATE TABLE AP
        (
        bssid TEXT NOT NULL,
        manuf TEXT,
        lat REAL,
        lon REAL,
        CONSTRAINT Key1 PRIMARY KEY (bssid)
        )
        ''')

    cursor.execute('''
        CREATE TABLE SeenAp
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
	CREATE TABLE Client
(
  mac TEXT NOT NULL,
  manuf TEXT,
  type TEXT,
  CONSTRAINT Key1 PRIMARY KEY (mac)
)
	''')
    cursor.execute('''
	CREATE TABLE SeenClient
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
	CREATE TABLE Connected
(
  bssid TEXT NOT NULL,
  mac TEXT NOT NULL,
  CONSTRAINT Key4 PRIMARY KEY (bssid,mac),
  CONSTRAINT Relationship2 FOREIGN KEY (bssid) REFERENCES AP (bssid),
  CONSTRAINT Relationship3 FOREIGN KEY (mac) REFERENCES Client (mac)
);
	''')
    cursor.execute('''
	CREATE TABLE Probe
(
  mac TEXT NOT NULL,
  ssid TEXT NOT NULL,
  max_rate REAL,
  packets int,
  CONSTRAINT Key5 PRIMARY KEY (mac,ssid),
  CONSTRAINT Relationship6 FOREIGN KEY (mac) REFERENCES Client (mac)
);
	''')
    db.commit()
except sqlite3.IntegrityError:
    print('Record already exists')


with open(sys.argv[2]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        print(row[0] + " "+row[1])
        try:
            cursor.execute('''INSERT INTO AP VALUES(?,?,?,?)''',
                           (row[0], 'unknow', 0, 0))
        except sqlite3.IntegrityError:
            print('Record already exists')

        try:
            cursor.execute('''INSERT INTO SeenAp VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                           (row[0], row[6], row[1], 1, '', 1, '', '', 1, 1, 1, 1, 1, 1, row[5], 1, row[5], 1, row[7], row[8], 1, 1, 1, '', ''))
        except sqlite3.IntegrityError:
            print('Record already exists')

db.commit()

with open(sys.argv[3]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        print(row[0] + " "+row[1])
        try:
            cursor.execute('''INSERT INTO Client VALUES(?,?,?)''',
                           (row[0], 'unknow', 'wifi'))
        except sqlite3.IntegrityError:
            print('Record already exists')

        try:
            cursor.execute('''INSERT INTO SeenClient VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                           (row[0], row[1], 1, 1, '', '', 1, 1, 1, 1, 1, 1, row[2], 1, row[2], 1, row[5], row[6], 1, 1))
        except sqlite3.IntegrityError:
            print('Record already exists')

        #Falta connections y probes 

db.commit()
