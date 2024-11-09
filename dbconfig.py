
import pymysql

def getDBConnection():
    connection = pymysql.connect(
        host='localhost',         
        user='root',    
        port=3306,
        password='Mypassword', 
        database='musicaPIA'  
    )
    return connection