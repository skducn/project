# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2021-1-22
# Description: pprint 漂亮打印
# ********************************************************************************************************************

# import pprint
# dictionary = {'coord': {'lon': 77.22, 'lat': 28.67},
#               'weather': [{'id': 721, 'main': 'Haze', 'description':
#                   'haze', 'icon': '50d'}], 'base': 'stations', 'main':
#                   {'temp': 44, 'feels_like': 40.42, 'temp_min': 44,
#                    'temp_max': 44, 'pressure': 1002, 'humidity': 11},
#               'visibility': 6000, 'wind': {'speed': 4.1, 'deg': 290,
#                                            'gust': 9.3}, 'clouds': {'all': 30}, 'dt': 1590398990,
#               'sys': {'type': 1, 'id': 9165, 'country': 'IN',
#                       'sunrise': 1590364538, 'sunset': 1590414050},
#               'timezone': 19800, 'id': 1273294, 'name': 'Delhi',
#               'cod': 200}
#
#
# pp = pprint.PrettyPrinter()
# pp.pprint(dictionary)

param="ardNo=310101198004110014&idOfTargetTable=310101198004110014&targetTable=HrCover&xx={$.data.use}"

param = str(param).replace("{$.data.use}", "jinhao")
print(param)



def test():
    x = "123"
    b = "333"
    d1 ={}
    d1[x] = b
    print(d1)

    x = "$.code"
    b = "32222"
    d1[x] = b
    print(d1)
    global xx
    xx = d1


