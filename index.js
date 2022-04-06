const express = require('express');
const axios = require('axios');
const fs = require('fs');
const uploadFile = require("./middleware/upload");

const app = express();
const port = 3000;

global.__basedir = __dirname;

app.use(express.urlencoded({ extended: true }));
app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Methods", "GET,HEAD,OPTIONS,POST,PUT,DELETE");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization,access-control-allow-origin");
    next();
});

app.get('/', function(req, res) {
    res.send('GET request to homepage')
})

app.get('/api/home', async function(req, res){
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

app.post('/api/upload', async function(req, res) {
    try {
        await uploadFile(req, res);
        if (req.file == undefined) {
          return res.status(400).send({ message: "Please upload a file!" });
        }
        res.status(200).send({
          message: "Uploaded the file successfully: " + req.file.originalname,
        });
    } catch (err) {
        if (err.code == "LIMIT_FILE_SIZE") {
            return res.status(500).send({
                message: "File size cannot be larger than 2MB!",
            });
    }
    res.status(500).send({
        message: `Could not upload the file: ${req.file.originalname}. ${err}`,
    });
    }  
})

app.get('/api/getfiles', function(req, res){
    const directoryPath = __basedir + "/assets/uploads/";
    fs.readdir(directoryPath, function (err, files) {
      if (err) {
        res.status(500).send({
          message: "Unable to scan files!",
        });
      }
      let fileInfos = [];
      files.forEach((file) => {
        fileInfos.push({
          name: file,
          url: 'http://localhost:3000/api/getfiles/' + file,
        });
      });
      res.status(200).send(fileInfos);
    });
}) 

app.listen(port, () => {
    console.log(`Now listening on port ${port}`);
}); 