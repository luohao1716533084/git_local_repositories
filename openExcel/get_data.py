#coding:utf-8

from functools import reduce
from pandas_excel import *
from sheet_cols import *
import os

class getDataSheet():
    def __init__(self, excel_dict):
        self.excel_dict = excel_dict
        self.index = excel_dict['index']

    def getExcelPath(self,):
        # 获取当前文件夹所有文件路径
        current_path = os.getcwd()
        file_path_list = []
        for root, dirs, files in os.walk(current_path):
            for name in files:
                file_path_list.append(os.path.join(root, name))
        #匹配文件名关键字，返回包含关键字的文件路径
        excelName = self.excel_dict['excelName']
        res = []
        for i in file_path_list:
            if excelName in i:
                res.append(i)
        return res

    def get_sheet_data(self, excelPath):
        sheetName, columns_list, n, flag = self.excel_dict['sheetName'], self.excel_dict['cols'], self.excel_dict['n'], self.excel_dict['flag']
        dataframe = OpenExcel(excelPath, sheetName, columns_list)
        if flag == "A":
            df = dataframe.pre_process_typeA(n)
        else:
            df = dataframe.pre_process_typeB(n)
        return df
    
    def get_sheet_data_csv(self, csvPath):
        columnsList = self.excel_dict['cols']
        df = pd.read_csv(csvPath, encoding="gb18030")
        return df[columnsList]
    
    def getConcatDataCsv(self,):
        pathList = self.getExcelPath()
        if len(pathList) == 1:
            res = self.get_sheet_data_csv(pathList[0])
        elif len(pathList) == 0:
            print("缺失: %s " % self.excel_dict['sheeName'])
        else:
            dfList = []
            for path in pathList:
                dfList.append(self.get_sheet_data_csv(path))
            res =  pd.concat(dfList, ignore_index=True)
        # if 'index' in res.columns.to_list() and not self.index:
        #     res.drop(columns='index', inplace=True)
        return res.reset_index()
        
    # 通过已经定义好的表结构的字典，获取excel data
    # 包括tpyeA，typeB类的表，以及合并表的操作。
    # 最终获取合并表的数据。
    def getConcatData(self,):
        pathList = self.getExcelPath()
        if len(pathList) == 1:
            res = self.get_sheet_data(pathList[0])
        elif len(pathList) == 0:
            print("缺失:(%s) " % self.excel_dict['sheetName'] )
        else:
            dfList = []
            for path in pathList:
                dfList.append(self.get_sheet_data(path))
            res = pd.concat(dfList, ignore_index=True)
        if 'index' in res.columns.to_list() and not self.index:
            res.drop(columns='index', inplace=True)
        return res
    

    # def reColName(self, df):
    #     df.columns = self.excel_dict['colsAlias']
    #     return df
    
    #增加"邻区关系"列
    def getNcellRelationCols(self, df, dx=False):
        df["邻区关系"] = ''
        if dx:
            count = 0
            for eNBid, Id in zip(df['nbrEnbId'], df['nbrCellId']):
                df.loc[count, "邻区关系"] = str("0:460:11:") + str(eNBid) + str(":") + str(Id) 
                count += 1
        else:
            count = 0
            for mcc, mnc, eNBid, Id in zip(df['nbrMCC'], df['nbrMNC'], df['nbrEnbId'], df['nbrCellId']):
                df.loc[count,"邻区关系"] = str("0:") + str(mcc) + ":" + str(mnc) + ":" + str(eNBid) + ":" + str(Id)
                count += 1
        return df
    
    def getECI(self, df, lst):
        df['ECI'] = ''
        count = 0
        for eNBid, Id in zip(df[lst[0]], df[lst[1]]):
            df.loc[count, "ECI"] = str("0:460:11:") + str(eNBid) + str(":") + str(Id) 
            count += 1
        return df
        