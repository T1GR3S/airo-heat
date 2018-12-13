echo "Node server installation..."
echo
echo
sudo apt-get install node nodejs-legacy npm
npm i express --build-from-source
npm i sqlite3 --build-from-source
npm i body-parser --build-from-source
npm i ejs --build-from-source

echo
echo
echo "Aircrack-ng installation..."
echo
echo
sudo su
airmon-ng start wlan0
gpsd /dev/ttyUSB0
airodump-ng wlan0mon -w prueba --gpsd --berlin 5 --write-interval 3
