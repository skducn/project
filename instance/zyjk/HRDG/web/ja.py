# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-8-21
# Description: 庙行健康档案数据治理页面自动化更新脚本
#***************************************************************

from HrdgPO import *
Hrdg_PO = HrdgPO()
# Hrdg_PO.clsApp("chrome.exe")

# 1，获取业务数据
# d_data = Hrdg_PO.reqPost(varurl)
# d_fData = fmtData(d_data) #格式化数据格式
dd = {
	'basicInformation': {
		'name': '魏梅娣',
		'nation': '苗族',
		'culture': '小学教育',
		'job': '军人',
		'career': '其他',
		'marriage': '离婚',
		'workUnit': '北京科美有限公司',
		'mobilePhone': '13011234567',
		'phone': '58776543',
		'contactName': '魏梅名',
		'contactPhone': '13356789098',
		'bloodType': 'B型',
		'RhType': '不详',
		'medicalPayment': '全自费',
		'handicapState': {
			'no': True,
			"vision": True,
			"audition": False,
			"member": "1212"
		}
	},
	'censusAddress': {
		'province': '上海市',
		'city': '市辖区',
		'county': '虹口区',
		'street': '广中路街道',
		'neighborhood': '新虹居委会',
		'address': '洪都拉斯100号'
	},
	'sameCensus': True,
	'liveAddress': {
		'province': '上海市',
		'city': '市辖区',
		'county': '虹口区',
		'street': '广中路街道',
		'neighborhood': '新虹居委会',
		'address': '洪都拉斯100号'
	},
	'otherInformation': {
		'kitchen': '烟囱',
		'fuel': '煤',
		'water': '井水',
		'toilet': '马桶',
		'livestock': '室内',
		'environmentDanger': {
			'no': True,
			'chemistry': False,
			'poison': True,
			'ray': True,
			'notInDetail': True,
			'other': '111'
		}
	},
	'diseaseInformation': {
		'disease': [{
			'type': '脑卒中',
			'date': '2010-12-01'
		}, {
			'type': '其他法定传染病',
			'name': '1212',
			'date':'2010-12-01'},
			{
			'type':'其他',
			'name':'1212',
			 'date': '2010-12-01'
		}],
		'operation': {
			'value': False,
			'relation': [{
				'name': '手术5',
				'date': '2010-12-01'
			}, {
				'name': '手术2',
				'date': '2010-12-03'
			}]
		},
		'trauma': {
			'value': True,
			'relation': [{
				'name': '外伤3',
				'date': '2010-12-01'
			}, {
				'name': '外伤4',
				'date': '2010-12-03'
			}]
		},
		'transfusion': {
			'value': True,
			'relation': [{
				'name': '输血7',
				'date': '2010-12-01'
			}, {
				'name': '输血8',
				'date': '2010-12-03'
			}]
		},
		'clan': [{
				'relation': "母亲",
				'dis': ['高血压', '糖尿病', '其他法定传染病', '其他'],
				'epidemic': "1212",
				'other': "456"
			},
			{
				'relation': "父亲",
				'dis': ['高血压', '糖尿病', '其他法定传染病', '贫血'],
				'epidemic': "1212"
			}
		],
		'transmissibility': '121212'
	}
}


varUrl = 'http://172.16.209.10:9071'

# 2，医生登录
Hrdg_PO.login(varUrl + '/health/select', "panxiaoye", "Pamam751200")
# Hrdg_PO.edtBasicInfo("310107194812044641")  # 魏梅娣







# try:
#     for d in range(len(d_fData)):
#         Hrdg_PO.edtBasicInfo(d_fData)
#         Web_PO.cls()
# except:
#     print(d_fData[idcard])

# 3，回填接口 更新状态
# Hrdg_PO.reqPost(varurl)
