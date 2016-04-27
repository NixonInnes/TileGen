from sqlalchemy.orm import sessionmaker
from . import models

Session = sessionmaker(bind=models.engine)
session = Session()
