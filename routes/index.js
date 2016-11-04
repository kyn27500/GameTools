var express = require('express');
var router = express.Router();

var resp;
/* GET home page. */
router.get('/', function(req, res, next) {

	// 获取ID
	var id = req.query.id;
	resp = res;

	printToHtml('欢迎使用在线工具，如有建议，请联系作者！');
});


// 打印
function printToHtml(ptext){
	console.log(ptext);
	resp.render('index', {text:ptext});
}
module.exports = router;
