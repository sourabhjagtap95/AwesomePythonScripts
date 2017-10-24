import MySQLdb
def connect():
    try:
    	db = MySQLdb.connect(host="localhost",user="Database User Name",passwd="Database Passsword",db="Database Name")
    	cur = db.cursor()
     	return db,cur
    except:
        return 'Authenticaion Failed!'
