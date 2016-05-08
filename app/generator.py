from . import session
from .models import Tile, Point
from random import uniform
from collections import deque
from sqlalchemy import and_

COMPASS = {
    'nw': Point(-1, 1),
    'n': Point(0, 1),
    'ne': Point(1, 1),
    'w': Point(-1, 0),
    'e': Point(1, 0),
    'sw': Point(-1, -1),
    's': Point(0, -1),
    'se': Point(1, -1)
}


def get_origin(temperature=25, precipitation=80, windspeed=5):
    if len(session.query(Tile).all()) is 0:
        tile = Tile(
            x=0,
            y=0,
            temperature=temperature,
            precipitation=precipitation,
            windspeed=windspeed
        )
        session.add(tile)
        session.commit()
        return tile
    return session.query(Tile).filter(Tile.x == 0, Tile.y == 0).first()


def generate_direction(start, compass_point):
    coord_mod = COMPASS.get(compass_point)
    if not coord_mod:
        raise Exception("Not a valid compass point.")
    if not getattr(start, compass_point):
        newtile = Tile(
            x=start.x + coord_mod.x,
            y=start.y + coord_mod.y,
            temperature=start.temperature * (1 + uniform(-0.1, 0.1)),
            precipitation=start.precipitation * (1 + uniform(-0.1, 0.1)),
            windspeed=start.windspeed * (1 + uniform(-0.1, 0.1))
        )
        query = session.query(Tile).filter(and_(
            Tile.x >= newtile.x - 1,
            Tile.x <= newtile.x + 1,
            Tile.y >= newtile.y - 1,
            Tile.y <= newtile.y + 1
        )).all()
        for qtile in query:
            for direction, mod_ in COMPASS.items():
                if qtile.x == newtile.x + mod_.x and qtile.y == newtile.y + mod_.y:
                    setattr(newtile, direction, qtile)
        session.add(newtile)
        session.commit()
        return newtile
    raise Exception('Already a tile in that direction!')


def generate_around(start, max_tiles=None):
    new_tiles = []
    for direction, coord_mod in COMPASS.items():
        if max_tiles and session.query(Tile).count() >= max_tiles:
            session.commit()
            return new_tiles
        if getattr(start, direction) is None:
            newtile = Tile(
                x=start.x + coord_mod.x,
                y=start.y + coord_mod.y,
                temperature=start.temperature * (1+uniform(-0.1, 0.1)),
                precipitation=start.precipitation * (1+uniform(-0.1, 0.1)),
                windspeed=start.windspeed * (1+uniform(-0.1, 0.1))
            )
            query = session.query(Tile).filter(and_(
                Tile.x >= newtile.x - 1,
                Tile.x <= newtile.x + 1,
                Tile.y >= newtile.y - 1,
                Tile.y <= newtile.y + 1,
            )).all()
            for qtile in query:
                for direction_inner, coord_mod_inner in COMPASS.items():
                    if qtile.x == newtile.x + coord_mod_inner.x and qtile.y == newtile.y + coord_mod_inner.y:
                        setattr(newtile, direction_inner, qtile)
            session.add(newtile)
            new_tiles.append(newtile)
    session.commit()
    return new_tiles


def generate_plane(max_tiles=10000):
    if session.query(Tile).count() is 0:
        get_origin()
    q = deque()
    q.extend(session.query(Tile).all())
    while session.query(Tile).count() < max_tiles:
        tile = q.popleft()
        new_tiles = generate_around(tile, max_tiles=max_tiles)
        q.extend(new_tiles)
