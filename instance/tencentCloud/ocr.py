# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2022-6-24
# Description: 文字识别 - 将图片内容转为excel
# https://www.cnblogs.com/littlefatsheep/p/11024505.html
# https://intl.cloud.tencent.com/zh/document/product/583/19698
# https://console.cloud.tencent.com/
# https://console.cloud.tencent.com/ocr/overview
# ***************************************************************


import numpy as np
import pandas as pd
import os
import json
import re
import base64
import xlwings as xw
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models


class Ocr():

    def excelFromPictures(self, picture, SecretId, SecretKey):
        try:
            with open(picture, "rb") as f:
                img_data = f.read()
            img_base64 = base64.b64encode(img_data)
            cred = credential.Credential(SecretId, SecretKey)  # ID和Secret从腾讯云申请
            httpProfile = HttpProfile()
            httpProfile.endpoint = "ocr.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)

            req = models.TableOCRRequest()
            params = '{"ImageBase64":"' + str(img_base64, 'utf-8') + '"}'
            req.from_json_string(params)
            resp = client.TableOCR(req)
            #     print(resp.to_json_string())
        except TencentCloudSDKException as err:
            print(err)
        ##提取识别出的数据，并且生成json
        result1 = json.loads(resp.to_json_string())
        rowIndex = []
        colIndex = []
        content = []
        for item in result1['TextDetections']:
            rowIndex.append(item['RowTl'])
            colIndex.append(item['ColTl'])
            content.append(item['Text'])
        ##导出Excel
        ##ExcelWriter方案
        rowIndex = pd.Series(rowIndex)
        colIndex = pd.Series(colIndex)
        index = rowIndex.unique()
        index.sort()
        columns = colIndex.unique()
        columns.sort()
        data = pd.DataFrame(index=index, columns=columns)
        for i in range(len(rowIndex)):
            data.loc[rowIndex[i], colIndex[i]] = re.sub(" ", "", content[i])
        writer = pd.ExcelWriter("./" + re.match(".*\.", f.name).group() + "xlsx", engine='xlsxwriter')
        data.to_excel(writer, sheet_name='Sheet1', index=False, header=False)
        writer.save()

    def get_filename(self, path, filetype):
        name = []
        final_name = []
        for root, dirs, files in os.walk(path):
            for i in files:
                if filetype in i:
                    name.append(i.replace(filetype, ''))
        final_name = [item + filetype for item in name]
        return final_name


    def x(self, SecretId, SecretKey, FileStyle):
        pictures = self.get_filename("./", FileStyle)

        for pic in pictures:
            self.excelFromPictures(pic, SecretId, SecretKey)
            print("[Done], " + pic + " => " + FileStyle)

if __name__ == '__main__':

    Ocr_PO = Ocr()

    # 对当前目录下所有jpg文件生成对应的excel
    Ocr_PO.x('AKIDqUt3ye4FAqHSO5XjgOq30iBOM4YmlV1I', '3qOgjW4MPCj14rOgjW4RZUBcpnW1IJ5b', "jpg")


