import time
from random import uniform, randint
from threading import Thread


class Ticker(Thread):
    def __init__(self, sleep, func):
        self.sleep = sleep
        self.func = func
        super().__init__(name='Ticker')
        self.setDaemon(True)

    def run(self):
        while True:
            time.sleep(self.sleep)
            self.func()


class World(object):
    def __init__(self):
        self.hamsters = []

        self.tick_queue = []
        self.tick_count = 0
        self.ticker = Ticker(1, self.do_tick)
        self.ticker.start()

    def do_tick(self):
        tick_gen = ((func, args, interval, repeat) for func, args, interval, repeat
                    in self.tick_queue if self.tick_count % interval is 0)
        for tick in tick_gen:
            func, args, interval, repeat = tick
            if args:
                func(**args)
            else:
                func()
            if not repeat:
                self.tick_queue.remove(tick)
        self.tick_count += 1

    def add_tick(self, func, args, interval, repeat=True):
        self.tick_queue.append((func, args, interval, repeat))

    def add_hamster(self, tile):
        hamster = Hamster(tile)
        self.hamsters.append(hamster)
        self.add_tick(hamster.move, None, int(hamster.dex/2))


class Hamster(object):
    def __init__(self, tile):
        self.tile = tile
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

    def move(self):
        if self.happiness > 99:
            return
        adj_hap = {dir_: self.calc_happiness(tile) for dir_, tile in self.tile.adjacents.items()}
        self.tile = self.tile.adjacents[min(adj_hap, key=adj_hap.get)]


