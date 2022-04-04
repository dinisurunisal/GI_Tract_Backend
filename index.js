const express = require('express');
const axios = require('axios');
const fileupload = require('express-fileupload');  

const app = express();
const port = 3000;

app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Methods", "GET,HEAD,OPTIONS,POST,PUT,DELETE");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization,access-control-allow-origin");
    next();
});

app.get('/', function(req, res) {
    res.send('GET request to homepage')
})

app.get('/home', async function(req, res){
    console.log('calling');

    const predict = await axios({
        method: 'POST',
        url: 'http://127.0.0.1:5000/flask',
        headers: { 'Content-Type': 'text/plain' },
        data: req,
    }).catch(e => e)
    if (predict instanceof Error) {
        result = "Cannot say Exactly";
        console.log('Error E:', predict)
    } else {
        console.log(res);
    }
});

app.post('/upload', function(req, res) {
    let file = req['files'].images;  
  
    console.log("File uploaded: ", file.name);  
})

app.listen(port, () => {
    console.log(`Now listening on port ${port}`);
}); 