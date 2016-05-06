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
    return


def generate_around(start):
    compass = (
        ('nw', -1, 1),
        ('n', 0, 1),
        ('ne', 1, 1),
        ('w', -1, 0),
        ('e', 1, 0),
        ('sw', -1, -1),
        ('s', 0, -1),
        ('se', 1, -1)
    )
    new_tiles = []
    for point, xmod, ymod in compass:
        if getattr(start, point) is None:
            newtile = Tile(
                x=start.x + xmod,
                y=start.y + ymod,
                temperature=start.temperature * (1+uniform(-0.1, 0.1)),
                precipitation=start.precipitation * (1+uniform(-0.1, 0.1)),
                windspeed=start.windspeed * (1+uniform(-0.1, 0.1))
            )
            query = session.query(Tile).filter(and_(
                Tile.x >= newtile.x - 1,
                Tile.x <= newtile.x + 1,
                Tile.y >= newtile.y - 1,
                Tile.y <= newtile.y + 1
            )).all()
            for qtile in query:
                for point, xmod, ymod in compass:
                    if qtile.x == newtile.x + xmod and qtile.y == newtile.y + ymod:
                        setattr(newtile, point, qtile)
            session.add(newtile)
            new_tiles.append(newtile)
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
