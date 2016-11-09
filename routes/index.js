var express = require('express');
var router = express.Router();

var resp;
var config = require("./config.json")
/* GET home page. */
router.get('/', function(req, res, next) {

	// 获取ID
	var id = req.query.id;
	resp = res;

	if(id==1){
		// 数据转换
		var scriptPath = process.cwd()+ "/routes/ExcelToLua.py";
		var cmd = scriptPath+' '+config.excelPath+' '+config.excelToLuaPath
		execPy(cmd)
	}
	else if(id==2){
		// 热更新
	}	
	else if(id==4){
		// 检查相同文件
		var scriptPath = process.cwd()+ "/routes/checkSameFile.py";
		var cmd = scriptPath+' '+config.sameFilePath
		execPy(cmd)

	}
	else if(id==5){
		// 测试svn
		var scriptPath = process.cwd()+ "/routes/svn.py";

	}
	else{
		printToHtml('欢迎使用在线工具，如有建议，请联系作者！');
	}


});

// 执行python 文件
function execPy(pCmd,pCallback){

	var exec = require('child_process').exec;

	exec('python '+pCmd,function(error,stdout,stderr){
	    if(stdout.length >1){
	        printToHtml(stdout);
	    } else {
	        console.log('you don\'t offer args');
	    }
	    if(error) {
	        printToHtml("\nerror:"+stderr);
	    }
	});
}

// 执行shell文件
function execShell(pCmd,pCallback){

	var exec = require('child_process').exec;

	exec('sh '+pCmd,function(error,stdout,stderr){
	    if(stdout.length >1){
	        printToHtml("程序已启动！");
	    } else {
	        console.log('you don\'t offer args');
	    }
	    if(error) {
	        printToHtml("\nerror:"+stderr);
	    }
	}); 
}
// 打印
function printToHtml(ptext){
	console.log(ptext);
	resp.render('index', {text:ptext});
}
module.exports = router;
