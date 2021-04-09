from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Config:
    def __init__(self, connection, **kwargs):
        self.__engine = create_engine(connection, **kwargs)
        self.Base = declarative_base()
        Session = sessionmaker(bind=self.__engine)
        self.session = Session()

    def init(self):
        self.Base.metadata.create_all(self.__engine)


db = Config("sqlite:///test.db", echo=False)
