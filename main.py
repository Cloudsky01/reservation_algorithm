from ortools.sat.python import cp_model

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
    else:
        print("No solution found!")


# Example data
reservations = [
    {"start": 8, "end": 10},
    {"start": 11, "end": 12},
    {"start": 13, "end": 14},
    {"start": 9, "end": 11},
]

num_rooms = 2
schedule_optimizer(reservations, num_rooms)
