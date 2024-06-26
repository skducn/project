# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2022-5-25
# Description: # orm 对象关系映射
# https://blog.csdn.net/weixin_46220599/article/details/124470724
# python 制作一个简单的orm框架
# 支持insert, update, select, delete操作
# 支持全表查询，全表删除，删除表操作
# 如需更复杂的sql操作，框架支持直接运行sql
# *****************************************************************

from copy import deepcopy

class Field(object):
        def __init__(self, name, ctype, *attrs):
                self._name = name
                self._ctype = ctype
                self._attrs = attrs

        @property
        def name(self):
                return self._name

        @property
        def ctype(self):
                return self._ctype

        @property
        def attrs(self):
                return self._attrs

class ModelMetaclass(type):
        def __new__(cls, name, based, attrs):
                if name == 'Model':
                        return type.__new__(cls, name, based, attrs)
                argsList = dict()
                for k, v in attrs.items():
                        if isinstance(v, Field):
                                argsList[k] = v
                for k in argsList.keys():
                        attrs.pop(k)
                attrs['__mapping__'] = argsList
                attrs['__table__'] = name
                attrs['__mapping_size__'] = len(argsList)
                return type.__new__(cls, name, based, attrs)

class Model(dict, metaclass = ModelMetaclass):
        def set(self, values):
                for i in range(len(self.__mapping__.keys())):
                        key = list(self.__mapping__.keys())[i]
                        self[key] = values[i]
                return self

        def create(self, cursor):
                ans = 'create table %s (' %self.__table__
                primaryKeys = []
                columns = []
                cnt = 0
                for k, v in self.__mapping__.items():
                        ans += v.name +' ' + v.ctype
                        for attr in v.attrs:
                                if attr == 'primary key':
                                        primaryKeys.append(v.name)
                                else:
                                        ans += ' ' + attr
                        cnt += 1
                        if cnt != self.__mapping_size__:
                                ans += ','
                if len(primaryKeys) != 0:
                        ans += ',primary key ('
                        cnt = 0
                        for key in primaryKeys:
                                ans += key
                                cnt += 1
                                if cnt != len(primaryKeys):
                                        ans += ','
                        ans += ')'
                ans += ')'
                cursor.execute(ans)
                return self

        def insert(self, cursor):
                columns = []
                values = []
                for k, v in self.__mapping__.items():
                        columns.append(v.name)
                        if 'primary key' in v.attrs and self[k] == '':
                                raise ValueError('primary key is empty')
                        if 'int' in v.ctype or 'float' in v.ctype or 'double' in v.ctype or 'decimal' in v.ctype:
                                values.append(str(self[k]))
                        else:
                                values.append('\'' + self[k] + '\'')
                cursor.execute('insert into %s (%s) values (%s)' %(self.__table__, ','.join(columns), ','.join(values)))
                return self

        def select(self, cursor):
                ans = 'select * from %s where ' %self.__table__
                columns = []
                values = []
                pstr = []
                for k, v in self.__mapping__.items():
                        columns.append(v.name)
                        if 'primary key' in v.attrs:
                                if self[k] == '':
                                        raise ValueError('primary key is empty')
                                if 'int' in v.ctype or 'float' in v.ctype or 'double' in v.ctype or 'decimal' in v.ctype:
                                        pstr.append(v.name + ' = ' + str(self[k]))
                                else:
                                        pstr.append(v.name + ' = \'' + self[k] + '\'')
                for i in range(len(pstr)):
                        ans += pstr[i]
                        if i != len(pstr) - 1:
                                ans += 'and '
                cursor.execute(ans)
                values = cursor.fetchall()
                for i in range(len(self.__mapping__.keys())):
                        self[list(self.__mapping__.keys())[i]] = values[0][i]
                return self

        def update(self, cursor):
                ans = 'update %s set ' %self.__table__
                pstr = []
                for k, v in self.__mapping__.items():
                        if 'primary key' in v.attrs:
                                if 'int' in v.ctype or 'float' in v.ctype or 'double' in v.ctype or 'decimal' in v.ctype:
                                        pstr.append(v.name + ' = ' + self[k])
                                else:
                                        pstr.append(v.name + ' = \'' + self[k] + '\'')
                        else:
                                if 'int' in v.ctype or 'float' in v.ctype or 'double' in v.ctype or 'decimal' in v.ctype:
                                        ans += '%s = %s, '%(v.name, str(self[k]))
                                else:
                                        ans += '%s = \'%s\', '%(v.name, self[k])
                ans = ans[:-2]
                ans += ' where '
                for i in range(len(pstr)):
                        ans += pstr[i]
                        if i != len(pstr) - 1:
                                ans += 'and '
                cursor.execute(ans)
                return self

        def delete(self, cursor):
                ans = 'delete from %s where ' %self.__table__
                columns = []
                values = []
                pstr = []
                for k, v in self.__mapping__.items():
                        columns.append(v.name)
                        if 'primary key' in v.attrs:
                                if self[k] == '':
                                        raise ValueError('primary key is empty')
                                if 'int' in v.ctype or 'float' in v.ctype or 'double' in v.ctype or 'decimal' in v.ctype:
                                        pstr.append(v.name + ' = ' + str(self[k]))
                                else:
                                        pstr.append(v.name + ' = \'' + self[k] + '\'')
                for i in range(len(pstr)):
                        ans += pstr[i]
                        if i != len(pstr) - 1:
                                ans += 'and '
                cursor.execute(ans)
                return self

class Database(object):
        def __init__(self, conn):
                self._conn = conn
                self._cursor = self._conn.cursor()

        def commit(self):
                self._conn.commit()

        def close(self):
                self._cursor.close()
                self._conn.close()

        @property
        def cursor(self):
                return self._cursor

        def insert(self, *models):
                for model in models:
                        model.insert(self.cursor)

        def create(self, *models):
                for model in models:
                        model.create(self.cursor)

        def update(self, *models):
                for model in models:
                        model.update(self.cursor)

        def delete(self, *models):
                for model in models:
                        model.delete(self.cursor)

        def select(self, *models):
                for model in models:
                        model.select(self.cursor)

        def deleteAll(self, model):
                self.cursor.execute('delete from ' + model.__table__)

        def drop(self, model):
                self.cursor.execute('drop table ' + model.__table__)

        def dropIf(self, model):
                self.cursor.execute('drop table if exists ' + model.__table__)

        def selectAll(self, model):
                self.cursor.execute('select * from ' + model.__table__)
                values = self.cursor.fetchall()
                ans = []
                for item in values:
                        temp = deepcopy(model)
                        temp.set(item)
                        ans.append(temp)
                return ans

        def execute(self, sql):
                self.cursor.execute(sql)
                return self.cursor.fetchall()
