# -*- coding: utf-8 -*- 

import os, glob
import requests
import time
import datetime
import sys
from config import Configuration
from db import DBConnection,Query
from xml.etree import ElementTree as et
import uuid

class Searchdust:

	def __init__(self,keyword,platform):
		#print('init')
		self.keyword = keyword
		self.platform = platform

	def set_params(self):
		#print('set_params')
		self.keyword = sys.argv[1]
		self.platform = sys.argv[2]

	def validate(self):
		default	= {
			'keyword':'서울',
			'platform':'local'
		}

		self.keyword = default.get('keyword')	if self.keyword == '' else self.keyword
		self.platform = default.get('platform')	if self.platform == '' else self.platform.lower()			

	def table_dust(self,vaule):
		if vaule == '-':
			result = '-'
		else:
			if int(vaule) < 16:
				result = '좋음'
			elif int(vaule) > 16 and int(vaule) < 36:
				result = '보통'
			elif int(vaule) > 36 and int(vaule) < 78:
				result = '나쁨'
			elif int(vaule) > 78:
				result = '매우나쁨'
			else:
				result = '-'

		return result		
		
	def openapi(self):
		self.validate()

		try:
			
			configuration = Configuration.get_configuration(self.platform)
			_host = configuration['host']
			_user = configuration['user']
			_password = configuration['password']
			_database = configuration['database']
			_port = configuration['port']
			_charset = configuration['charset']

			conn = DBConnection(host=_host,
				user=_user,
				password=_password,
				database=_database,
				port=_port,
				charset=_charset)

			now = time.localtime()

			sess = uuid.uuid1() # or uuid.uuid4()

			url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey=SERVICEKEY'

			rtime = []
			city = []
			so2 = []
			co = []
			o3 = []
			no2 = []
			pm10 = []
			pm25 = []	

			location = {
						'1':'서울',
						'2':'부산',
						'3':'대구',
						'4':'인천',
						'5':'광주',
						'6':'대전',
						'7':'울산',
						'8':'경기',
						'9':'강원',
						'10':'충북',
						'11':'충남',
						'12':'전북',
						'13':'전남',
						'14':'경북',
						'15':'경남',
						'16':'제주',
						'17':'세종',
						}
				
			rows = '40'
			sido = location[self.keyword]
			#print('sido:',sido)

			page = '1'
			srch = 'HOUR'

			params = {'numOfRows': rows, 'pageNo': page, 'sidoName': sido, 'searchCondition': srch}

			print('params:',params)

			kind = 'dust'

			keyword = self.keyword

			trace = 'python'

			response = requests.get(url, params=params)

			directory = '/home/ubuntu/searchdust/xml/'

			filename = '{}dust.xml'.format(directory)

			with open(filename,'w') as file:
				file.write(response.text)
			
			tree = et.parse(filename)
			root = tree.getroot()

			for response in root:
				for header in response:
					if header.tag == 'resultCode':
						_resultCode = header.text

			for response in root:
				for body in response:
					if body.tag == 'totalCount':
						_totalCount = body.text

			for response in root:
				for body in response:
					for items in body:
						for item in items:
							if item.tag == 'dataTime':
								rtime.append(item.text)
								#print(item.text)
							elif item.tag == 'cityName':
								city.append(item.text)
								#print(item.text)
							elif item.tag == 'so2Value': #아황산가스
								so2.append(item.text)
								#print(item.text)
							elif item.tag == 'coValue': #일산화탄소
								co.append(item.text)
								#print(item.text)
							elif item.tag == 'o3Value': #오존
								o3.append(item.text)
								#print(item.text)
							elif item.tag == 'no2Value': #이산화질소
								no2.append(item.text)
								#print(item.text)
							elif item.tag == 'pm10Value': #미세먼지
								pm10.append(item.text)
								#print(item.text)
							elif item.tag == 'pm25Value': #미세먼지
								pm25.append(item.text)
								##print(item.text)


			print(sess,_resultCode,_totalCount)

			result = _resultCode

			conn.exec_insert_request_dust(sess,kind,sido,result,trace)	

			if int(_totalCount) > int(rows):
				_totalCount = rows

			for i in range(0,int(_totalCount)):

				cnt = conn.exec_select_response_dust(sess,kind,sido,city[i])

				if cnt:
					print('overlap seq: ',i,cnt)
				else:	
					print('does not overlap seq: ',i,cnt)

					#print(sess,kind,rtime[0],sido,city[0],so2[0],co[0],o3[0],no2[0],pm10[0],pm25[0])

					conn.exec_insert_response_dust(sess,kind,rtime[i],sido,city[i],so2[i],co[i],o3[i],no2[i],pm10[i],pm25[i])
	
		except Exception as e:
			with open('./searchdust.log','a') as file:
				file.write('{} You got an error: {}\n'.format(datetime.datetime.now().strtime('%Y-%m-%d %H:%M:%S'),str(e)))

def run():
	searchdust = Searchdust('','')
	searchdust.set_params()
	searchdust.openapi()

if __name__ == "__main__":
	run()
