import math
from typing import List, Optional


ROOM_CONNECTIONS_FACTOR = 1000
GAP_FACTOR = 100
PRIORITY_FACTOR = 1


class Reservation:
    def __init__(self, res: dict, index, increment, sheetStart):
        self.id = res["id"]
        self.startTime: int = math.ceil((res["startTime"] - sheetStart) / increment)
        self.endTime: int = math.floor((res["endTime"] - sheetStart) / increment)
        self.actualRooms: List[str] = res["actualRooms"]
        self.wantedRooms: List[Optional(str)] = res["wantedRooms"]
        self.suitableRooms: List[str] = res["suitableRooms"]
        self.connectedSolutions: List[List[str]] = res["connectedSolutions"]
        self.index: int = index


class Sheet:
    def __init__(self, sheet: dict):
        self.endTime = math.ceil((sheet["endTime"] - sheet["startTime"]) / sheet["increment"])
        self.rooms = sheet["rooms"]
        self.increment = sheet["increment"]
        self.reservations = [ Reservation(res, i, self.increment, sheet["startTime"]) for i, res in enumerate(sheet["reservations"])]
        self.roomPriority = [roomConfig["priority"] for roomConfig in sheet["roomConfigs"]]
        self.tenant = sheet.get("tenant", "unknown")
        self.priorityFactor = sheet.get("priorityFactor", PRIORITY_FACTOR)
        self.gapFactor = sheet.get("gapFactor", GAP_FACTOR)
        self.roomConnections = sheet.get("roomConnectionsFactor", ROOM_CONNECTIONS_FACTOR)
