from random import uniform, randint
import asyncio

from app.generator import get_origin


class World(object):
    def __init__(self):
        self.hamsters = []
        self.loop = asyncio.get_event_loop()

    def start(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.stop()
        finally:
            self.loop.close()

    def add_hamster(self):
        hamster = Hamster(len(self.hamsters))
        self.hamsters.append(hamster)
        asyncio.Task(hamster.move())


class Hamster(object):
    def __init__(self, name):
        self.name = name
        self.tile = get_origin()
        self.tile_history = []
        self.sex = randint(0, 1)
        self.pref_temp = 25 * (1 + uniform(-0.5, 0.5))
        self.pref_prec = 80 * (1 + uniform(-0.5, 0.5))
        self.pref_wind = 5 * (1 + uniform(-0.5, 0.5))

        self.str = randint(2, 12)
        self.dex = randint(2, 12)

        self.happiness = self.calc_happiness(self.tile)

    def calc_happiness(self, tile):
        temp_level = abs(self.pref_temp - tile.temperature)/self.pref_temp
        prec_level = abs(self.pref_prec - tile.precipitation)/self.pref_prec
        wind_level = abs(self.pref_wind - tile.windspeed)/self.pref_wind
        return int(((temp_level + prec_level + wind_level)/3)*100)

    @asyncio.coroutine
    def move(self):
        if self.happiness > 90:
            return
        adj_hap = {dir_: self.calc_happiness(tile) for dir_, tile in self.tile.adjacents.items()
                   if tile is not None and tile not in self.tile_history}
        self.tile_history.append(self.tile)
        if len(self.tile_history) > 3:
            self.tile_history.pop(0)
        self.tile = self.tile.adjacents[max(adj_hap, key=adj_hap.get)]
        self.happiness = self.calc_happiness(self.tile)
        print("Hamster %s moved to tile (%s,%s)" % (self.name, self.tile.x, self.tile.y))
        yield from asyncio.sleep(25 - self.dex)
        asyncio.Task(self.move())
