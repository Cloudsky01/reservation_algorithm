from ortools.sat.python import cp_model
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
    ax.set_yticklabels([f'Room {i + 1}' for i in range(num_rooms)])
    
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

def is_schedulable(reservations, num_rooms_guess):
    model = cp_model.CpModel()
    num_reservations = len(reservations)

    # Create a boolean variable for each reservation-room assignment
    # assignment[i][j] = 1 if reservation i is assigned to room j
    assignment = [
        [model.NewBoolVar(f"assignment_{i}_{j}") for j in range(num_rooms_guess)]
        for i in range(num_reservations)
    ]

    # Each reservation is assigned to exactly one room
    for i in range(num_reservations):
        model.Add(sum(assignment[i]) == 1)

    # No overlapping reservations in the same room
    for j in range(num_rooms_guess):
        for i1 in range(num_reservations):
            for i2 in range(i1 + 1, num_reservations):
                if not (reservations[i1]['end'] <= reservations[i2]['start'] or reservations[i1]['start'] >= reservations[i2]['end']):
                    model.Add(assignment[i1][j] + assignment[i2][j] <= 1)

    # Intermediate variable to represent overlap for gap computation
    # overlap[i1][i2][j] = 1 if reservation i1 and i2 overlap in room j
    overlap = [[[model.NewBoolVar(f"overlap_{i1}_{i2}_{j}") for j in range(num_rooms_guess)] for i2 in range(num_reservations)] for i1 in range(num_reservations)]

    # Define overlap variable
    """
        Depends on the following constraints:
        The overlap variable is dependent on the assignment variables.
        For each pair of reservations (i1, i2) and for each room j, if both assignment[i1][j] and assignment[i2][j] are true, then overlap[i1][i2][j] should be true.
        For each pair of reservations (i1, i2) and for each room j, if overlap[i1][i2][j] is true, then at least one of assignment[i1][j] and assignment[i2][j] should be false.
    """
    for j in range(num_rooms_guess):
        for i1 in range(num_reservations):
            for i2 in range(i1 + 1, num_reservations):
                # If there is an overlap, then both assignments must be true
                model.AddImplication(overlap[i1][i2][j], assignment[i1][j])
                model.AddImplication(overlap[i1][i2][j], assignment[i2][j])
                model.AddBoolOr([overlap[i1][i2][j].Not(), assignment[i1][j].Not()])
                model.AddBoolOr([overlap[i1][i2][j].Not(), assignment[i2][j].Not()])

    # Objective: minimize gap time using overlap variable
    """
        The objective is to minimize the gap time.
        The gap time is the time between the end of one reservation and the start of the next reservation.
        The gap time is computed for each pair of reservations (i1, i2) and for each room j.
        The gap time is computed as the difference between the start of reservation i2 and the end of reservation i1, multiplied by the overlap variable.
    """
    gap_time = []
    for j in range(num_rooms_guess):
        for i1 in range(num_reservations):
            for i2 in range(i1 + 1, num_reservations):
                if reservations[i1]['end'] <= reservations[i2]['start']:
                    gap = (reservations[i2]['start'] - reservations[i1]['end']) * overlap[i1][i2][j]
                    gap_time.append(gap)
    model.Minimize(sum(gap_time))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        optimized_schedule = [
            [solver.Value(assignment[i][j]) for j in range(num_rooms_guess)]
            for i in range(num_reservations)
        ]
        return optimized_schedule
    return None

def schedule_optimizer(reservations):
    max_rooms = len(reservations)
    min_rooms = 1

    # Binary search for the minimum number of rooms
    while min_rooms < max_rooms:
        mid = (min_rooms + max_rooms) // 2
        schedule = is_schedulable(reservations, mid)

        if schedule:
            max_rooms = mid
        else:
            min_rooms = mid + 1

    # Return the optimal schedule for the minimum number of rooms found
    return is_schedulable(reservations, min_rooms)

# Example reservations
reservations = [
    {"start": 8, "end": 10},
    {"start": 11, "end": 12},
    {"start": 13, "end": 15},
    {"start": 9, "end": 11},
    {"start": 10, "end": 12},
    {"start": 10, "end": 12},
    {"start": 10, "end": 12},
    {"start": 10, "end": 12},
    {"start": 14, "end": 16},
    {"start": 15, "end": 17},
    {"start": 16, "end": 18},
    {"start": 17, "end": 19},
    {"start": 18, "end": 20},
    {"start": 19, "end": 21},
    {"start": 20, "end": 22},
    {"start": 21, "end": 23},
    {"start": 22, "end": 24},
]


if __name__ == "__main__":
    optimized_schedule = schedule_optimizer(reservations)
    print("Optimized Schedule:")
    visualize_schedule(optimized_schedule, reservations)
    visualize_solution_plot(reservations, optimized_schedule, len(optimized_schedule[0]))


