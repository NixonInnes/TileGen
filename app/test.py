import asyncio
from random import randint
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


class World(object):
    def __init__(self):
        self.hamsters = []
        self.loop = asyncio.get_event_loop()

    def start_loop(self):
        #tasks = self.move_hamsters()
        self.loop.run_forever()

    def where_hamsters(self):
        for hamster in self.hamsters:
            print("Hamster %s is at (%s, %s)" % (self.hamsters.index(hamster), hamster.x, hamster.y))

    #@asyncio.coroutine
    #def move_hamsters(self):
    #    for hamster in self.hamsters:
    #        yield from hamster.move()

    def add_hamster(self):
        hamster = Hamster(len(self.hamsters))
        asyncio.Task(hamster.move())
        self.hamsters.append(hamster)

    def add_hamsters(self, num=1):
        for i in range(num):
            self.add_hamster()


class Hamster(object):
    def __init__(self, name):
        self.name = name
        self.x = 0
        self.y = 0
        self.sex = 'm' if randint(0, 1) is 0 else 'f'
        self.speed = randint(0, 9)

    @asyncio.coroutine
    def move(self):
        self.x += randint(-1, 1)
        self.y += randint(-1, 1)
        print('%s (speed: %s) moved to (%s,%s)' % (self.name, self.speed, self.x, self.y))
        yield from asyncio.sleep(10 - self.speed)
        asyncio.Task(self.move())

    def coord(self):
        return Point(self.x, self.y)

