from . import session
from .models import Tile
from random import uniform
from collections import deque
from sqlalchemy import and_


def make_zero():
    if len(session.query(Tile).all()) is 0:
        tile = Tile(
            x=0,
            y=0,
            temperature=25,
            precipitation=80,
            windspeed=5
        )
        session.add(tile)
        session.commit()
        return tile
    return None


def generate_around(start):
    new_tiles = []
    if not start.nw:
        nw = Tile(
            x=start.x - 1,
            y=start.y + 1,
            temperature=start.temperature * (1+uniform(-0.1, 0.1)),
            precipitation=start.precipitation * (1+uniform(-0.1, 0.1)),
            windspeed=start.windspeed * (1+uniform(-0.1, 0.1))
        )
        nw.nw = session.query(Tile).filter(and_(Tile.x == nw.x-1, Tile.y == nw.y+1)).first()
        nw.n = session.query(Tile).filter(and_(Tile.x == nw.x, Tile.y == nw.y+1)).first()
        nw.ne = session.query(Tile).filter(and_(Tile.x == nw.x+1, Tile.y == nw.y+1)).first()
        nw.e = session.query(Tile).filter(and_(Tile.x == nw.x+1, Tile.y == nw.y)).first()
        nw.se = start
        nw.s = session.query(Tile).filter(and_(Tile.x == nw.x, Tile.y == nw.y-1)).first()
        nw.sw = session.query(Tile).filter(and_(Tile.x == nw.x-1, Tile.y == nw.y-1)).first()
        nw.w = session.query(Tile).filter(and_(Tile.x == nw.x-1, Tile.y == nw.y)).first()
        session.add(nw)
        new_tiles.append(nw)
    if not start.n:
        n = Tile(
            x=start.x,
            y=start.y + 1,
            temperature=start.temperature * (1+uniform(-0.1, 0.1)),
            precipitation=start.precipitation * (1+uniform(-0.1, 0.1)),
            windspeed=start.windspeed * (1+uniform(-0.1, 0.1))
        )
        n.nw = session.query(Tile).filter(and_(Tile.x == n.x - 1, Tile.y == n.y + 1)).first()
        n.n = session.query(Tile).filter(and_(Tile.x == n.x, Tile.y == n.y + 1)).first()
        n.ne = session.query(Tile).filter(and_(Tile.x == n.x + 1, Tile.y == n.y + 1)).first()
        n.e = session.query(Tile).filter(and_(Tile.x == n.x + 1, Tile.y == n.y)).first()
        n.se = session.query(Tile).filter(and_(Tile.x == n.x + 1, Tile.y == n.y - 1)).first()
        n.s = start
        n.sw = session.query(Tile).filter(and_(Tile.x == n.x - 1, Tile.y == n.y - 1)).first()
        n.w = session.query(Tile).filter(and_(Tile.x == n.x - 1, Tile.y == n.y)).first()
        session.add(n)
        new_tiles.append(n)
    if not start.ne:
        ne = Tile(
            x=start.x + 1,
            y=start.y + 1,
            temperature=start.temperature * (1+uniform(-0.1, 0.1)),
            precipitation=start.precipitation * (1+uniform(-0.1, 0.1)),
            windspeed=start.windspeed * (1+uniform(-0.1, 0.1))
        )
        ne.nw = session.query(Tile).filter(and_(Tile.x == ne.x - 1, Tile.y == ne.y + 1)).first()
        ne.n = session.query(Tile).filter(and_(Tile.x == ne.x, Tile.y == ne.y + 1)).first()
        ne.ne = session.query(Tile).filter(and_(Tile.x == ne.x + 1, Tile.y == ne.y + 1)).first()
        ne.e = session.query(Tile).filter(and_(Tile.x == ne.x + 1, Tile.y == ne.y)).first()
        ne.se = session.query(Tile).filter(and_(Tile.x == ne.x + 1, Tile.y == ne.y - 1)).first()
        ne.s = session.query(Tile).filter(and_(Tile.x == ne.x, Tile.y == ne.y - 1)).first()
        ne.sw = start
        ne.w = session.query(Tile).filter(and_(Tile.x == ne.x - 1, Tile.y == ne.y)).first()
        session.add(ne)
        new_tiles.append(ne)
    if not start.e:
        e = Tile(
            x=start.x + 1,
            y=start.y,
            temperature=start.temperature * (1+uniform(-0.1, 0.1)),
            precipitation=start.precipitation * (1+uniform(-0.1, 0.1)),
            windspeed=start.windspeed * (1+uniform(-0.1, 0.1))
        )
        e.nw = session.query(Tile).filter(and_(Tile.x == e.x - 1, Tile.y == e.y + 1)).first()
        e.n = session.query(Tile).filter(and_(Tile.x == e.x, Tile.y == e.y + 1)).first()
        e.ne = session.query(Tile).filter(and_(Tile.x == e.x + 1, Tile.y == e.y + 1)).first()
        e.e = session.query(Tile).filter(and_(Tile.x == e.x + 1, Tile.y == e.y)).first()
        e.se = session.query(Tile).filter(and_(Tile.x == e.x + 1, Tile.y == e.y - 1)).first()
        e.s = session.query(Tile).filter(and_(Tile.x == e.x, Tile.y == e.y - 1)).first()
        e.sw = session.query(Tile).filter(and_(Tile.x == e.x - 1, Tile.y == e.y - 1)).first()
        e.w = start
        session.add(e)
        new_tiles.append(e)
    if not start.se:
        se = Tile(
            x=start.x + 1,
            y=start.y - 1,
            temperature=start.temperature * (1+uniform(-0.1, 0.1)),
            precipitation=start.precipitation * (1+uniform(-0.1, 0.1)),
            windspeed=start.windspeed * (1+uniform(-0.1, 0.1))
        )
        se.nw = start
        se.n = session.query(Tile).filter(and_(Tile.x == se.x, Tile.y == se.y + 1)).first()
        se.ne = session.query(Tile).filter(and_(Tile.x == se.x + 1, Tile.y == se.y + 1)).first()
        se.e = session.query(Tile).filter(and_(Tile.x == se.x + 1, Tile.y == se.y)).first()
        se.se = session.query(Tile).filter(and_(Tile.x == se.x + 1, Tile.y == se.y - 1)).first()
        se.s = session.query(Tile).filter(and_(Tile.x == se.x, Tile.y == se.y - 1)).first()
        se.sw = session.query(Tile).filter(and_(Tile.x == se.x - 1, Tile.y == se.y - 1)).first()
        se.w = session.query(Tile).filter(and_(Tile.x == se.x - 1, Tile.y == se.y)).first()
        session.add(se)
        new_tiles.append(se)
    if not start.s:
        s = Tile(
            x=start.x,
            y=start.y - 1,
            temperature=start.temperature * (1+uniform(-0.1, 0.1)),
            precipitation=start.precipitation * (1+uniform(-0.1, 0.1)),
            windspeed=start.windspeed * (1+uniform(-0.1, 0.1))
        )
        s.nw = session.query(Tile).filter(and_(Tile.x == s.x - 1, Tile.y == s.y + 1)).first()
        s.n = start
        s.ne = session.query(Tile).filter(and_(Tile.x == s.x + 1, Tile.y == s.y + 1)).first()
        s.e = session.query(Tile).filter(and_(Tile.x == s.x + 1, Tile.y == s.y)).first()
        s.se = session.query(Tile).filter(and_(Tile.x == s.x + 1, Tile.y == s.y - 1)).first()
        s.s = session.query(Tile).filter(and_(Tile.x == s.x, Tile.y == s.y - 1)).first()
        s.sw = session.query(Tile).filter(and_(Tile.x == s.x - 1, Tile.y == s.y - 1)).first()
        s.w = session.query(Tile).filter(and_(Tile.x == s.x - 1, Tile.y == s.y)).first()
        session.add(s)
        new_tiles.append(s)
    if not start.sw:
        sw = Tile(
            x=start.x - 1,
            y=start.y - 1,
            temperature=start.temperature * (1+uniform(-0.1, 0.1)),
            precipitation=start.precipitation * (1+uniform(-0.1, 0.1)),
            windspeed=start.windspeed * (1+uniform(-0.1, 0.1))
        )
        sw.nw = session.query(Tile).filter(and_(Tile.x == sw.x - 1, Tile.y == sw.y + 1)).first()
        sw.n = session.query(Tile).filter(and_(Tile.x == sw.x, Tile.y == sw.y + 1)).first()
        sw.ne = start
        sw.e = session.query(Tile).filter(and_(Tile.x == sw.x + 1, Tile.y == sw.y)).first()
        sw.se = session.query(Tile).filter(and_(Tile.x == sw.x + 1, Tile.y == sw.y - 1)).first()
        sw.s = session.query(Tile).filter(and_(Tile.x == sw.x, Tile.y == sw.y - 1)).first()
        sw.sw = session.query(Tile).filter(and_(Tile.x == sw.x - 1, Tile.y == sw.y - 1)).first()
        sw.w = session.query(Tile).filter(and_(Tile.x == sw.x - 1, Tile.y == sw.y)).first()
        session.add(sw)
        new_tiles.append(sw)
    if not start.w:
        w = Tile(
            x=start.x - 1,
            y=start.y,
            temperature=start.temperature * (1+uniform(-0.1, 0.1)),
            precipitation=start.precipitation * (1+uniform(-0.1, 0.1)),
            windspeed=start.windspeed * (1+uniform(-0.1, 0.1))
        )
        w.nw = session.query(Tile).filter(and_(Tile.x == w.x - 1, Tile.y == w.y + 1)).first()
        w.n = session.query(Tile).filter(and_(Tile.x == w.x, Tile.y == w.y + 1)).first()
        w.ne = session.query(Tile).filter(and_(Tile.x == w.x + 1, Tile.y == w.y + 1)).first()
        w.e = start
        w.se = session.query(Tile).filter(and_(Tile.x == w.x + 1, Tile.y == w.y - 1)).first()
        w.s = session.query(Tile).filter(and_(Tile.x == w.x, Tile.y == w.y - 1)).first()
        w.sw = session.query(Tile).filter(and_(Tile.x == w.x - 1, Tile.y == w.y - 1)).first()
        w.w = session.query(Tile).filter(and_(Tile.x == w.x - 1, Tile.y == w.y)).first()
        session.add(w)
        new_tiles.append(w)
    session.commit()
    return new_tiles


def generate_plane(max_tiles=10000):
    if session.query(Tile).count() is 0:
        make_zero()
    q = deque()
    q.extend(session.query(Tile).all())
    while True:
        if session.query(Tile).count() >= max_tiles:
            break
        tile = q.popleft()
        new_tiles = generate_around(tile)
        q.extend(new_tiles)


def print_coords():
    tiles = session.query(Tile).all()
    with open('coords.txt', 'w') as file:
        for tile in tiles:
            file.write('(%s,%s)\n' % tile.coord)
