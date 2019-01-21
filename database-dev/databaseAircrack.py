# -*- coding: utf-8 -*-
import csv
import xml.etree.ElementTree as ET
import sqlite3
import sys
from lxml import etree
import os
import ftfy
#test fix xml error
import codecs


#reload(sys)
#sys.setdefaultencoding('utf8')

if len(sys.argv) > 1:
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
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


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


exists = os.path.isfile(sys.argv[2]+".kismet.netxml")
if exists:
    with open(sys.argv[2]+".kismet.netxml", 'r') as file :
        filedata = file.read()
    filedata = filedata.replace('&#x  ', '&#x') #fix aircrack error, remove spaces

    raiz = ET.fromstring(filedata)
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
            if essid is not None:
                essid=ftfy.fix_text(essid)
                print(essid)
            else:
                essid=""
            bssid = wireless.find("BSSID").text
            manuf = wireless.find("manuf").text
            channel = wireless.find("channel").text
            freqmhz = wireless.find("freqmhz").text.split()[0]
            carrier = wireless.find("carrier").text
            manuf = wireless.find("manuf").text
            if wireless.find("SSID").find("encryption") != None:
                encryption = wireless.find("SSID").find("encryption").text
            else:
                encryption = ""

            packetsT = wireless[8].find("total").text

            try:
                cursor.execute('''INSERT INTO AP VALUES(?,?,?,?,?,?,?,?,?,?)''', (bssid,
                                                                                essid, manuf, channel, freqmhz, carrier, encryption, packetsT, 0, 0))
            except sqlite3.IntegrityError:
                pass #print('Record already exists')
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
                    pass #print('Record already exists')
                # connected
                print (bssid, clientMac)
                try:
                    cursor.execute(
                        '''INSERT INTO connected VALUES(?,?)''', (bssid,  clientMac))
                except sqlite3.IntegrityError:
                    pass #print('Record already exists')

    # client ./
    # ap ./
    # probes ./
    # connections ./


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

exists = os.path.isfile(sys.argv[2]+".kismet.csv")
try:
	if exists:
	    with open(sys.argv[2]+".kismet.csv") as csv_file:
	        csv_reader = csv.reader(csv_file, delimiter=';')
        	line_count = 0
	        for row in csv_reader:
	            if len(row) > 0 and row[0] != "Network":
	                try:
	                    cursor.execute('''INSERT INTO AP VALUES(?,?,?,?,?,?,?,?,?,?)''', (
	                        row[3], row[2], '', row[5], 0, '', row[7], row[16], 0, 0))  # manuf y carrier implementar
	                except sqlite3.IntegrityError:
	                    pass #print('Record already exists')
	db.commit()
except:
	print("Error in kismet.csv")

try:
	exists = os.path.isfile(sys.argv[2]+".csv")
	if exists:
	    with open(sys.argv[2]+".csv") as csv_file:
	        csv_reader = csv.reader(csv_file, delimiter=',')
	        line_count = 0
	        client = False
	        for row in csv_reader:
	            if len(row) > 0 and row[0] == "Station MAC":
	                client = True
	            elif len(row) > 0 and client:
	                print(row[0])
	                try:
	                    cursor.execute('''INSERT INTO client VALUES(?,?,?,?,?,?)''',
	                                (row[0], '', 'Unknown', 'W', row[4], 'Misc'))  # manuf implementar
	                except sqlite3.IntegrityError:
	                    pass #print('Record already exists')
	
	                if row[5] != " (not associated) ":
	                    try:
	                        cursor.execute(
	                            '''INSERT INTO connected VALUES(?,?)''', (row[5],  row[0]))
	                    except sqlite3.IntegrityError:
	                        print('Record already exists')
	
	                contador = 6
	                while contador < len(row) and row[contador] != "":
	                    try:
	                        cursor.execute(
	                            '''INSERT INTO Probe VALUES(?,?,?)''', (row[0],  row[contador], 0))
	                    except sqlite3.IntegrityError:
	                        pass #print('Record already exists')
	                    contador += 1
	db.commit()
except:
        print("Error in .csv")

exists = os.path.isfile(sys.argv[2]+".log.csv")
if exists:
    with open(sys.argv[2]+".log.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if row[0] != "LocalTime":
                if len(row)>=10 and row[10] == "Client":
                    try:
                        cursor.execute('''INSERT INTO client VALUES(?,?,?,?,?,?)''',
                                    (row[3], '', 'Unknown', 'W', -1, 'Misc'))
                    except sqlite3.IntegrityError:
                        pass #print('Record already exists')

                    try:
                        if row[6] != 0.0:
                            cursor.execute('''INSERT INTO SeenClient VALUES(?,?,?,?,?,?,?)''',
                                    (row[3], row[0], 'aircrack-ng', row[4], row[6], row[7], '0.0'))
                    except sqlite3.IntegrityError:
                        pass #print('Record already exists')

                if len(row)>=10 and row[10] == "AP":

                    try:
                        cursor.execute('''INSERT INTO AP VALUES(?,?,?,?,?,?,?,?,?,?)''', (
                            row[3], row[2], '', 0, 0, '', '', 0, 0, 0))  # manuf y carrier implementar
                    except sqlite3.IntegrityError:
                        pass #print('Record already exists')

                    try:
                        if row[6] != 0.0:
                            cursor.execute('''INSERT INTO SeenAp VALUES(?,?,?,?,?,?,?,?)''', (row[3], row[0], 'aircrack-ng', row[4], row[6], row[7], '0.0', 0))
                    except sqlite3.IntegrityError:
                        pass #print('Record already exists')

db.commit()
