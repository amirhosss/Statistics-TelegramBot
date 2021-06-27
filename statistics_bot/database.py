import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create engine
DATABASE_URL = os.environ.get('DATABASE_URL').replace('postgres', 'postgresql')
engine = create_engine(DATABASE_URL, 
                       echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()