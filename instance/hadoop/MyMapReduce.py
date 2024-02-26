# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-2-26
# Description: Python3调用Hadoop MapReduce API
# https://blog.csdn.net/agurt80004/article/details/101136785

# pip3 install mrjob -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

# hadoop fs -chown -R hadoop:hadoop  /tmp    #在执行MapReduce任务的时候hadoop用户会创建socket，通过jdbc访问。所以在执行你写得MapReduce之前一定要设置权限

# python3版wordCount
# python /MyMapReduce.py /a.txt -r hadoop  #在Hadoop集群，执行Python的MapReduce任务。


from mrjob.job import MRJob
import re

class MRwordCount(MRJob):
    '''
        line:一行数据
        (a,1)(b,1)(c,1)
        (a,1)(c1)
        (a1)
       '''
    def mapper(self, _, line):
        pattern=re.compile(r'(\W+)')
        for word in re.split(pattern=pattern,string=line):
            if word.isalpha():
                yield (word.lower(),1)


    def reducer(self, word, count):
        #shuff and sort 之后
        '''
        (a,[1,1,1])
        (b,[1])
        (c,[1])
        '''
        l=list(count)
        yield (word,sum(l))

if __name__ == '__main__':
    MRwordCount.run() #run()方法，开始执行MapReduce任务。