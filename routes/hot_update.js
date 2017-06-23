var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {

	var filename = req.query.filename;
	res.download(process.cwd()+"/public/hot_update/"+filename,filename);
	
});

module.exports = router;
