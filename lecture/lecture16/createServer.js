
const http = require('http');
const url = require('url');
const fs = require('fs');
const qs = require('querystring');

http.createServer(function (req, res) {
  var q = url.parse(req.url, true);
  var filename = "." + q.pathname;
  if(req.url === '/'){
    indexPage(req,res);
  }
  else if(req.url === '/index.html'){
    indexPage(req,res);
  }
  else if(req.url == '/calendar.html'){
    calendarPage(req, res);
    //getCalendarPage(req, res);
  }
  else{
    res.writeHead(404, {'Content-Type': 'text/html'});
    return res.end("404 Not Found");
  }
}).listen(9000);


function indexPage(req, res) {
  fs.readFile('client/index.html', function(err, html) {
    if(err) {
      throw err;
    }
    res.statusCode = 200;
    res.setHeader('Content-type', 'text/html');
    res.write(html);
    res.end();
  });
}

function calendarPage(req, res) {
  fs.readFile('client/calendar.html', function(err, html) {
  if(err){
    throw err;
  }
  res.statusCode = 200;
  res.setHeader('Content-type', 'text/html');
  res.write(html);
  res.end();
  });
}

function getCalendarPage(req, res) {
  fs.readFile('calendar.json', function(err, jsonfcontents) {
  if(err){
    throw err;
  }
  //res.statusCode = 200;
  res.setHeader('Content-type', 'application/json');
  res.write(jsonfcontents);
  res.end();
  });
}





















