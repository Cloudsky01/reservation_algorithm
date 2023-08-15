from main import is_schedulable, visualize_solution_plot
from parser import Reservation


reservations = [
    Reservation({"startTime": 37800000, "endTime": 41400000, "wantedRooms": "golf #2", "actualRooms": "golf #2"}),
]

solution = is_schedulable(reservations=reservations, num_rooms_guess=5, start_time=7.0, end_time=27.0)
print(solution)