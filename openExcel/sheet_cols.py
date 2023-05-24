#coding:utf-8

# 输出表说明:
import os

"""
n值说明:
case1:当表类型为A时,需要删除的行数等于n;
case2:当表类型为B时,且为标准表时,n等于0;
case3:当表类型为B是,且首行(列名)与数据行有n行的间隔时,n等于n+1;
"""



dic = {
    'excelName': '昆明电信800M开共享清单（区块链取数4月13日）联通反馈关闭共享',
    'sheetName': 'sheet1',
    'cols': ['基站ID', '小区名称'],
    'n': 0,
    'flag': 'B',
    'index': True
}
