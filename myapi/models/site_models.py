from myapi.app import session, engine, Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class Configuration(Base):
    __tablename__ = 'configuration'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    spotify_code = Column(String)
    spotify_access_token = Column(String)
    spotify_refresh_token = Column(String)
    snap_client_id = Column(String)

    def __repr__(self):
        return  "<Configuration(name='%s', id='%s')>" % (self.name, self.id)
