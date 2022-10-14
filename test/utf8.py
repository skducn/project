# coding: utf-8
#****************************************************************
# Author     : John
# Date       : 2017-4-6
# Description: 编码与解码
# 中文\unicode编码在线转换工具, http://www.bangnishouji.com/tools/chtounicode.html
# 在线base64编码解码、base64加密解密 - aTool在线工具 http://www.atool.org/base64.php
# 乱码解析 http://www.mytju.com/classCode/tools/messyCodeRecover.asp
#****************************************************************


# 在str的文档中有这样的一句话:
# 也就是说在读取一个文件的内容或者从网络上读取到内容时，保持的对象为str类型；
# 如果想把一个str转换成特定编码类型，需要把str转为Unicode,然后从unicode转为特定的编码类型如：utf-8、gb2312等；

# unicode 转 gb2312,utf-8等
x = '[{"end":3760,"start":1930,"text":"鍡紝鏅氫笂濂斤紝鎴戞槸濯涘獩銆�"},{"end":8470,"start":4200,"text":"鎴戠涓€娆￠偅涔堟竻妤氬湴鐪嬪埌濂充富澶栵紝鐢蜂富鍐呯殑瀹跺涵"},{"end":10600,"start":8620,"text":"鍘熸潵骞舵病鏈夋兂璞′腑鐨勭畝鍗曘€�"},{"end":13120,"start":10940,"text":"鎴戣窡瀵硅薄涔嬪墠鐩樼畻寰楀ソ濂界殑锛�"},{"end":15090,"start":13380,"text":"鎴戜滑涓嶆寜浠€涔堢敺濂冲垎"},{"end":20630,"start":15090,"text":"灏辫皝鐨勬敹鍏ユ洿楂橈紝璋佸氨璐熻矗瀹跺涵鐨勭粡娴庢潵婧愶紝鍙︿竴鏂规寜闇€鍦ㄥ甯﹀▋銆�"},{"end":23930,"start":20910,"text":"鐞嗘兂寰堜赴婊★紝浣嗚涓€绡囨枃绔犳墦鍊掋€�"},{"end":27380,"start":24250,"text":"鏂囩珷寰堢湡璇氾紝鏄竴浣嶅コ鍗氬＋鐨勮嚜杩帮紝"},{"end":29540,"start":27680,"text":"浠栧崥澹鍘嗗仛绉戠爺"},{"end":31160,"start":29670,"text":"鎷垮埌鐨刼ffer寰堝ソ銆�"},{"end":37660,"start":31410,"text":"浠栧璞℃湰绉戝鍘嗘瘯涓氬悗灏辫窡鐫€瀵煎笀鍒涗笟锛屼絾鍏徃涓€鐩存病浠€涔堣捣鑹诧紝鏀跺叆涓嶅浠�"},{"end":43400,"start":37940,"text":"瀹跺涵鍒╃泭鏈€澶у寲鐨勭洰鐨勩€備笅鎬€瀛曠敓瀛╁瓙鐨勬椂鍊欐槸鐢风敓閫掍氦浜嗚緸鑱屼俊鍥炰簡瀹躲€�"},{"end":45410,"start":43740,"text":"浣嗘槸鍛紝浜嬪疄璇佹槑锛�"},{"end":49160,"start":45760,"text":"灏辩畻鐢蜂富鍐呭コ鎬х殑宸ヤ綔渚濇棫浼氭柇銆傚綋"},{"end":51060,"start":49420,"text":"鏂囩珷閲屾湁涓粏鑺傦紝"},{"end":57030,"start":51400,"text":"浣滆€呮妸鑷繁浠庝簩闆朵竴鍏勾璇诲崥鍒颁簩闆朵簩浜屽勾鍏勾闂村彂琛ㄧ殑鏂囩珷鍋氭垚浜嗕竴涓垪琛ㄣ€�"},{"end":62880,"start":57320,"text":"鐒跺悗鎶婂勾浠介兘鏍囨敞绾㈣壊锛岄棶瀛︾敓鑳藉惁浠庤繖閲岄潰鐪嬪嚭澹拌獕瀵逛粬鐨勫奖鍝嶏紝"},{"end":66020,"start":63190,"text":"鏈変釜濂冲悓瀛﹀緢蹇氨鍙戠幇闂锛岃"},{"end":69160,"start":66060,"text":"鑰佸笀2020骞村唴涓€骞存槸绌虹櫧鐨勩€�"},{"end":71790,"start":69440,"text":"浠栭棶濂冲悓瀛︼紝鐭ヤ笉鐭ラ亾鍘熷洜锛�"},{"end":74430,"start":72100,"text":"濂冲悓瀛﹁锛屼綘鍘荤敓瀛╁瓙浜嗐€�"},{"end":79080,"start":74790,"text":"浠栬锛屽锛屽苟涓旇繖骞朵笉鏄粬涓€涓汉鐗规湁鐨勭幇璞°€�"},{"end":85020,"start":79400,"text":"寰堝濂冲鑰呴兘浼氬嚭鐜扮被浼肩殑瀛︽湳鏂。锛屽線寰€灏辨槸浠栦滑鍘荤敓瀛╁瓙鐨勯偅鍑犲勾銆�"},{"end":86790,"start":85300,"text":"鑰屼笌姝ゅ悓鏃讹紝"},{"end":89690,"start":86810,"text":"鐢峰鑰呭嵈鍑犱箮涓嶅彈鐢熻偛鐨勪换浣曞奖鍝嶏紝"},{"end":92880,"start":90060,"text":"闄や簡鎶婂瀛愮敓鍑烘潵鍠傚ザ涔熸槸涓€澶ч噸浠汇€俓n"},{"end":95490,"start":93210,"text":"浣滆€呰锛屼粬姣忓ぉ瑕佸杺濂藉嚑娆″ザ锛�"},{"end":101250,"start":95790,"text":"鏅氫笂鍗佷竴鐐瑰杺瀹岋紝褰撳ぉ鏈€鍚庝竴娆″ザ鍚庡氨鍘荤潯瑙夈€傜浜屽ぉ鏃╀笂鍏偣鍐嶈捣搴婂杺濂�"},{"end":103740,"start":101590,"text":"澹拌獕浼间箮鏄コ浜虹殑澶╄亴锛�"},{"end":110140,"start":104060,"text":"鍥犱负鐢峰コ鐨勬瀯閫犱笉鍚岋紝鎵€浠ュコ鎬т笉鍙兘鍋氬埌鍜岀敺鎬т竴鏍凤紝瀹屽叏涓嶅彈鐢熻偛鐨勫奖鍝嶃€�"},{"end":111960,"start":110470,"text":"鎴戞兂浜嗘兂锛屽鎴戯紝"},{"end":114470,"start":112060,"text":"鎴戝皢鏉ュ叾瀹炰篃浼氶潰涓村悓鏍风殑闂銆�"},{"end":118820,"start":114790,"text":"涓€锛屾€€瀛曟垜鐨勭洿鎾枃绔狅紝瑙嗛鏇存柊閮戒細鍙楀奖鍝嶏紝"},{"end":123530,"start":119160,"text":"鍐嶄笉鑳戒竴澶╁崄鍏釜灏忔椂杩炶酱宸ヤ綔锛屽噷鏅ㄤ笁鍥涚偣鎵嶇潯瑙変簡銆�"},{"end":126890,"start":123850,"text":"灏辩畻鏄コ涓诲涓э紝鍋跺紡濠氬Щ涔熷彲鑳藉瓨鍦ㄣ€俓n"},{"end":129040,"start":127200,"text":"涓轰粈涔堣杩欎釜鏂囩珷鐪熻瘹锛�"},{"end":132100,"start":129370,"text":"鍥犱负浣滆€呮壙璁よ嚜宸变笉绠椾竴涓ソ濡堝銆�"},{"end":136430,"start":132460,"text":"浠栧伐浣滃緢蹇欙紝缁忓父涓嬬彮鍥炲鍚庤繕瑕佷細棰嗗娑堟伅锛�"},{"end":139360,"start":136750,"text":"鎵€浠ユ病鏈夋洿澶氭椂闂村幓闄瀛愩€�"},{"end":144590,"start":139660,"text":"娌℃椂闂村埌銆備袱宀佸鐨勫効瀛愪細鎷跨潃鎵嬫満妯′豢浠栬锛屾垜瑕佸洖蹇嗕竴涓嬮瀵间俊鎭€�"},{"end":147230,"start":144680,"text":"浼氭ā浠垮濡堣嫤鐫€鑴稿繖宸ヤ綔鐨勮〃鎯咃紝"},{"end":152210,"start":147620,"text":"浠栦篃鎵胯鑷繁涓嬬彮鍚庝篃鎯宠翰杩涜溅閲屾娊鏍圭儫锛岀紦瑙ｇ紦瑙ｅ帇鍔涖€�"},{"end":156770,"start":152500,"text":"鐢氳嚦鎯抽€冮伩鑲插効锛屽畞鎰垮幓鍋ヨ韩鎴挎捀閾侊紝涔熶笉鎯冲洖瀹跺杺濂讹紝"},{"end":159270,"start":157110,"text":"鍍忎竴涓櫘閫氱殑涓勾鐢蜂汉涓€鏍凤紝"},{"end":170500,"start":159570,"text":"鏈夋鏃堕棿璺熻€佸叕涓€璧峰甫濞冿紝浠栧彂鐜拌嚜宸卞繀椤绘瘡澶╁湪鍠傚ザ缈昏瘧锛屼拱鑿滐紝鍐欒鏂囷紝鍋氶キ锛屽璇撅紝娲楃锛岀湅涔︼紝鍋氬鍔′箣闂存潵鍥炲垏鎹€�"},{"end":177160,"start":170670,"text":"闈炲父闈炲父绱紝鐢氳嚦鍩嬫€ㄨ€佸叕涓轰粈涔堜笉鑳藉儚鍏朵粬鍏ㄨ亴濡堝涓€鏍凤紝涓€涓汉鍖呮徑鎵€鏈変簨锛�"},{"end":181180,"start":177510,"text":"浠栧潶璇氳嚜宸卞彉鎴愪簡钀ㄥ寮忕帀鍎块噷鐨勯偅涓伓銆�"},{"end":183940,"start":181470,"text":"鐢ㄦ剰娈嬮叿鐨勭湡鐩歌鍛堢幇鍑烘潵锛�"},{"end":188620,"start":184260,"text":"璧氶挶鐨勯偅涓汉鐪熺殑涓嶄細鍦ㄦ煇涓灛闂村珜寮冧綘鐨勪即渚ｅ悧锛�"},{"end":194380,"start":188900,"text":"浣犵湡鐨勮兘澶熷仛鍒拌嚜濮嬭嚦缁堝彂鑷唴蹇冪殑璁ゅ彲浣犵殑浼翠荆鑲插効鍔冲姩鐨勪环鍊煎悧锛�"},{"end":200460,"start":194700,"text":"宸ヤ綔寰堝繖锛屼綘鑳藉璐熸媴寰楄捣鑷繁搴斿敖鐨勯偅涓€浠借偛鍎胯矗浠伙紝鑰屼笉鏄矗浠绘帹鍗稿悧銆�"},{"end":204760,"start":200760,"text":"鏃犺姘寸叜鐖憋紝鐢熸椿鐨勯噸鎷呴兘涓嶄細娑堝け锛屽彧浼氳浆绉汇€�"},{"end":207280,"start":205070,"text":"杩欎簺杩介棶閮藉€煎緱琚彁鍓嶈€冭檻銆�"},{"end":212050,"start":207600,"text":"灏辩畻涓や汉閮借鍚岃繖绉嶅搴ā寮忥紝涔熶竴瀹氫細鏈変汉瀵规鏀寔鐐圭偣"},{"end":219890,"start":212340,"text":"澶栦汉鐨勭溂鍏夈€備綔鑰呯殑鑰佸叕鐧藉ぉ鍦ㄥ皬鍖洪噷閬涘▋鏃讹紝浼氬彈鍒板叾浠栧甫濞冪殑濂跺ザ濠嗗﹩浠紓鏍风殑鐩厜銆�"},{"end":223700,"start":220180,"text":"鍥犱负寰堝皯鏈夊勾杞荤敺浜猴紝澶х櫧澶╁湪灏忓尯閲屽甫濞�"},{"end":226730,"start":224030,"text":"瀹朵汉鐨勭溂鍏夈€備綔鑰呭憿锛屽﹩濠�"},{"end":232230,"start":226750,"text":"浼氭嬁璇濋鐐瑰埌缁欏皬浜戝効娲楁尽杩樻槸濂充汉鐨勬墜姣旇緝閫傚悎濂充汉鐨勬墜姣旇緝杞€�"},{"end":234950,"start":232530,"text":"浣滆€呯殑鐖哥埜浼氭暣澶滃け鐪狅紝"},{"end":239690,"start":235000,"text":"璐ㄩ棶灏忓か濡讳咯锛屽ス涓€涓ぇ鐢蜂汉鎬庝箞鑳藉ぉ澶╁憜鍦ㄥ閲屽甫瀛╁瓙鍛紵"},{"end":241500,"start":239990,"text":"鎯虫兂涔熸槸鍙互鐞嗚В锛�"},{"end":243480,"start":241780,"text":"鏉庢垚濞熷綋鍏ㄨ亴锛岀埜鐖�"},{"end":245010,"start":243480,"text":"鐜板湪琚緢澶氫汉鍦紝"},{"end":247070,"start":245330,"text":"浣嗗叾瀹炲垰寮€濮嬬殑鏃跺€�"},{"end":248580,"start":247090,"text":"涓嶄篃寰堝鎸囩偣鍚楋紝"},{"end":250650,"start":248720,"text":"浣犲湪瀹惰繕璁╀綘鐨勫吇浣狅紝"},{"end":252540,"start":250940,"text":"浣犲畨鍊嶈€佹湅鍙嬪吇浜嗗叚骞达紝"},{"end":258830,"start":252810,"text":"涓堟瘝濞樼湅鍒板ぉ澶╀笅鍘ㄥ仛楗究鎻愭潕瀹夛紝浣犺繖涔堜細鐑ц彍锛屾垜鎶曡祫缁欎綘寮€涓棣嗗惂銆�"},{"end":263290,"start":259110,"text":"鑰佷笀浜轰篃浠庡綋浼楁€掞紝瀵硅繖涔堝ぇ鐨勭敺浜猴紝鎬庝箞涓嶅幓鎵句唤宸ヤ綔锛�"},{"end":265300,"start":263450,"text":"闈犲瀛愬吇鎴愪綍浣撶粺锛�"},{"end":268060,"start":265650,"text":"鐗圭珛鐙灏辨槸姣旈殢娉㈤€愭祦鏇撮毦銆�"},{"end":272380,"start":268390,"text":"鍏跺疄娌℃湁浠€涔堟ā寮忔槸100%鐨勫ソ锛屽氨鎱㈡參鎽哥储锛�"},{"end":277350,"start":272720,"text":"鎻愬墠鎯冲ソ锛屽鏋滃埌鏃跺€欓亣鍒版柊闂锛屽啀鍐欓暱鏂囷紝璺熶綘浠垎浜�"},{"end":282940,"start":278170,"text":"鏅氬畨锛屾洿澶氭枃绔犲彲浠ュ叧娉ㄦ垜浠殑鍏彿锛岄€嗘祦鑰屼笂銆俓n"},{"end":284860,"start":282960,"text":"鍒樺氨鏄垬濯涘獩鐨勫垬锛�"}]'

