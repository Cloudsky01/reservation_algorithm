from ortools.sat.python import cp_model
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from flask import Flask, request, jsonify
import random
from parser import Sheet, Reservation, Room
import requests

app = Flask(__name__)

def visualize_solution_plot(reservations: list[Reservation], assignments, num_rooms):
    """
    Visualize the reservation assignments.
    
    reservations: List of reservation dicts with "start" and "end" keys.
    assignments: Result of the optimizer (2D list) where assignments[i][j] == 1 indicates
                 that reservation i is assigned to room j.
    num_rooms: Number of rooms.
    """
    
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, num_rooms))
    ax.set_xlim(min(r['startTime'] for r in reservations), max(r.endTime for r in reservations))
    ax.set_ylim(0, num_rooms)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Room')
    ax.set_yticks([i + 0.5 for i in range(num_rooms)])
    ax.set_yticklabels([f'Room {i}' for i in range(num_rooms)])
    
    # Loop through each reservation and room, checking assignments
    for i, reservation in enumerate(reservations):
        for j in range(num_rooms):
            if assignments[i][j] == 1:  # If reservation i is assigned to room j
                rect = patches.Rectangle((reservation.startTime, j), reservation.endTime - reservation.startTime, 1, facecolor='blue', edgecolor='black')
                ax.add_patch(rect)
                ax.text((reservation.startTime + reservation.endTime) / 2, j + 0.5, f"R{i}", ha='center', va='center', color='white')
                
    plt.tight_layout()
    plt.show()

"""
The is_schedulable function takes in a list of reservations and a number of rooms to guess.
It returns a schedule if the reservations can be scheduled in the given number of rooms.
Otherwise, it returns None.
"""

def is_schedulable(reservations: list[Reservation], num_rooms_guess: int, start_time: int, end_time: int):
    print("Start time: ", start_time)
    print("End time: ", end_time)
    print("Reservations: ", reservations)
    [print(reservation.startTime) for reservation in reservations]
    model = cp_model.CpModel()
    num_reservations = len(reservations)

    # Create a boolean variable for each reservation-room assignment
    # assignment[i][j] = 1 if reservation i is assigned to room j
    assignment = [
        [model.NewBoolVar(f"assignment_{i}_{j}") for j in range(num_rooms_guess)]
        for i in range(num_reservations)
    ]

    # OK - Number 4
    # Each reservation is assigned to exactly one room
    for i in range(num_reservations):
        model.Add(sum(assignment[i]) == 1)

    # OK - Number 2
    # No overlapping reservations in the same room
    for j in range(num_rooms_guess):
        for i1 in range(num_reservations):
            for i2 in range(i1 + 1, num_reservations):
                if not (reservations[i1].endTime <= reservations[i2].startTime or reservations[i1].startTime >= reservations[i2].endTime):
                    model.Add(assignment[i1][j] + assignment[i2][j] <= 1)


    # NOT OK - Number 1
    gaps = [[model.NewBoolVar(f"gap_{j}_time_{t}") for t in range(end_time - start_time)] for j in range(num_rooms_guess)]

    result_start = []
    result_end = []

    for j in range(num_rooms_guess):
        for t in range(end_time - start_time):
            result_start = [assignment[i][j] for i, reservation in enumerate(reservations) if reservation.startTime == t]
            result_end = [assignment[i][j] for i, reservation in enumerate(reservations) if reservation.endTime == t]
            model.Add(sum(result_end) - sum(result_start) <= gaps[j][t])

            
    # OK - Number 3
    # TODO : Fix this constraint
    for i, reservation in enumerate(reservations):
        if 'wantedRoom' in reservation.wantedRooms:
            preferred_room = reservation.wantedRooms
            model.Add(assignment[i][preferred_room] == 1)

    # Objective: minimize gap time using overlap variable
    gap_time = []
    for t in gaps:
        for r in t:
            gap_time.append(r)
    model.Minimize(sum(gap_time))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        optimized_schedule = [
            [solver.Value(assignment[i][j]) for j in range(num_rooms_guess)]
            for i in range(num_reservations)
        ]
        return optimized_schedule
    else: 
        print("No solution found")
    return None

def generate_random_reservations_without_wanted_room(start_time, end_time):
    """
    Generate a list of random reservations without the 'wantedRoom' attribute.
    
    num_reservations: Number of reservations to generate.
    start_time: Start time range for reservations.
    end_time: End time range for reservations.
    """
    start = random.randint(start_time, end_time - 4)
    end = random.randint(start + 1, start + 4)
    reservation = {"start": start, "end": end}
    return reservation

@app.route('/', methods=['GET'])
def index():
    return "Hello World!"

@app.route('/schedule', methods=['POST'])
def schedule():
    try:
        sheet = request.get_json()
        sheet = Sheet(sheet)
        [print(reservation.startTime) for reservation in sheet.reservations]
        return is_schedulable(sheet.reservations, sheet.numRooms, int(sheet.startTime), int(sheet.endTime))
    except:
        return "Error"    



if __name__ == '__main__':
    app.run(debug=True)
    app.config['TEMPLATES_AUTO_RELOAD'] = True



