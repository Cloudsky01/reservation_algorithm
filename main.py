from ortools.sat.python import cp_model
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def visualize_solution_plot(reservations, assignments, num_rooms):
    """
    Visualize the reservation assignments.
    
    reservations: List of reservation dicts with "start" and "end" keys.
    assignments: Result of the optimizer (2D list) where assignments[i][j] == 1 indicates
                 that reservation i is assigned to room j.
    num_rooms: Number of rooms.
    """
    
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, num_rooms))
    ax.set_xlim(min(r['start'] for r in reservations), max(r['end'] for r in reservations))
    ax.set_ylim(0, num_rooms)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Room')
    ax.set_yticks([i + 0.5 for i in range(num_rooms)])
    ax.set_yticklabels([f'Room {i}' for i in range(num_rooms)])
    
    # Loop through each reservation and room, checking assignments
    for i, reservation in enumerate(reservations):
        for j in range(num_rooms):
            if assignments[i][j] == 1:  # If reservation i is assigned to room j
                rect = patches.Rectangle((reservation['start'], j), reservation['end'] - reservation['start'], 1, facecolor='blue', edgecolor='black')
                ax.add_patch(rect)
                ax.text((reservation['start'] + reservation['end']) / 2, j + 0.5, f"R{i}", ha='center', va='center', color='white')
                
    plt.tight_layout()
    plt.show()

def visualize_schedule(optimized_schedule, reservations):
    """
    Visualizes the optimized schedule in matrix form.
    Rows: Reservations with their start and end times
    Columns: Rooms
    'X' indicates the room assignment for a reservation.
    """
    print(" " * 15 + "|".join(f" Room {i+1} " for i in range(len(optimized_schedule[0]))))
    print("-" * (8 * len(optimized_schedule[0]) + 14))
    for i, room_assignments in enumerate(optimized_schedule):
        timing = f"({reservations[i]['start']}-{reservations[i]['end']})"
        row = f"Rsv {i+1} {timing:<7}" + "".join("    X   " if room else "        " for room in room_assignments)
        print(row)

"""
The is_schedulable function takes in a list of reservations and a number of rooms to guess.
It returns a schedule if the reservations can be scheduled in the given number of rooms.
Otherwise, it returns None.
"""

def is_schedulable(reservations, num_rooms_guess, start_time=0, end_time=24):
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
                if not (reservations[i1]['end'] <= reservations[i2]['start'] or reservations[i1]['start'] >= reservations[i2]['end']):
                    model.Add(assignment[i1][j] + assignment[i2][j] <= 1)


    # NOT OK - Number 1
    gaps = [[model.NewBoolVar(f"gap_{j}_time_{t}") for t in range(end_time - start_time)] for j in range(num_rooms_guess)]

    result_start = []
    result_end = []

    for j in range(num_rooms_guess):
        for t in range(end_time - start_time):
            result_start = [assignment[i][j] for i, reservation in enumerate(reservations) if reservation['start'] == t]
            result_end = [assignment[i][j] for i, reservation in enumerate(reservations) if reservation['end'] == t]
            model.Add(sum(result_end) - sum(result_start) <= gaps[j][t])

            
    # OK - Number 3
    for i, reservation in enumerate(reservations):
        if 'wantedRoom' in reservation:
            preferred_room = reservation['wantedRoom']
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


# Example reservations
reservations = [
    {"start": 8, "end": 10, "wantedRoom": 1},
]


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

if __name__ == "__main__":
    optimized_schedule = is_schedulable(reservations, 15)
    count = 0
    while len(reservations) != 80:
        reservation = generate_random_reservations_without_wanted_room(8, 24)
        reservations.append(reservation)
        optimized_schedule = is_schedulable(reservations, 15)
        if optimized_schedule == None:
            reservations.pop()
        count += 1
        print(len())
        print(count)
    print(count)
    reservations.pop()
    optimized_schedule = is_schedulable(reservations, 15)
    # print("Optimized Schedule:")
    # print(optimized_schedule)
    # visualize_schedule(optimized_schedule, reservations)
    visualize_solution_plot(reservations, optimized_schedule, len(optimized_schedule[0]))


