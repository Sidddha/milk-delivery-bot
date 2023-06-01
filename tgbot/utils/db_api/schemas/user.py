from sqlalchemy import Column, BigInteger, String, sql, Integer, ARRAY
from tgbot.utils.db_api.db_gino import TimedBaseModel

    
class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    phone = Column(Integer)
    status = Column(String(15))
    address = Column(String(150))
    geo = Column(ARRAY(String))

    @property
    def latitude(self):
        return self.coordinates[0]

    @property
    def longitude(self):
        return self.coordinates[1]

    query: sql.Select