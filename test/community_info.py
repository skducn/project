# -*- coding: utf-8 -*-
import MySQLdb
import time
import urllib2
import json
class community_info(object):
    def __init__(self, location, city, into_db):
        self.location = location
        self.city = city
        self.ziduan = ['name', 'address', 'city', 'district', 'scope', 'crawler_time', 'location']
        self.seq = ['"', '"', '"', '"', '"', '', '"']
        self.into_db = into_db
    def do(self):
        # location =
        dif = [self.location[0] - self.location[2], self.location[3] - self.location[1]]
        b = [x / 100.0 + self.location[2] for x in xrange(int(dif[0] * 100))]
        c = [x / 100.0 + self.location[1] for x in xrange(int(dif[1] * 100))]

        d = [[x, y] for x in b for y in c]

        cnxn = MySQLdb.connect(host=self.into_db[0], user=self.into_db[1], passwd=self.into_db[2], charset=self.into_db[3])
        cursor = cnxn.cursor()
        sql = "select name from house.community_info where  city = '{}' ".format(self.city)
        cursor.execute(sql)
        url_database = [item[0] for item in cursor.fetchall()]  # 取出当前城市已有小区的名字
        # print url_database
        # for x in url_database:
        #     print x
        cnxn.commit()
        dict_data_list = []  # 字典列表
        i = 0
        for x in d:  # 遍历当前城市所有划分出来的小矩形

            html = urllib2.urlopen(
                r'http://api.map.baidu.com/place/v2/search?query=小区&bounds={},{},{},{}4&page_size=20&output=json&ak=你的ak'.format(
                    x[0], x[1], x[0] + 0.01, x[1] + 0.01))
            b = html.read()  # str
            print b
            c = json.loads(b)  # dict

            if not c['results']:
                continue
                # print json.dumps(c, ensure_ascii=False, encoding='UTF-8', indent=4)
            for x in c['results']:
                dict_data = {}
                dict_data['city'] = self.city
                dict_data['name'] = x['name'].encode('utf-8', 'ignore')
                dict_data['address'] = x['address'].encode('utf-8', 'ignore')
                try:
                    lng_lat = str(x['location']['lng']) + ',' + str(x['location']['lat'])
                except KeyError:
                    lng_lat = '0.0,0.0'
                dict_data['location'] = lng_lat
                lng_lat = ','.join(lng_lat.split(',')[::-1])
                html = urllib2.urlopen(
                    r'http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&location={}&output=json&pois=1&ak=c9nNGFV74RjSG70xIXdVLVxWPizCqXdw&callba'.format(
                        lng_lat))
                b = html.read()  # str
                b = b.split('renderReverse&&renderReverse(')[1][:-1]
                c = json.loads(b)  # dict
                dict_data['scope'] = c['result']['business'].split(',')[0].encode('utf-8', 'ignore')
                dict_data['crawler_time'] = str(int(time.time())).encode('utf-8', 'ignore')
                if not dict_data['scope']:
                    dict_data['scope'] = '其他'
                dict_data['district'] = c['result']['addressComponent']['district'].encode('utf-8', 'ignore')
                if not dict_data['district']:
                    dict_data['district'] = '其他'
                dict_data_list.append(dict_data)
                # print json.dumps(dict_data, ensure_ascii=False, encoding='UTF-8', indent=4)


        cnxn = MySQLdb.connect(host=self.into_db[0], user=self.into_db[1], passwd=self.into_db[2],
                               charset=self.into_db[3])  ###
        cursor = cnxn.cursor()
        # for x in dict_data_list:
        #     print json.dumps(x, ensure_ascii=False, encoding='UTF-8', indent=4)
        print len(dict_data_list)
        for x in dict_data_list :  # 遍历字典列表
            if not x['name'].decode('utf-8') in url_database:  # 判断小区是否已经存在
                sql = "insert into house.community_info ({}) values ({})".format(
                    ",".join([item for item in self.ziduan]),
                    ",".join([j + x[i] + j for j, i in zip(self.seq, self.ziduan)]))
                cursor.execute(sql)
        cnxn.commit()
        cnxn.close()