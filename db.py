import pymysql

class DBConnection:
	def __init__(self,host,user,password,database,charset,port):
		self.connection = pymysql.connect(
			host=host,
			user=user,
			password=password,
			db=database,
			charset=charset,
			port=port,
			cursorclass=pymysql.cursors.DictCursor)

	def exec_insert_request_dust(self,sess,kind,keyword,result,trace): 
		query = Query().get_insert_request_dust(sess,kind,keyword,result,trace) 
		with self.connection as cur:
			cur.execute(query)

	def exec_select_response_dust(self,sess,kind,keyword,area02):
		with self.connection.cursor() as cursor:
			query = Query().get_select_response_dust(sess,kind,keyword,area02)
			cursor.execute(query)
			for row in cursor:
				data = row.get('cnt')
		return data	

	def exec_insert_response_dust(self,sess,kind,mdate,area01,area02,so2,co,o3,no2,pm10,pm25): 
		query = Query().get_insert_response_dust(sess,kind,mdate,area01,area02,so2,co,o3,no2,pm10,pm25) 
		with self.connection as cur:
			cur.execute(query)						

	def close(self):
		self.connection.close()

	def commit(self):
		self.connection.commit()

class Query:

	def get_insert_request_dust(self,sess,kind,keyword,result,trace):
		query = 'insert into request_dust (sess,kind,keyword,result,trace) \
		values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(sess,kind,keyword,result,trace)
		#print('qery:',query)
		return query	

	def get_select_response_dust(self,sess,kind,keyword,area02):
		query = 'select \
		count(*) as cnt \
		from response_dust \
		where sess=\'{}\' and kind=\'{}\' and area01=\'{}\' and area02=\'{}\''.format(sess,kind,keyword,area02)
		return query

	def get_insert_response_dust(self,sess,kind,mdate,area01,area02,so2,co,o3,no2,pm10,pm25):
		query = 'insert into response_dust (sess,kind,mdate,area01,area02,so2,co,o3,no2,pm10,pm25) \
		values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(sess,kind,mdate,area01,area02,so2,co,o3,no2,pm10,pm25)
		return query