# x = utf.encode("gbk").decode("utf-8", errors="ignore")
x = x.encode("GB18030").decode("utf-8", errors="ignore")
print(x)

s = '中国'
s_gb1 = s.encode('gb2312')
s_gb2 = s.encode('utf-8')
print(s_gb1)  # b'\xd6\xd0\xb9\xfa'
print(s_gb2)  # b'\xe4\xb8\xad\xe5\x9b\xbd'

#
# # utf-8,GBK 转 unicode 使用函数unicode(s,encoding) 或者s.decode(encoding)
s = u'上海'
s_utf8 = s.encode('UTF-8')  # 先将unicode 转 utf-8
print(s_utf8.decode('utf-8'))  # 上海
#
#
# # str 转 unicode
# s = '北京'  #因为s为所在的.py(# -*- coding=UTF-8 -*-)编码为utf-8
# s_unicode = s.decode('UTF-8')  # 将 utf-8 转 unicode
# print s_unicode  # 北京
# print s.decode('utf-8').encode('gb2312')  # ���� , s 先转 unicode 再转 gb2312
# # 如果直接执行s.encode('gb2312')会发生什么？
# # print s.encode('gb2312')  # UnicodeDecodeError: 'ascii' codec can't decode byte 0xe5 in position 0: ordinal not in range(128)
# # Python 会自动的先将 s 解码为 unicode ，然后再编码成 gb2312。因为解码是python自动进行的，我们没有指明解码方式，
# # python 就会使用 sys.defaultencoding 指明的方式来解码。很多情况下 sys.defaultencoding 是 ANSCII，如果 s 不是这个类型就会出错。
# # 拿上面的情况来说，我的 sys.defaultencoding 是 anscii，而 s 的编码方式和文件的编码方式一致，是 utf8 的，
# # 所以出错了: UnicodeDecodeError: 'ascii' codec can't decode byte 0xe4 in position 0: ordinal not in range(128)
# # 如：
# import sys
# reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
# sys.setdefaultencoding('utf-8')
# str = '中文'
# print str.encode('gb2312')  # ����
#
#
# # 文件编码与print函数
# # 建立一个文件test.txt，文件格式用ANSI，内容为: abc中文
# # text.py 内容如下：
# # coding=gbk
# # print open("Test.txt").read()
# # 结果：abc中文
# # 把文件格式改成UTF-8，结果：abc涓枃
# # 显然，这里需要解码：
# # coding=gbk
# import codecs
# # print open("Test.txt").read().decode("utf-8")
# # 结果：abc中文
# # 上面的test.txt我是用Editplus来编辑的，但当我用Windows自带的记事本编辑并存成UTF-8格式时，
# # 运行时报错：
# # Traceback (most recent call last):
# #   File "ChineseTest.py", line 3, in <module>
# #     print open("Test.txt").read().decode("utf-8")
# # UnicodeEncodeError: 'gbk' codec can't encode character u'/ufeff' in position 0: illegal multibyte sequence
# # 原来，某些软件，如notepad，在保存一个以UTF-8编码的文件时，会在文件开始的地方插入三个不可见的字符（0xEF 0xBB 0xBF，即BOM）。
# # 因此我们在读取时需要自己去掉这些字符，python中的codecs module定义了这个常量：
# # # coding=gbk
# # import codecs
# # data = open("Test.txt").read()
# # if data[:3] == codecs.BOM_UTF8:
# #   data = data[3:]
# # print data.decode("utf-8")
# # 结果：abc中文
#
#
#
# # 如果在python文件中指定编码方式为 utf-8(# coding=utf-8)，那么所有带中文的字符串都会被认为是utf-8编码的 byte string
# # （例如：mystr="你好"），
# # 但是在函数中所产生的字符串则被认为是 unicode string。
#
# # 问题就出在这边，unicode string和 byte string 是不可以混合使用的，一旦混合使用了，就会产生这样的错误。例如：
# # self.response.out.write("你好" + self.request.get("argu"))
# # 其中，"你好"被认为是byte string，而self.request.get("argu")的返回值被认为是unicodestring。
# # 由于预设的解码器是ascii，所以就不能识别中文bytestring。然后就报错了。
#
# # 以下有两个解决方法：
# # 1.将字符串全都转成byte string。
# # self.response.out.write("你好" + self.request.get("argu").encode("utf-8"))
# #
# # 2.将字符串全都转成unicode string。
# # self.response.out.write(u"你好" + self.request.get("argu"))
# # bytestring转换成unicode
# # string可以这样转unicode(unicodestring, "utf-8")
#
# # python中包含UTF-8编码中文的列表或字典的输出  https://segmentfault.com/a/1190000002447836
# dict = {"abcd123": "测试学习"}
# print dict   # {'abcd123': '\xe6\xb5\x8b\xe8\xaf\x95\xe5\xad\xa6\xe4\xb9\xa0'}
# list = ["人民解放军", "12", 0]  # ['\xe4\xba\xba\xe6\xb0\x91\xe8\xa7\xa3\xe6\x94\xbe\xe5\x86\x9b', '12', 0]
# print list
# list = [u"人民解放军", "12", 0] # [u'\u4eba\u6c11\u89e3\u653e\u519b', '12', 0]
# print list
#
# # 格式化输出
# import json
# print json.dumps(dict, encoding="UTF-8", ensure_ascii=False)  # {"abcd123": "测试学习"}
# print json.dumps(list, encoding="UTF-8", ensure_ascii=False)  # ["人民解放军", "12", 0]
#
# # Python encode() 方法以 encoding 指定的编码格式编码字符串。errors参数可以指定不同的错误处理方案。
# # 字符串的话直接用 encode("utf-8")
#
# str = u"中国"
# print str  # 中国
#
# # 将 字符串 转 base64
# str = "this is string example....wow!!!"
# print str.encode("base64", 'strict')  # 中国
#
#
# # ======================================================================================
# # 2、[python]去掉 unicode 字符串前面的 u
# # https://mozillazg.com/2013/12/python-raw-unicode.html
# # unicode.encode('raw_unicode_escape')
# print "~~~~~~~"
# a = ['你好']
# print a
# print u"你好".encode('raw_unicode_escape')
# print u'\xe4\xbd\xa0\xe5\xa5\xbd'.encode('raw_unicode_escape')
# print u'\xe4\xbd\xa0\xe5\xa5\xbd'.encode('raw_unicode_escape').decode('utf8')   # u'\u4f60\u597d'
# print u'\u4f60\u597d'
# str2='\u91d1\u91d1 \u7ed9\u60a8\u53d1\u73b0\u91d1\u7ea2\u5305\u5566\uff010.20\u5143\u7ea2\u5305\u7b49\u5927\u5bb6\u6765\u62a2\uff0c\u62a2\u5230\u5c31\u80fd\u63d0\u73b0\u54e6~'
# print str2.decode('unicode_escape')
# print "!!!!!!!!"
#
#
# # ======================================================================================
# # 3、关于python编码的文章，http://blog.csdn.net/liuxincumt/article/details/8183391
#
# # ======================================================================================
# # 4、普通字符串可以用多种方式编码成Unicode
# # Description: Python如何将Unicode中文字符串转换成 string字符串
# # http://python.jobbole.com/81244/
# unicodestring = u"Hello world"
# # 将Unicode转化为普通Python字符串："encode"
# utf8string = unicodestring.encode("utf-8")
# asciistring = unicodestring.encode("ascii")
# isostring = unicodestring.encode("ISO-8859-1")
# utf16string = unicodestring.encode("utf-16")
# print utf8string
# print asciistring
# print isostring
# print utf16string
#
#
# # 将普通Python字符串转化为Unicode："decode"
# plainstring1 = unicode(utf8string, "utf-8")
# plainstring2 = unicode(asciistring, "ascii")
# plainstring3 = unicode(isostring, "ISO-8859-1")
# plainstring4 = unicode(utf16string, "utf-16")
# print plainstring1
# print plainstring2
# print plainstring3
# print plainstring4
#
#
# # ======================================================================================
# # 5、自动编码转换
# stri = "金浩"
# def zh2unicode(stri):
#    """Auto converter encodings to unicode
#    It will test utf8,gbk,big5,jp,kr to converter"""
#    for c in ('utf-8', 'gbk', 'big5', 'jp', 'euc_kr', 'utf16', 'utf32'):
#        try:
#             return stri.decode(c)
#        except:
#             pass
#    return stri
# print zh2unicode(stri)
#
#
# # 6、自动识别是unicode还是utf-8
# # s = u"中文"
# s = "中文"
# if isinstance(s, unicode):
#    #s=u"中文"
#    print s.encode('utf-8')
#    print "1111"
# else:
#    #s="中文"
#    print s.decode('utf-8').encode('utf-8')
#    print "2222"
#
# # ======================================================================================================================
# #  python raw-input odd behavior with accents containing strings
# # 它是将终端的输入编码通过decode转换成unicode编码
# # https://stackoverflow.com/questions/11068581/python-raw-input-odd-behavior-with-accents-containing-strings
# # To read a unicode string in, you need to realise that raw_input gives you a bytestring - so, you need to convert it
# # using its .decode method. You need to pass .decode the encoding of your STDIN - which is available as sys.stdin.encoding
# #  (don't just assume that this is UTF8 - it often will be, but not always) - so, the whole line will be:
# # string = raw_input(...).decode(sys.stdin.encoding)
# # But by far the easiest way around this is to upgrade to Python 3 if you can - there, input() (which behaves like the
# # Py2 raw_input otherwise) gives you a unicode string (it calls .decode for you so you don't have to remember it), and
# # unprefixed strings are unicode strings by default. Which all makes for a much easier time working with accented characters
# # - it essentially implies that the logic you were trying would just work in Py3, since it does the right thing.
# # Note, however, that the error you're seeing would still manifest in Py3 - but since it does the right thing by default,
# # you have to work hard to run into it. But if you did, the comparison would just be False, with no warning - Py3 doesn't
# # ever try to implictly convert between byte and unicode strings, so any byte string will always compare unequal to any
# # unicode string, and trying to order them will throw an exception.
#
# varProductName = raw_input(unicode('\n请输入产品名称：', 'utf-8').encode('gbk')).decode(sys.stdin.encoding)
# print type(varProductName)  # <type 'unicode'>
#
# # ======================================================================================================================
# # 从cmd中输入中文传入python，如下
#
# unicode(varValue, 'gbk')
#
# https://blog.csdn.net/eastmount/article/details/48841593