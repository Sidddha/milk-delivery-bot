from sqlalchemy import Column, BigInteger, String, sql, Integer
from tgbot.utils.db_api.db_gino import TimedBaseModel
from sqlalchemy.dialects import postgresql

    
class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    phone = Column(Integer)
    status = Column(String(15))
    address = Column(String(150))
    geo = Column(postgresql.POINT())

    @property
    def latitude(self):
        return self.coordinates[0]

    @property
    def longitude(self):
        return self.coordinates[1]

    query: sql.Select