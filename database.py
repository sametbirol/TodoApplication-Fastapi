from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# your SQLAlchemy Database URL go here
# URL = postgresql://postgres:PASSWORD@localhost/DATABASENAME
SQLALCHEMY_DATABASE_URL = ""


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush= False, bind=engine)

Base =declarative_base()