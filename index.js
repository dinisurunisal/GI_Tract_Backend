const express = require('express');

const app = express();
const PORT = 3000;

app.get('/', function(req, res) {
    res.send('GET request to homepage')
})