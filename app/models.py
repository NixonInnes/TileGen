from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from collections import namedtuple

engine = create_engine('sqlite:///db.sqlite')
Base = declarative_base()
Point = namedtuple('Point', ['x', 'y'])


class Plane(Base):
    __tablename__ = 'planes'
    id = Column(Integer, primary_key=True)

    name = Column(String)

    def __repr__(self):
        return '<Plane id: %s>' % self.id


class Tile(Base):
    __tablename__ = 'tiles'
    id = Column(Integer, primary_key=True)

    _plane = Column(Integer, ForeignKey('planes.id'))
    plane = relationship

    x = Column(Integer, index=True)
    y = Column(Integer, index=True)
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
        return Point(self.x, self.y)

    @property
    def adjacents(self):
        return {'nw': self.nw,
                'n': self.n,
                'ne': self.ne,
                'e': self.e,
                'se': self.se,
                's': self.s,
                'sw': self.sw,
                'w': self.w}

    def __repr__(self):
        return '<Tile id: %s, coord: (%s,%s)>' % (self.id, self.x, self.y)


Base.metadata.create_all(engine)
