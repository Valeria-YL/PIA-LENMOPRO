import pymysql

def getDBConnection():
    connection = pymysql.connect(
        host='localhost',         
        user='root',    
        password='Mypassword', 
        database='musicaPIA'  
    )
    return connection