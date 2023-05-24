#coding:utf-8

import pandas as pd


class OpenExcel:
	def __init__(self, excel_path, sheetName, col_list):
		self.path = excel_path
		self.sheetName = sheetName
		self.col_list = col_list
		
		self.df = pd.read_excel(self.path, sheet_name=None)
		sheetNamelst = list(self.df.keys())
		self.tmp = []
		for i in sheetNamelst:
			if self.sheetName in i:
				self.tmp.append(i)

	"""
	1.删除sheet前n行无效行,同时定义第n+1行为列名。
	2.指标导出类表,使用该方法
	"""
	def pre_process_typeA(self, n):
		lst = []
		for i in self.tmp:
			tmp_df = pd.read_excel(self.path, self.sheetName, header=n)              #自动默认第n行为列名，同时默认第n+1行开始为数据行
			lst.append(tmp_df[self.col_list])
		res = pd.concat(lst)
		return res

	"""
	1.选取第n行开始为数据行,同时使用第一行为列名
	2.参数导出类表,使用该方法
	"""
	def pre_process_typeB(self, n):
		lst = []
		for i in self.tmp:
			tmp_df = pd.read_excel(self.path, sheet_name=i)
			lst.append(tmp_df.iloc[n:][self.col_list])
		res = pd.concat(lst, ignore_index=True)
		return res.reset_index()

class WriteToExcel:
	def __init__(self, listTuple, colName, sheetName):
		self.listTuple = listTuple
		self.colName = colName
		self.sheetName = sheetName

	def writeExcel(self,):
		df = pd.DataFrame(self.listTuple)
		df.columns = self.colName
		df.to_excel("result.xlsx", sheet_name=self.sheetName, index=False)

	
	