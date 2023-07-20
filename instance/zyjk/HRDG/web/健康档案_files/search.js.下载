function toggleVisibility(div1) {
	if (div1.style.display == "") {
		div1.style.display = "none";
		document.getElementById("pctid").src = ctxStatic
			+ '/main/wd_images/pp_up.png';
	} else {
		div1.style.display = "";
		document.getElementById("pctid").src = ctxStatic
			+ '/main/wd_images/pp_down.png';
	}
}
function toggleVisibility2(div1) {
	if (div1.style.display == "none") {
		div1.style.display("pctid").src = ctxStatic
				+ '/main/wd_images/pp_down.png';
	} else {
		div1.style.display = "none";
	}
}
function validateKey(key) {
	if(key != null && key != undefined && key != '' && key.length < 6){
		var flag = false;
		for(var i = 0 ; i < key.length ; i++){
			var c = key[i];
			if(!((c >= '0' && c <= '9') || c == "x" || c == "X" || c == " ")){
				flag = true;
				break;
			}
		}
        if(!flag) {
            mini.showTips({content: "按照身份证查询，输入不能小于六位", state: "success", x: "center", y: "center", timeout: "2000"});
        }
		return flag;
	}
	return true;
}


//function validateIDCard(key){
//	if(key != null && key != undefined && key != ''){
//		if(key.length >= 6){
//			if(key.length == 15 || key.length == 18){
//				var reg = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;
//				if(reg.test(key) === false){
//					mini.showTips({content: "身份证格式不正确", state: "success", x: "center", y: "center", timeout: "2000"});
//					return  false;
//				}
//			}else{
//				var reg = /(^\d{5,17}(\d|X|x)$)/;
//				if(reg.test(key) === false){
//					mini.showTips({content: "身份证格式不正确", state: "success", x: "center", y: "center", timeout: "2000"});
//					return  false;
//				}
//			}
//		}else{
//			var reg = /(^\d*(\d|X|x)$)/;
//			if(reg.test(key) === false){
//				mini.showTips({content: "身份证格式不正确", state: "success", x: "center", y: "center", timeout: "2000"});
//				return  false;
//			}else{
//				mini.showTips({content: "身份证格式不正确,且输入不能小于6位", state: "success", x: "center", y: "center", timeout: "2000"});
//				return  false;
//			}
//		}
//	}
//	return true;
//}
