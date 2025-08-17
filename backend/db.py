from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base,sessionmaker
import os

DATABASE_URL=os.getenv("DATABASE_URL", "sqlite:///./users.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base= declarative_base()

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,index=True)
    hashed_password=Column(String,nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)