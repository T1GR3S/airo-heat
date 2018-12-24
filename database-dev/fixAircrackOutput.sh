#Aircrack tiene problemas con ASCII extendido en kismet.xml
#Aircrack tambien tiene errores en kismet.csv con nul en ESSID 0x0

sed -i -e 's/&#x  ef;&#x  bc;&#x  8c;/,/g'  $1
sed -i -e 's/&#x  c3;&#x  b1;/ñ/g' $1
sed -i -e 's/&#x  c3;&#x  ad;/í/g' $1
sed -i -e 's/&#x  c3;&#x  ba;/ú/g' $1

sed -i -e 's/&#x  c2;&#x  ae;/®/g' $1
sed -i -e 's/&#x  c3;&#x  a9;/é/g' $1
sed -i -e 's/&#x  e9;&#x  96;&#x  92;/éf/g' $1
sed -i -e 's/&#x  ef;&#x  bc;&#x  89;/) /g' $1
sed -i -e 's/&#x  /0x/g' $1

