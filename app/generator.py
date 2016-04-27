from . import session
from .models import Tile
from random import uniform


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
        start.nw = nw
        nw.e = start.n
        nw.s = start.w
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
        start.n = n
        n.w = start.nw
        n.e = start.ne
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
        start.ne = ne
        ne.w = start.n
        ne.s = start.e
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
        start.e = e
        e.n = start.ne
        e.s = start.se
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
        start.se = se
        se.n = start.e
        se.w = start.s
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
        start.s = s
        s.e = start.se
        s.w = start.sw
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
        start.sw = sw
        sw.e = start.s
        sw.n = start.w
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
        start.w = w
        w.n = start.nw
        w.s = start.sw
        session.add(w)
        new_tiles.append(w)
    session.commit()
    return new_tiles


def generate_plane(max_tiles=10000):
    if session.query(Tile).count() is 0:
        make_zero()
    q = session.query(Tile).all()
    while True:
        if session.query(Tile).count() >= max_tiles:
            break
        tile = q.pop(0)
        new_tiles = generate_around(tile)
        q += new_tiles


def print_coords():
    tiles = session.query(Tile).all()
    with open('coords.txt', 'w') as file:
        for tile in tiles:
            file.write('(%s,%s)\n' % tile.coord)
