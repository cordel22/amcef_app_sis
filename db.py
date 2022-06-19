##### this module creates an empty database it there is none

##### or connects to an existing one


from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# connect with the data base or create it if soesn't exist
engine = create_engine('sqlite:///db.sqlite', echo=True)
# manage tables
base = declarative_base()

# def db_connect():

# class Posts creates an object of a row in 'posts' database
class Posts(base):
    __tablename__ = 'posts'

    
    user_id = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True)
    title = Column(String, primary_key=True)
    
    body = Column(String, primary_key=True)
    date = Column(DateTime, primary_key=True)

    def __init__ (self, user_id, id, title, body):

        self.user_id = user_id
        self.id = id
        self.title = title
        self.body = body
        self.date = datetime.now()

# ceate data base and tables

base.metadata.create_all(engine)

