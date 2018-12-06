import csv
import xml.etree.ElementTree
import sqlite3
import sys


if len(sys.argv) > 1:
    if sys.argv[1] == "-h" or sys.argv[1] =="--help":
        print('''
        Usage: databaseHeatMapAircrack.py <outputDB> <aircrack output without format>
        \t outputDB: Database de salida SQLite3
        \t aircrack output without format
        ''')
        sys.exit(0) 

if len(sys.argv) < 3:
    print('databaseHeatMapAircrack.py <outputDB> <aircrack output without format>')
    sys.exit(2)

db = sqlite3.connect(sys.argv[1])
db.text_factory = str

cursor = db.cursor()

try:
    cursor.execute('''
CREATE TABLE IF NOT EXISTS AP
(
  bssid TEXT NOT NULL,
  ssid TEXT,
  manuf TEXT,
  channel int,
  frequency int,
  carrier TEXT,
  encryption TEXT,
  packetsTotal int,
  lat_t REAL,
  lon_t REAL,
  CONSTRAINT Key1 PRIMARY KEY (bssid)
);
     ''')
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
  CONSTRAINT SeenClients FOREIGN KEY (mac) REFERENCES Client (mac)
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
    db.commit()
except sqlite3.IntegrityError:
    print('Record already exists')


with open(sys.argv[2]+".kismet.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if len(row)>0 and row[0]!="Network":
            try:
                cursor.execute('''INSERT INTO AP VALUES(?,?,?,?,?,?,?,?,?,?)''', (row[3], row[2], '', row[5], 0,'', row[7] , row[16] , 0, 0)) #manuf y carrier implementar
            except sqlite3.IntegrityError:
                print('Record already exists')

db.commit()

with open(sys.argv[2]+".csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    client=False
    for row in csv_reader:
        if len(row)>0 and row[0]=="Station MAC":
            client=True
        elif len(row)>0 and client:
            try:
                cursor.execute('''INSERT INTO client VALUES(?,?,?,?,?,?)''', (row[0], '', '', 'W',row[4], 'Misc')) #manuf implementar
            except sqlite3.IntegrityError:
                print('Record already exists')
            
            if row[5]!=" (not associated) ":
                try:
                    cursor.execute('''INSERT INTO connected VALUES(?,?)''', (row[5],  row[0]))
                except sqlite3.IntegrityError:
                    print('Record already exists')

            contador=6
            while contador < len(row) and row[contador] != "":
                try:
                    cursor.execute('''INSERT INTO Probe VALUES(?,?,?)''', (row[0],  row[contador], 0))
                    contador+=1
                except sqlite3.IntegrityError:
                    print('Record already exists')


db.commit()


with open(sys.argv[2]+".gps.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if row[0]!="BSSID":
            if row[2] == "client":
                try:
                    cursor.execute('''INSERT INTO client VALUES(?,?,?,?,?,?)''', (row[0], '', '', 'W',-1, 'aircrack-ng'))
                except sqlite3.IntegrityError:
                    print('Record already exists')

                try:
                    cursor.execute('''INSERT INTO SeenClient VALUES(?,?,?,?,?,?,?)''', (row[0], row[1], 'aircrack-ng', row[4], row[5], row[6], row[7])) 
                except sqlite3.IntegrityError:
                    print('Record already exists')

            if row[2] == "ap":

                try:
                    cursor.execute('''INSERT INTO AP VALUES(?,?,?,?,?,?,?,?,?,?)''', (row[0], '', '', 0, 0,'', '' , 0 , 0, 0)) #manuf y carrier implementar
                except sqlite3.IntegrityError:
                    print('Record already exists')

                try:
                    cursor.execute('''INSERT INTO SeenAp VALUES(?,?,?,?,?,?,?,?)''', (row[0], row[1], 'aircrack-ng', row[4], row[5], row[6], row[7], 0))
                except sqlite3.IntegrityError:
                    print('Record already exists')
            
db.commit()


