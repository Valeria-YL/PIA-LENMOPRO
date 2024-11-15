import cryptography
import pymysql

def getDBConnection():
    connection = pymysql.connect(
        host='mysql',         
        user='root',    
        port=30278,
        password='Mypassword', 
        database='musicaPIA'  
    )
    return connection