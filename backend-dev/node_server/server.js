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

app.get('/table', function(req, res){
    db.all("SELECT lat,lon,signal_rssi FROM SeenAP where essid=' Cybercamp2018'", function(err, row){
        //console.log(row);
        res.render('html/tables.html', {row:row});
    });
});


app.get('/table_clients', function(req, res){
    db.all("SELECT mac,manuf,type FROM Client", function(err, row){
        //console.log(row);
        res.render('html/table_clients.html', {row:row});
    });
});

app.get('/table_ap', function(req, res){
	var networkName = ' Cybercamp2018';
    db.all("SELECT essid,bssid,signal_rssi FROM SeenAP where essid='"+networkName+"' GROUP BY bssid", function(err, row){
        //console.log(row);
        res.render('html/table_ap.html', {row:row, name:networkName});
    });
});


app.get('*', function(req, res) {  
    res.sendfile('html/index.html');
});

app.listen(config.web.port);
console.log("Visit http://localhost:3000");
