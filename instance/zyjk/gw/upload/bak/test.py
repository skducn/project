# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-1-10
# Description: 公卫 - 省平台数据上报
# 警告如下：D:\dwp_backup\python study\GUI_wxpython\lib\site-packages\openpyxl\worksheet\_reader.py:312: UserWarning: Unknown extension is not supported and will be removed warn(msg)
# 解决方法：
import warnings
warnings.simplefilter("ignore")




import json
import time
import requests
from lxml import etree

class TengXunDoc():
    def __init__(self, doc_url, local_padId, cookie_value):
        self.doc_url = doc_url
        self.local_padId = local_padId
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'Cookie': cookie_value
        }
    # 获取当前用户信息
    def get_now_user(self):
        """
        # nowUserIndex = 'ec61dc70ef244cc0b771e772045092b6'
        # uid = '144115225804776585'
        # utype = 'wx'
        """
        req = requests.get(url=self.doc_url, headers=self.headers)
        req.encoding = req.apparent_encoding
        html = etree.HTML(req.text)
        user_list = html.xpath("/html/head/script[3]/text()")
        # 转换成字符串，再转换成json格式读取数据
        data = str(user_list[0])
        user_dict = json.loads(data.replace('window.global_multi_user=','').replace(';', ''))
        if user_dict.get("nowUserIndex") is not None:
            print(user_dict.get("nowUserIndex"))
            return user_dict['nowUserIndex']
        return 'cookie过期,请重新输入'

    # 获取当前用户ID号
    def export_task(self, export_url):
        body = {
            "docId": self.local_padId,
            "version": 2
        }
        req = requests.post(url=export_url, headers=self.headers, data=body)
        operat_id = req.json()["operationId"]
        return operat_id

    # 下载腾讯文档
    def downlowd_excel(self, check_url, file_name):
        start_time = time.time()
        file_url = ""
        while True:
            req = requests.get(url=check_url, headers=self.headers)
            progress = req.json()["progress"]

            if progress == 100:
                file_url = req.json()["file_url"]
                break
            elif time.time() - start_time > 60:
                print("数据下载超时，请检查")
                break
        if file_url:
            self.headers["content-type"] = "application/octet-stream"
            res = requests.get(url=file_url, headers=self.headers)
            with open(file_name,'wb') as fp:
                fp.write(res.content)
                print(f"文件下载成功，文件名：{file_name}")
        else:
            print("下载excel表格失败，请检查文件获取地址")

