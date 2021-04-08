import datetime
import random


# Represents a "square" in the store at a particular location, and contain all valid moves from that location
class Location:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        # a list of all valid moves. Each move is a tuple of the form
        # ("adjacent x location", "adjacent y location", "is this closer to the exit?")
        self.validMoves = [(a, b, True if a <= self.x and b <= self.y else False) for a in
                           range(max(self.x - 1, 0), min(self.x + 2, width)) for b in
                           range(max(self.y - 1, 0), min(self.y + 2, height)) if not (a == self.x and b == self.y)]


class Store:
    def __init__(self, width: int, height: int):
        self.height = height
        self.width = width
        self.locations = [[Location(x, y, width, height) for y in range(0, height)] for x in range(0, width)]


class Customer:
    def __init__(self, store, customer_id: str, name: str):
        self.store = store
        # customers enter and exit from the bottom left corner of the store
        self.currentLocation = store.locations[0][0]
        # the *average* amount of time this customer will spend on a square
        self.meanDwellTime = random.uniform(1, 20)
        # how consistently the customer spends that time. Higher means more inconsistent
        self.consistency = random.uniform(1, 5)
        self.nextMoveTime = self.get_next_move_time()
        self.isExiting = False
        # the time this customer will start to exit
        self.exitTime = datetime.datetime.now() + datetime.timedelta(0, random.uniform(1, 600))
        self.id = customer_id
        self.name = name

    def get_next_move_time(self):
        # amount of time spent at a location is a random value picked from a gaussian distribution,
        # with a mean equal to the customer's average dwell time and a standard deviation
        # equal to the customer's consistency
        return datetime.datetime.now() + datetime.timedelta(0, random.gauss(self.meanDwellTime, self.consistency))

    def move(self):
        # if the customer is exiting, only move to an adjacent location that is towards the exit.
        # If they are already at the door, don't move
        if self.isExiting:
            if self.currentLocation.x == 0 and self.currentLocation.y == 0:
                (newX, newY) = (0, 0)
            else:
                (newX, newY, isTowardsExit) = random.choice(
                    [(x, y, e) for (x, y, e) in self.currentLocation.validMoves if e is True])
        else:
            # if the customer is not exiting, pick any adjacent location
            (newX, newY, isTowardsExit) = random.choice(self.currentLocation.validMoves)

        self.currentLocation = self.store.locations[newX][newY]

    def tick(self):
        if not self.isExiting and self.exitTime < datetime.datetime.now():
            self.isExiting = True

        if self.nextMoveTime < datetime.datetime.now():
            self.nextMoveTime = self.get_next_move_time()
            self.move()
            return True

        return False
