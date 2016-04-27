from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

engine = create_engine('sqlite:///db.sqlite')

Base = declarative_base()


class Tile(Base):
    __tablename__ = 'tiles'
    id = Column(Integer, primary_key=True)

    x = Column(Integer)
    y = Column(Integer)
    temperature = Column(Float)
    precipitation = Column(Float)
    windspeed = Column(Float)

    _n = Column(Integer, ForeignKey('tiles.id'))
    n = relationship('Tile', foreign_keys=[_n], uselist=False, backref=backref('s', uselist=False, remote_side=[id]))

    _ne = Column(Integer, ForeignKey('tiles.id'))
    ne = relationship('Tile', foreign_keys=[_ne], uselist=False, backref=backref('sw', uselist=False, remote_side=[id]))

    _e = Column(Integer, ForeignKey('tiles.id'))
    e = relationship('Tile', foreign_keys=[_e], uselist=False, backref=backref('w', uselist=False, remote_side=[id]))

    _se = Column(Integer, ForeignKey('tiles.id'))
    se = relationship('Tile', foreign_keys=[_se], uselist=False, backref=backref('nw', uselist=False, remote_side=[id]))

    @property
    def coord(self):
        return tuple([self.x, self.y])

    @property
    def adjacents(self):
        return [self.nw, self.n, self.ne, self.e, self.se, self.s, self.sw, self.w]


Base.metadata.create_all(engine)

