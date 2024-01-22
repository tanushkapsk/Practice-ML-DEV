from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine, Column, Integer, LargeBinary, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pickle

from app.db.base import Base


class TableML(Base):
    __tablename__ = "table_ml"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    file_path = Column(String)
