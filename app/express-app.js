var express = require('express');
var fs = require('fs');
var app = express();
var bodyParser = require('body-parser');

app.use(bodyParser.json());

app.get('/', function (req, res) {
    res.sendFile('index.html', { root: __dirname + '/' });
});

app.get('/series.json', function (req, res) {
    res.sendFile('series.json', { root: __dirname + '/../' });
});

app.get('/*', function (req, res) {
    console.log('params length: '+req.originalUrl);
    res.sendFile(req.originalUrl, { root: __dirname + '/'});
});

app.put('/series.json', function(req, res){
    var html = fs.writeFileSync('series.json', JSON.stringify(req.body));
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end('thanks');
});

var server = app.listen(3000, function () {
    var host = server.address().address;
    var port = server.address().port;

    console.log('Server running at http://%s:%s', host, port);
});
