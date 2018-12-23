import xml.etree.ElementTree
import sqlite3
import sys
from lxml import etree

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
    

exists = os.path.isfile(sys.argv[2]+".netxml")
if exists:
    doc = etree.parse(sys.argv[2]+".netxml")
    raiz = doc.getroot()
    for wireless in raiz:
        if wireless.get("type") == "probe":
            bssid = wireless.find("BSSID").text
            manuf = wireless.find("manuf").text
            packetsT = wireless.find("packets").find("total").text
            #print bssid, manuf, "W", packetsT
            try:
                cursor.execute('''INSERT INTO client VALUES(?,?,?,?,?,?)''',
                            (bssid, '', manuf, 'W', packetsT, 'Misc'))
            except sqlite3.IntegrityError:
                print('Record already exists')

            # probe
            if wireless.find("wireless-client").find("SSID").find("ssid") != None:
                essidProbe = wireless.find("wireless-client").findall("SSID")
                for ssid in essidProbe:
                    #print bssid, ssid.find("ssid").text
                    try:
                        cursor.execute('''INSERT INTO Probe VALUES(?,?,?)''',
                                    (bssid, ssid.find("ssid").text, 0))
                    except sqlite3.IntegrityError:
                        print('Record already exists')

        elif wireless.get("type") == "infrastructure":
            # ap
            essid = wireless.find("SSID").find("essid").text
            bssid = wireless.find("BSSID").text
            manuf = wireless.find("manuf").text
            channel = wireless.find("channel").text
            freqmhz = wireless.find("freqmhz").text
            if wireless.find("carrier") != None:
                carrier = wireless.find("carrier").text
            else: 
                carrier = ""
            manuf = wireless.find("manuf").text
            if wireless.find("SSID").find("encryption") != None:
                encryption = wireless.find("SSID").find("encryption").text
            else:
                encryption = ""
            if wireless[8].find("total") != None:
                packetsT = wireless[8].find("total").text
            else:
                packetsT = ""
            try:
                cursor.execute('''INSERT INTO AP VALUES(?,?,?,?,?,?,?,?,?,?)''', (bssid,
                                                                                essid, manuf, channel, freqmhz, carrier, encryption, packetsT, 0, 0))
            except sqlite3.IntegrityError:
                print('Record already exists')
            #print bssid, essid, manuf, channel,freqmhz, carrier, encryption, packetsT

            # client
            clients = wireless.findall("wireless-client")
            for client in clients:
                clientMac = client.find("client-mac").text
                manuf = client.find("client-manuf").text
                packetsT = client.find("packets").find("total").text
                #print clientMac, manuf, "W", packetsT
                try:
                    cursor.execute('''INSERT INTO client VALUES(?,?,?,?,?,?)''',
                                (clientMac, '', manuf, 'W', packetsT, 'Misc'))
                except sqlite3.IntegrityError:
                    print('Record already exists')
                # connected
                print bssid, clientMac
                try:
                    cursor.execute(
                        '''INSERT INTO connected VALUES(?,?)''', (bssid,  clientMac))
                except sqlite3.IntegrityError:
                    print('Record already exists')



exists = os.path.isfile(sys.argv[2]+".gpsdxml")
if exists:
    e = xml.etree.ElementTree.parse(sys.argv[2]+".gpsxml").getroot()

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
                cursor.execute('''INSERT INTO AP VALUES(?,?,?,?,?,?,?,?,?,?)''',
                            (bssid, 'unknow', '', 0, 0, '', '', 0, 0, 0))
            except sqlite3.IntegrityError:
                print('Record already exists')

            try:
                cursor.execute('''INSERT INTO SeenAP VALUES(?,?,?,?,?,?,?,?)''',
                            (bssid, timesec, 'Kismet', signal_dbm, lat, lon, alt, 0))
            except sqlite3.IntegrityError:
                print('Record already exists')

db.commit()
