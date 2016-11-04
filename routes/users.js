var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
  
  // 工具ID号
  var id = req.query.id;
  
});

module.exports = router;
