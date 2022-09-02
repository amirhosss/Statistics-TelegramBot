import os

import config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create engine
engine = create_engine(config.DATABASE_URL, 
                       echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
