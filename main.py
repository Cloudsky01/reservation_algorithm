from ortools.sat.python import cp_model
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def visualize_solution(reservations, assignments, num_rooms):
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

def schedule_optimizer(reservations, num_rooms):
    model = cp_model.CpModel()

    num_reservations = len(reservations)

    # Variables: assignment[i][j] is True if reservation i is assigned to room j
    assignment = [[model.NewBoolVar(f"assignment_{i}_{j}")
                   for j in range(num_rooms)]
                  for i in range(num_reservations)]

    # Each reservation is assigned to exactly one room
    for i in range(num_reservations):
        model.Add(sum(assignment[i]) == 1)

    # No overlapping reservations in the same room
    for j in range(num_rooms):
        for i1 in range(num_reservations):
            for i2 in range(i1 + 1, num_reservations):
                # If two reservations overlap, they can't be in the same room
                if not (reservations[i1]['end'] <= reservations[i2]['start'] or reservations[i1]['start'] >= reservations[i2]['end']):
                    model.Add(assignment[i1][j] + assignment[i2][j] <= 1)

    # Compute the gaps between reservations in the same room
    total_gap_time = model.NewIntVar(0, 24*60*num_rooms, "total_gap_time")
    gaps = []

    for j in range(num_rooms):
        for i1 in range(num_reservations):
            for i2 in range(i1 + 1, num_reservations):
                # If two reservations do not overlap and are in the same room, compute the gap
                if reservations[i1]['end'] <= reservations[i2]['start']:
                    gap = reservations[i2]['start'] - reservations[i1]['end']
                    gap_var = model.NewIntVar(0, 24*60, f"gap_{i1}_{i2}_{j}")
                    model.Add(gap_var == gap).OnlyEnforceIf([assignment[i1][j], assignment[i2][j]])
                    gaps.append(gap_var)

    model.Add(total_gap_time == sum(gaps))
    model.Minimize(total_gap_time)

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Print results
    if status == cp_model.OPTIMAL:
        print(f"Minimum total gap time: {solver.Value(total_gap_time)} minutes")
        for i in range(num_reservations):
            for j in range(num_rooms):
                if solver.Value(assignment[i][j]):
                    print(f"Reservation {i} -> Room {j}")
        visualize_solution(reservations, [[solver.Value(assignment[i][j]) for j in range(num_rooms)] for i in range(num_reservations)], num_rooms)
    else:
        print("No solution found!")


# Example data
reservations = [
    {"start": 8, "end": 10},
    {"start": 11, "end": 12},
    {"start": 13, "end": 14},
    {"start": 9, "end": 11},
    {"start": 10, "end": 12},
    {"start": 14, "end": 15},
    {"start": 15, "end": 16},
]

num_rooms = 2
assignment = schedule_optimizer(reservations, num_rooms)

