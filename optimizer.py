from classes import Sheet
from ortools.sat.python import cp_model

def getOptimizedSheet(sheet: Sheet):
    model = cp_model.CpModel()

    # Variables
    assignments_i_r = [[0 for _ in sheet.rooms] for _ in sheet.reservations]
    sol_i_s = [[] for _ in sheet.reservations]
    gap_r_t = [[0 for _ in range(sheet.endTime+1)] for _ in sheet.rooms]
    priority_list = [priority for priority in sheet.roomPriority]

    # Arrays to store assignements_i_r variables that start and end at time t in room r
    start_t_r = [[[] for _ in sheet.rooms] for _ in range(sheet.endTime+1)]
    end_t_r = [[[] for _ in sheet.rooms] for _ in range(sheet.endTime+1)]

    for i, reservation in enumerate(sheet.reservations):
        for r, room in enumerate(sheet.rooms):
            if room in reservation.suitableRooms:
                assignments_i_r[i][r] = model.NewBoolVar(f"assignment_i{i}_r{r}")

            # Store the variables that start and end at time t in room r
            start_t_r[reservation.startTime][r].append(assignments_i_r[i][r])
            end_t_r[reservation.endTime][r].append(assignments_i_r[i][r])

            # Contrainte 2
            for i2 in range(i):
                if sheet.reservations[i].endTime > sheet.reservations[i2].startTime and sheet.reservations[i].startTime < sheet.reservations[i2].endTime:
                    model.Add(assignments_i_r[i][r] + assignments_i_r[i2][r] <= 1)

            # Contrainte 3
            if room in reservation.wantedRooms:
                model.Add(assignments_i_r[i][r] == 1)
        
        # Contrainte 4
        model.Add(sum(assignments_i_r[i]) == len(reservation.wantedRooms))

        # Contrainte 5
        for s, solution in enumerate(reservation.connectedSolutions):
            sol_i_s[i].append(model.NewBoolVar(f"solution_i{i}_s{s}"))
            model.Add(
                sum([assignments_i_r[i][sheet.rooms.index(room)] for room in solution])
                >= sol_i_s[i][s] * len(solution)
            )

    # Contrainte 1
    for r, room in enumerate(sheet.rooms):
        for t in range(sheet.endTime+1):
            gap_r_t[r][t] = model.NewBoolVar(f"gap_r{r}_t{t}")
            model.Add(sum(end_t_r[t][r]) - sum(start_t_r[t][r]) <= gap_r_t[r][t])

    room_priority_penalty = sum(
        assignments_i_r[i][r] * -priority_list[r] for i in range(len(sheet.reservations)) for r in range(len(sheet.rooms))
    )

    model.Minimize(
        sum([sum(gap) for gap in gap_r_t]) - sum([sum(sol) for sol in sol_i_s]) + room_priority_penalty
    )

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        optimized_schedule = [
            [solver.Value(assignments_i_r[i][r]) for r in range(len(sheet.rooms))]
            for i in range(len(sheet.reservations))
        ]
        return optimized_schedule
    else:
        print("No solution found")
    return None
