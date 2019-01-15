echo
echo
echo "Aircrack-ng installation..."
echo
echo
sudo su
airmon-ng start wlan0
gpsd /dev/ttyUSB0
airodump-ng wlan0mon -w prueba --gpsd --berlin 5 --write-interval 3
