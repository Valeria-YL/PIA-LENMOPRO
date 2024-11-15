import cryptography
import pymysql

def getDBConnection():
    connection = pymysql.connect(
        host='mysql',         
        user='root',    
        port=3396,
        password='Mypassword', 
        database='musicaPIA'  
    )
    return connection