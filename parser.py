class Reservation:
    def __init__(self, data):
        self.startTime = convertToHours(data['startTime'])
        self.endTime = convertToHours(data['endTime'])
        self.wantedRooms = data['wantedRooms']
        self.actualRooms = data['actualRooms']

    def transform_into_original_data_format(self):
        return {
            'startTime': convertToMs(self.startTime),
            'endTime': convertToMs(self.endTime),
            # TODO : Rethink this
            'wantedRooms': None,
            'actualRooms': self.actualRooms
        }

class Connection:
    def __init__(self, connection):
        self.name = connection
        self.connection = [Room(room) for room in connection]

class Room:
    def __init__(self, room):
        self.room = room

class Sheet:
    def __init__(self, data):
        self.sheet = data
        self.connections = [Connection(connection) for connection in data['connections']]
        self.reservations: list[Reservation] = createReservations(data['reservation'])
        self.numRooms = len(data['connections'])
        self.increment = data['increment']
        self.startTime: int = convertToHours(data['startTime'])
        self.endTime: int = convertToHours(data['endTime'])
        self.optimizedSheet: OptimizedSheet = None

    def transform_assignment(self):
        for i, assignment_list in enumerate(self.optimizedSheet):
            for j, is_assigned in enumerate(assignment_list):
                if is_assigned == 1:
                    room_name = self.connections[j].name  # Get room name from Connection instance
                    self.reservations[i].actualRooms = room_name
                    break  # Only assign to one room, so exit the inner loop

    def transform_into_original_data_format(self):
        for idx, value in enumerate(self.sheet['reservation']):
            self.sheet['reservation'][idx] = self.reservations[idx].transform_into_original_data_format()

class OptimizedSheet:
    def __init__(self,result):
        self.result: list[list[int]] = result

def convertToHours(ms) -> int:
    return ms / 3600000

def convertToMs(hours) -> int:
    return hours * 3600000

def createReservations(reservations) -> list[Reservation]:
    result = []
    for reservation in reservations:
        for room in reservation['wantedRooms']:
            r = Reservation(reservation)
            r.wantedRooms = Room(room)
            result.append(r)
    return result