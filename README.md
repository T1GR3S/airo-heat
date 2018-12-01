# airoheat
Repositorio del equipo T1GR3$ en el hackathon de Cybercamp 2018


# TODO

- Leyenda en el mapa

- Ruta de puntos en el mapa

## Aircrack-ng 

### Install modification. 
sudo apt-get install build-essential autoconf automake libtool pkg-config libnl-3-dev libnl-genl-3-dev libssl-dev libsqlite3-dev libpcre3-dev ethtool shtool rfkill zlib1g-dev libpcap-dev

cd aircrack-ng
autoreconf -i
./configure --with-experimental
make
sudo make install

##Running example
sudo su
airmon-ng start wlan0
gpsd /dev/ttyUSB0
airodump-ng wlan0mon -w prueba --gpsd --berlin 5 --write-interval 3

##Create Database
python databaseHeatMapAircrack.py <outputDB> <inputAP> <inputClient>
Donde:      	 
        outputDB: Base de datos de salida SQLite3
     	inputAP: Fichero de aircrack modificado con los ap (formato .ap.csv)
      	inputClient: Fichero de aircrack modificado con los clientes (formato .cli.csv)
      	
      	
## Node Server 

### Installation

*sudo apt-get install node nodejs-legacy npm*

*npm i express --build-from-source*

*npm i sqlite3 --build-from-source*

*npm i body-parser --build-from-source*  

*npm i ejs --build-from-source*


### Running

*node server.js*

Visit localhost:3000

## Screenshots


# Authors

- Silvia Nerea Anguita de Blas (@silvianerea)

- Ricardo José Ruiz Fernández (@ricardojoserf)

- Elena del Portillo Peña (@elenadpp)

- Raúl Calvo Laorden (@raulcalvolaorden)

