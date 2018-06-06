import MySQLdb

def connection():
	conn = MySQLdb.connect(host="localhost", user = "root", 
						passwd = "shazam62", db = "pear")

	c = conn.cursor()

	return c, conn