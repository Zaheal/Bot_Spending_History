from .models import *

from sqlalchemy.orm import Session
from sqlalchemy import create_engine

engine = create_engine("sqlite:///database/database.db")
Base.metadata.create_all(bind=engine)
session = Session(engine)
