class Reservation:
    def __init__(self, data):
        self.startTime = data['startTime']
        self.endTime = data['endTime']
        self.wantedRooms = data['wantedRooms']
        self.actualRooms = data['actualRooms']

class Connection:
    def __init__(self, connection):
        self.connection = [Room(room) for room in connection]

class Room:
    def __init__(self, room):
        self.room = room

class Sheet:
    def __init__(self, data):
        self.connections = [Connection(connection) for connection in data['connections']]
        self.reservations = [Reservation(reservation) for reservation in data['reservation']]
        self.increment = data['increment']
        self.startTime = data['startTime']
        self.endTime = data['endTime']
