from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://user:password@localhost:5432/postgres'

engine = create_engine(SQLALCHEMY_DATABASE_URL)#starting up

SessionLocal = sessionmaker(autocommit=False,autoflush = False,bind=engine) #use for creating sessions

Base = declarative_base() #creating table by using class

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()