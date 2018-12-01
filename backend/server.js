// Based on: https://gist.github.com/dalelane/6ce08b52d5cca8f92926

var config = require('./config');
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database(config.web.db);
var bodyParser = require('body-parser');
var express = require('express');
var app = express();

app.use(express.static(__dirname + '/'));
app.use(bodyParser.urlencoded({extend:true}));
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.set('views', __dirname);

app.get('/data', function(req, res){
    db.all("SELECT lat,lon,signal_rssi FROM SeenAP where essid=' Cybercamp2018'", function(err, row){
        //console.log(row);
        res.render('heatmap/test.html', {row:row});
    });
});

/// BORRAR
app.get('/data2', function(req, res){
    db.all("SELECT lat,lon,signal_rssi FROM SeenAP where essid=' Cybercamp2018'", function(err, row){
        //console.log(row);
        res.render('heatmap/prueba.html', {row:row});
    });
});

/*
/// BORRAR
app.get('/table', function(req, res){
    db.all("SELECT lat,lon,signal_rssi FROM SeenAP where essid=' Cybercamp2018'", function(err, row){
        //console.log(row);
        res.render('html/tables.html', {row:row});
    });
});
*/

app.get('/select_clients', function(req, res){
    db.all("SELECT distinct essid from SeenAP", function(err, row){
        res.render('html/select_client.html', {row:row});
    });
});

app.post('/table_clients', function(req, res){
    var networkName = req.body.network_name || '';
    db.all("SELECT Connected.bssid, mac, Client.type as 'Type (Wifi/Bluetooth)' from Connected NATURAL JOIN Client WHERE Connected.bssid in (SELECT bssid FROM SeenAp where essid='"+networkName+"')", function(err, row){
        res.render('html/table_clients.html', {row:row});
    });
});

//APs filtered by ESSID
app.post('/table_ap', function(req, res){
	var networkName = req.body.ap_name || '';
    db.all("SELECT essid, bssid, MAX(signal_rssi) 'Max RSSI', MIN(signal_rssi) 'Min RSSI', CAST(round(AVG(signal_rssi)) as int) 'Average RSSI' FROM SeenAP where essid='"+networkName+"' GROUP BY bssid", function(err, row){
        res.render('html/table_ap.html', {row:row, name:networkName});
    });
});

//APs filtered by BSSID
app.post('/table_ap_mac', function(req, res){
	var networkMAC= req.body.ap_mac || '';
    db.all("SELECT essid, bssid, MAX(signal_rssi) 'Max RSSI', MIN(signal_rssi) 'Min RSSI', CAST(round(AVG(signal_rssi)) as int) 'Average RSSI' FROM SeenAP where bssid='"+networkMAC+"' GROUP BY bssid", function(err, row){
        res.render('html/table_ap.html', {row:row, name:networkMAC});
    });
});

app.get('/select_ap', function(req, res){
    res.render('html/select_ap.html');
});

app.get('/select_ap_mac', function(req, res){
    res.render('html/select_ap_mac.html');
});

app.get('/select_heatmap_name', function(req, res){
    res.render('html/select_heatmap_name.html');
});

app.get('/select_heatmap_mac', function(req, res){
    res.render('html/select_heatmap_mac.html');
});

app.post('/heatmap_name', function(req, res){
	var networkName = req.body.ap_name || '';
    db.all("SELECT lat,lon,MAX(signal_rssi) FROM SeenAP where essid='"+networkName+"' GROUP BY lat,lon", function(err, row){
        //console.log(row);
        res.render('heatmap/prueba.html', {row:row});
    });
});

app.post('/heatmap_mac', function(req, res){
	var networkMAC= req.body.ap_mac || '';
    db.all("SELECT lat,lon,MAX(signal_rssi) FROM SeenAP where bssid='"+networkMAC+"' GROUP BY lat,lon", function(err, row){
    //db.all("SELECT lat,lon,signal_rssi FROM SeenAP where bssid='"+networkMAC+"'", function(err, row){
        //console.log(row);
        res.render('heatmap/prueba.html', {row:row});
    });
});

app.get('*', function(req, res) {  
    res.sendfile('html/index.html');
});

app.listen(config.web.port);
console.log("Visit http://localhost:3000");
