runAllEHR.py

from parameterized import parameterized    //unitest @parameterized.expand
from BeautifulReport import BeautifulReport as bf   //生成报表


1，遍历case获取参数
xls.py - XLS - getCaseParam([[2, 3, 5], [], 0],'/inter/HTTP/auth')
返回：[['获取Token', 'post', '/inter/HTTP/auth', 'None', '$.status','200']]

           d_jsonres = xls.result(excelNo, caseName, method, interName, dict(eval(param)), jsonpathKey, expected)

      xls.setCaseParam(excelNo, "token=" + token[0], 'pass', str(d_jsonres), '', '')

2，每个接口名称对应的函数，如 '/inter/HTTP/auth'
testAuth('获取Token', 'post', '/inter/HTTP/auth', 'None', '$.status','200')

	a，HTTP反射函数
	reflection.run(['获取Token', 'post', '/inter/HTTP/auth', 'None', '$.status','200'])
	调用iDriven.py - HTTP - post(interName, param, jsonpath1, expected)
	如同：post('/inter/HTTP/auth', 'None', '$.status','200')
	返回： # {"status":401,"msg":"用户名密码错误"}
	
	判断 status = 401，输出assert
	保存 token值
	更新excel对应的 saveparam，result,actual 


  jsonres = reflection.run([caseName, method, interName, param, jsonpathKey, expected])
        d_jsonres = json.loads(jsonres)
        jsonpathValue = jsonpath.jsonpath(d_jsonres, expr=jsonpathKey)
        jsonpathValue = str(jsonpathValue[0])
        # 断言预期结果
        if jsonpathValue != expected :
            xls.setCaseParam(excelNo, '', 'Fail', str(d_jsonres))
            assert jsonpathValue == expected, "预期值是" + expected + "，而实测值是" + jsonpathValue
        else:
            token = jsonpath.jsonpath(d_jsonres, expr='$.token')
            runAll.token = token[0]
            token = "token=" + str(runAll.token)
            xls.setCaseParam(excelNo,token,'pass',str(d_jsonres))


'''

        :return: userid
        '''

        # 自动匹配 param 参数
        if '=' not in param:
            for k, v in xls.d_inter.items():
                if '/inter/HTTP/login' == k :
                    param = http.getJointParam(v, param)
                    break
        jsonres = reflection.run([caseName, method, interName, param, jsonpathKey, expected])
        d_jsonres = json.loads(jsonres)
        jsonpathValue = jsonpath.jsonpath(d_jsonres, expr=jsonpathKey)
        jsonpathValue = str(jsonpathValue[0])
        # 断言预期结果
        if str(jsonpathValue) != str(expected):
            xls.setCaseParam(excelNo, '', 'Fail', str(d_jsonres))
            assert str(jsonpathValue) == str(expected), "预期值：" + str(expected) + "，实测值：" + str(jsonpathValue)
        else:
            # 获取根节点下的userid节点的值，用于关联下个接口
            if "userid" in d_jsonres:
                userid = jsonpath.jsonpath(d_jsonres, expr='$.userid')
                runAll.userid = userid[0]
                userid = "userid=" + str(runAll.userid)
                xls.setCaseParam(excelNo, userid, 'pass', str(d_jsonres))
            else:
                xls.setCaseParam(excelNo, '', 'pass', str(d_jsonres))


 """ 登出 """

        # result('userid',runAll.userid,'token',runAll.token)

        if '=' not in param:
            for k, v in xls.d_inter.items():
                if '/inter/HTTP/logout' == k:
                    param = http.getJointParam(v, param)
                    break
        # 关联参数
        if "?" or "&" in param:
            param = param.replace("userid=?", "userid=" + runAll.userid)
            param = param.replace("token=?", "token=" + runAll.token)
            param = param.replace("userid=$userid", "userid=" + runAll.userid)
            param = param.replace("token=$token", "token=" + runAll.token)
        jsonres = reflection.run([caseName, method, interName, param, jsonpathKey, expected])
        d_jsonres = json.loads(jsonres)
        jsonpathValue = jsonpath.jsonpath(d_jsonres, expr=jsonpathKey)
        jsonpathValue = str(jsonpathValue[0])
        # 断言预期结果
        if str(jsonpathValue) != str(expected):
            xls.setCaseParam(excelNo, '', 'Fail', str(d_jsonres))
            assert str(jsonpathValue) == str(expected), "预期值：" + str(expected) + "，实测值：" + str(jsonpathValue)
        else:
            xls.setCaseParam(excelNo, '', 'pass', str(d_jsonres))