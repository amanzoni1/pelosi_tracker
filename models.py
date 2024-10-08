# models.py
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from utils import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=False)
    subscription_status = Column(String(20), default='inactive')  # 'active', 'inactive', 'canceled'
    subscription_start = Column(DateTime)
    subscription_end = Column(DateTime)

    def __repr__(self):
        return f'<User {self.email}>'

# Create tables
Base.metadata.create_all(bind=engine)