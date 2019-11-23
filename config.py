
'''
CREATE TABLE request_dust (
  num int(11) NOT NULL AUTO_INCREMENT,
  sess varchar (50) NOT NULL,  
  kind varchar(50) DEFAULT '-',
  keyword varchar(100) DEFAULT '-',
  result varchar(50) DEFAULT '-',
  trace varchar(100) DEFAULT '-',
  rdate datetime DEFAULT NOW(),
  primary key (num)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

CREATE TABLE response_dust (
  num int(11) NOT NULL AUTO_INCREMENT,
  sess varchar (50) NOT NULL,  
  kind varchar(50) DEFAULT '-',
  mdate varchar(20) DEFAULT '-',
  area01 varchar(50) DEFAULT '-',
  area02 varchar(50) DEFAULT '-',
  so2 varchar(10) DEFAULT '-',
  co varchar(10) DEFAULT '-',
  o3 varchar(10) DEFAULT '-',
  no2 varchar(10) DEFAULT '-',
  pm10 varchar(10) DEFAULT '-',
  pm25 varchar(10) DEFAULT '-',
  rdate datetime DEFAULT NOW(),
  primary key (num)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

END'''

class Configuration:

  def get_configuration(choose):

    if(choose == 'local'):
      connect_value = dict(host='HOSTNAME',
        user='USERID',
        password='PASSWORD',
        database='DATABASE',
        port=3307,
        charset='utf8')
      
    elif(choose == 'ubuntu'):
      connect_value = dict(host='HOSTNAME',
        user='USERID',
        password='PASSWORD',
        database='DATABASE',
        port=3307,
        charset='utf8')

    else:
      print('Not Selected')
      connect_value = ''

    return connect_value
  