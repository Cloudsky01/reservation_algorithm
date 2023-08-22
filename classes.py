import math
from typing import List, Optional


class Reservation:
    def __init__(self, res: dict, index, increment):
        self.id = res["id"]
        self.startTime: int = math.ceil(res["startTime"] / increment)
        self.endTime: int = math.floor(res["endTime"] / increment)
        self.actualRooms: List[str] = res["actualRooms"]
        self.wantedRooms: List[Optional(str)] = res["wantedRooms"]
        self.suitableRooms: List[str] = res["suitableRooms"]
        self.connectedSolutions: List[List[str]] = res["connectedSolutions"]
        self.index: int = index


class Sheet:
    def __init__(self, sheet: dict):
        self.startTime = math.ceil(sheet["startTime"] / sheet["increment"])
        self.endTime = math.ceil(sheet["endTime"] / sheet["increment"])
        self.rooms = sheet["rooms"]
        self.increment = sheet["increment"]
        self.reservations = [ Reservation(res, i, self.increment) for i, res in enumerate(sheet["reservations"])]
