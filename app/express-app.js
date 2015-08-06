var express = require('express');
var fs = require('fs');
var app = express();

app.get('/', function (req, res) {
    var html = fs.readFileSync('app/index.html');
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end(html);
});

app.get('/?*', function (req, res) {
    res.send('/?*');
});

app.post('/*', function(req, res){
    var html = fs.writeFileSync('/*', req.body);
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end('thanks');
});

var server = app.listen(3000, function () {
    var host = server.address().address;
    var port = server.address().port;

    console.log('Server running at http://%s:%s', host, port);
});
