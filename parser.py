class Reservation:
    def __init__(self, id, data):
        self.id = id
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
        self.increment = convertToHours(data['increment'] * 60 * 1000)  # Convert increment in minutes to hours
        self.startTime: int = convertToHours(data['startTime'])
        self.endTime: int = convertToHours(data['endTime'])
        self.optimizedSheet: OptimizedSheet = None

    def get_room_index(self, room_name):
        for index, connection in enumerate(self.connections):
            if connection.name == room_name:
                return index
        return None  # Returns None if the room is not found


    def transform_assignment(self):
        for i, assignment_list in enumerate(self.optimizedSheet):
            for j, is_assigned in enumerate(assignment_list):
                if is_assigned == 1:
                    room_name = self.connections[j].name  # Get room name from Connection instance
                    self.reservations[i].actualRooms = room_name
                    break  # Only assign to one room, so exit the inner loop

    def transform_into_original_data_format(self):
        result = []

        # Step 1: Group reservations by ID
        grouped_reservations = self.group_reservations_by_id()

        # Step 2: For each group, aggregate the actualRooms
        for reservation_id, reservations in grouped_reservations.items():
            aggregated_res = {
                'startTime': convertToMs(reservations[0].startTime),  # Assuming all reservations with the same ID have the same startTime
                'endTime': convertToMs(reservations[0].endTime),      # Similarly for endTime
                'wantedRooms': [r.wantedRooms.room for r in reservations],
                'actualRooms': [r.actualRooms for r in reservations]
            }
            result.append(aggregated_res)

        return result

    def group_reservations_by_id(self) -> dict:
        grouped_reservations = {}
        for reservation in self.reservations:
            reservation_id = reservation.id
            if reservation_id not in grouped_reservations:
                grouped_reservations[reservation_id] = []
            grouped_reservations[reservation_id].append(reservation)
        return grouped_reservations

class OptimizedSheet:
    def __init__(self,result):
        self.result: list[list[int]] = result

PRECISION_FACTOR = 4

def convertToHours(ms) -> int:
    return int(ms / 3600000 * PRECISION_FACTOR)

def convertToMs(hours) -> int:
    return int(hours * 3600000 / PRECISION_FACTOR)

def createReservations(reservations) -> list[Reservation]:
    result = []
    i = 0
    for reservation in reservations:
        for room in reservation['wantedRooms']:
            r = Reservation(i, reservation)
            r.wantedRooms = Room(room)
            result.append(r)
        i += 1
    return result