if __name__ == '__main__':
    # 腾讯文档在线地址
    # doc_url = "https://docs.qq.com/sheet/DQ1RrcEhmaXJNZkJW?tab=xxx"
    doc_url = 'https://docs.qq.com/sheet/DQmt3b0ZtaFJ0UUx0?tab=d8div6'

    # 查阅doc_info接口参数
    local_padId = "BkwoFmhRtQLt"
    # cookie_value = "fingerprint=7e633ff9db9242c99009cf614e691f5734; low_login_enable=1; pgv_pvid=630326933; fqm_pvqid=bfb7a773-809a-484d-86df-a0ca70d15941; RK=tAtYHYF5NB; ptcz=46501b5925a0c4a1dc2aec9f37dbd8f031f4a508818b3d7c44de0e48bdd1f899; OUTFOX_SEARCH_USER_ID_NCOO=567127373.0534872; optimal_cdn_domain=docs.qq.com; uid=144115264940481755; uid_key=EOP1mMQHGixtTUQ1VEJ2L1B4dlVIZnBmQmtBR0NxNW5WcEZzNk8rU3hFbXJxZzZvZlhBPSJINJTqPPgk%2FmVCNll%2BGF3I8d5iXWs65SGnN0AG4%2BJxdxMXs%2Fms2kFYE%2F%2FRVLAcCfTOOhAgJcUbi1%2BoP85ea5Be0q1CoprrcbDAKOnT0a0G; utype=wx; wx_appid=wxd45c635d754dbf59; openid=oDzL40G5enYnbGiOPcaLgatCbM7Y; access_token=75_4vqL1QeB1V-je_W0Zg8FyS-UChit8AcuDQEusHr64eQC__Wq_aR1kDb-rOFccPpY0EFAbmyn5dG5VxH9YT_EoUBaOsDUCgyxSMln-RHA7Ig; refresh_token=75_0o6XtTFLAvMZ5-j0g858sOvCL1QI1_SdXNH3u4cI4tYwOb0X00E-gSGnO6QnOwmgFhlBIIJb5lwjgNPOCRVLI9wO5NoCT3YOuW6Ed9xlHSE; env_id=gray-no2; gray_user=true; DOC_SID=2eb6521f3ebf4082a3f4891d8ecec81dfdc7588778b24f048cf05ee4047bab75; SID=2eb6521f3ebf4082a3f4891d8ecec81dfdc7588778b24f048cf05ee4047bab75; loginTime=1703730413042; pac_uid=0_b07d7f3125a41; iip=0; _qimei_uuid42=181020f0f0f1007a31502cc5a4466c0e188ba19b7d; _qimei_fingerprint=76c9f9fb45e6f34058a9a6fbba65f856; _qimei_q36=; _qimei_h38=ef971e7231502cc5a4466c0e0300000e118102; ptui_loginuin=420639919; traceid=659b6ad1bb; TOK=659b6ad1bb5a162d; hashkey=659b6ad1"
    cookie_value = "fingerprint=7e633ff9db9242c99009cf614e691f5734; low_login_enable=1; pgv_pvid=630326933; fqm_pvqid=bfb7a773-809a-484d-86df-a0ca70d15941; RK=tAtYHYF5NB; ptcz=46501b5925a0c4a1dc2aec9f37dbd8f031f4a508818b3d7c44de0e48bdd1f899; OUTFOX_SEARCH_USER_ID_NCOO=567127373.0534872; optimal_cdn_domain=docs.qq.com; uid=144115264940481755; uid_key=EOP1mMQHGixtTUQ1VEJ2L1B4dlVIZnBmQmtBR0NxNW5WcEZzNk8rU3hFbXJxZzZvZlhBPSJINJTqPPgk%2FmVCNll%2BGF3I8d5iXWs65SGnN0AG4%2BJxdxMXs%2Fms2kFYE%2F%2FRVLAcCfTOOhAgJcUbi1%2BoP85ea5Be0q1CoprrcbDAKOnT0a0G; utype=wx; wx_appid=wxd45c635d754dbf59; openid=oDzL40G5enYnbGiOPcaLgatCbM7Y; access_token=75_4vqL1QeB1V-je_W0Zg8FyS-UChit8AcuDQEusHr64eQC__Wq_aR1kDb-rOFccPpY0EFAbmyn5dG5VxH9YT_EoUBaOsDUCgyxSMln-RHA7Ig; refresh_token=75_0o6XtTFLAvMZ5-j0g858sOvCL1QI1_SdXNH3u4cI4tYwOb0X00E-gSGnO6QnOwmgFhlBIIJb5lwjgNPOCRVLI9wO5NoCT3YOuW6Ed9xlHSE; env_id=gray-no2; gray_user=true; DOC_SID=2eb6521f3ebf4082a3f4891d8ecec81dfdc7588778b24f048cf05ee4047bab75; SID=2eb6521f3ebf4082a3f4891d8ecec81dfdc7588778b24f048cf05ee4047bab75; loginTime=1703730413042; pac_uid=0_b07d7f3125a41; iip=0; _qimei_uuid42=181020f0f0f1007a31502cc5a4466c0e188ba19b7d; _qimei_fingerprint=76c9f9fb45e6f34058a9a6fbba65f856; _qimei_q36=; _qimei_h38=ef971e7231502cc5a4466c0e0300000e118102; ptui_loginuin=420639919; traceid=659b6ad1bb; TOK=659b6ad1bb5a162d; hashkey=659b6ad1"
    html = TengXunDoc(doc_url, local_padId, cookie_value)
    now_user = html.get_now_user()

    # 导出文件
    export_url = f"https://docs.qq.com/v1/export/export_office?u={now_user}"
    print(export_url)

    operat_Id  = html.export_task(export_url)
    check_url = f"https://docs.qq.com/v1/export/query_progress?u={now_user}&operationId={operat_Id}"

    # 保存文件路径
    file_name = "test.xlsx"
    html.downlowd_excel(check_url, file_name)