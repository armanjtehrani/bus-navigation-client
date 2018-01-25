import _thread
import time

from bus import *


BUS_TOKENS = [
    'qwerty',
]


if __name__ == "__main__":
    bus_list = []
    for token in BUS_TOKENS:
        bus_list.append(Bus(token))
    for bus in bus_list:
        bus.start()
