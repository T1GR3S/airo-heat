// Based on: https://gist.github.com/dalelane/6ce08b52d5cca8f92926

var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('database.db');
var bodyParser = require('body-parser');
var express = require('express');
var app = express();

app.use(express.static(__dirname + '/'));
app.use(bodyParser.urlencoded({extend:true}));
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.set('views', __dirname);


app.get('/data', function(req, res){
    db.all("SELECT lat,lon,signal_rssi FROM SeenAP", function(err, row){
        console.log(row);
        res.render('heatmap/test.html', {row:row});
    });
});

app.listen(3000);
console.log("Visit http://localhost:3000/data");