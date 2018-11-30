/*
Created: 18/11/2018
Modified: 29/11/2018
Model: SQLite 3.7
Database: SQLite 3.7
*/


-- Create tables section -------------------------------------------------

-- Table AP

CREATE TABLE AP
(
  bssid TEXT NOT NULL,
  manuf TEXT,
  lat REAL,
  lon REAL,
  CONSTRAINT Key1 PRIMARY KEY (bssid)
);

-- Table Client

CREATE TABLE Client
(
  mac TEXT NOT NULL,
  manuf TEXT,
  type TEXT,
  CONSTRAINT Key1 PRIMARY KEY (mac)
);

-- Table SeenClient

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

-- Table Connected

CREATE TABLE Connected
(
  bssid TEXT NOT NULL,
  mac TEXT NOT NULL,
  CONSTRAINT Key4 PRIMARY KEY (bssid,mac),
  CONSTRAINT Relationship2 FOREIGN KEY (bssid) REFERENCES AP (bssid),
  CONSTRAINT Relationship3 FOREIGN KEY (mac) REFERENCES Client (mac)
);

-- Table SeenAp

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

-- Table Probe

CREATE TABLE Probe
(
  mac TEXT NOT NULL,
  ssid TEXT NOT NULL,
  max_rate REAL,
  packets int,
  CONSTRAINT Key5 PRIMARY KEY (mac,ssid),
  CONSTRAINT Relationship6 FOREIGN KEY (mac) REFERENCES Client (mac)
);

