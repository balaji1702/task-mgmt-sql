# IMPORT THE SQALCHEMY LIBRARY's CREATE_ENGINE METHOD
from sqlalchemy import create_engine
  
# DEFINE THE DATABASE CREDENTIALS
user = 'root'
password = 'balaji1702'
host = '127.0.0.1'
port = 3306
database = 'To_Do'
  
# PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT
def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )
  
  
engine= get_connection()
connection=engine.connect()
