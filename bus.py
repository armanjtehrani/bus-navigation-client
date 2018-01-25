import json
import threading
import time
from websocket import create_connection


class Bus(threading.Thread):
    def __init__(self, token):
        threading.Thread.__init__(self)
        self.token = token
        self.ws = create_connection("ws://localhost:8000/buses/")

        self.line = None
        self.prev_station = None
        self.next_station = None
        self.bus_info = None

        self.x = None
        self.y = None
        self.speed = None
        self.next_station_x = None
        self.next_station_y = None
        self.is_on_station = None
        self.bus_wait_time = None

    def print(self, text=''):
        print(text)
        print('line:', self.line)
        print('x:', self.x)
        print('y:', self.y)
        print('speed:', self.speed)
        print('next_station_x:', self.next_station_x)
        print('next_station_y:', self.next_station_y)
        print('is_on_station:', self.is_on_station)
        print('bus_wait_time:', self.bus_wait_time)

    def run(self):
        print("Starting " + self.token)
        self.init()
        self.begin()
        self.ws.close()

    def init(self):
        self.send('unknown')
        bus_data = self.recv()
        self.line = bus_data['line']
        self.next_station = bus_data['next_station']
        self.prev_station = bus_data['prev_station']
        self.bus_info = bus_data['bus']
        self.x = self.bus_info['x_pos']
        self.y = self.bus_info['y_pos']
        self.speed = self.bus_info['speed']
        self.next_station_x = self.next_station['x_pos']
        self.next_station_y = self.next_station['y_pos']
        self.is_on_station = self.bus_info['is_on_station']
        self.bus_wait_time = self.next_station['bus_wait_time']
        self.print('init:::')

    def send(self, status, data={}):
        data['token'] = self.token
        data['status'] = status
        print('send data:', data)
        self.ws.send(json.dumps(data))

    def recv(self):
        recv_data = json.loads(self.ws.recv())
        print('recv data:', recv_data)
        return recv_data

    def begin(self):
        while True:
            if not self.is_on_station:
                print('on the way')
                self.calculate_my_next_position()
                self.wait_to_rich_next_position()
                if not self.arrived_next_station():
                    self.send('new_pos', {'x_pos': self.x, 'y_pos': self.y})
                else:
                    self.build_new_bus_info()
            else:
                print('arrived to next station!!')
                self.wait_to_go_from_station()
                self.is_on_station = False

    def calculate_my_next_position(self):
        distance = self.get_distance_from_next_station()
        if distance <= self.speed:
            self.x = self.next_station_x
            self.y = self.next_station_y
            return
        # tg = (self.next_station_y - self.y)/(self.next_station_x - self.x)
        sin = (self.next_station_y - self.y)/distance
        cos = (self.next_station_x - self.x)/distance
        diff_y = self.speed * sin
        diff_x = self.speed * cos
        self.y += diff_y
        self.x += diff_x

    def get_distance_from_next_station(self):
        distance = ((self.next_station_y - self.y) ** 2 + (self.next_station_x - self.x) ** 2) ** .5
        print('distance:', distance)
        return distance

    def wait_to_rich_next_position(self):
        time.sleep(1)

    def arrived_next_station(self):
        if self.x == self.next_station_x and \
                        self.y == self.next_station_y:
            return True
        return False

    def build_new_bus_info(self):
        self.send('arrived_to_station')
        bus_data = self.recv()
        self.line = bus_data['line']
        self.next_station = bus_data['next_station']
        self.prev_station = bus_data['prev_station']
        self.bus_info = bus_data['bus']
        self.x = self.bus_info['x_pos']
        self.y = self.bus_info['y_pos']
        self.speed = self.bus_info['speed']
        self.next_station_x = self.next_station['x_pos']
        self.next_station_y = self.next_station['y_pos']
        self.is_on_station = self.bus_info['is_on_station']
        self.bus_wait_time = self.next_station['bus_wait_time']
        self.print('arived to next station:::')

    def wait_to_go_from_station(self):
        time.sleep(self.bus_wait_time)

# ws = create_connection("ws://localhost:8000/buses/")
# print("Sending 'Hello, World'...")
# data = {'status': 'unknown', 'token': 'qwer'}
# data = json.dumps(data)
# ws.send(data)
# print("Sent")
# print("Reeiving...")
# result = ws.recv()
# print("Received '%s'" % result)
# print("Received '%s'" % json.loads(result)['line'])
#
# ws.close()
