class Reservation:
    def __init__(self, data):
        self.startTime = convertToHours(data['startTime'])
        self.endTime = convertToHours(data['endTime'])
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
        self.numRooms = len(data['connections'])
        self.increment = data['increment']
        self.startTime: int = convertToHours(data['startTime'])
        self.endTime: int = convertToHours(data['endTime'])


def convertToHours(ms) -> int:
    return ms / 3600000