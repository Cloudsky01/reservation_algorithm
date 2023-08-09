from ortools.linear_solver import pywraplp

def schedule_optimizer():
    # Create the solver
    solver = pywraplp.Solver.CreateSolver('GLOP')

    # Data
    workers = ['Worker_1', 'Worker_2', 'Worker_3']
    tasks = ['Task_1', 'Task_2', 'Task_3', 'Task_4']

    time_matrix = [
        [2, 4, 5, 6],  # Time taken for Worker_1 for each task
        [3, 2, 3, 1],  # Time taken for Worker_2 for each task
        [5, 3, 2, 8]   # Time taken for Worker_3 for each task
    ]

    # Variables
    # x[i][j] is an array of 0/1 variables, which will be 1 if worker i is assigned to task j.
    x = []
    for i in range(len(workers)):
        x.append([])
        for j in range(len(tasks)):
            x[i].append(solver.BoolVar(f'x[{i}][{j}]'))

    # Constraints
    # Each worker is assigned to at most one task.
    for i in range(len(workers)):
        solver.Add(sum(x[i][j] for j in range(len(tasks))) <= 1)

    # Each task is assigned to exactly one worker.
    for j in range(len(tasks)):
        solver.Add(sum(x[i][j] for i in range(len(workers))) == 1)

    # Objective
    objective_terms = []
    for i in range(len(workers)):
        for j in range(len(tasks)):
            objective_terms.append(time_matrix[i][j] * x[i][j])
    solver.Minimize(solver.Sum(objective_terms))

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Objective value =', solver.Objective().Value())
        for i in range(len(workers)):
            for j in range(len(tasks)):
                if x[i][j].solution_value():
                    print(f'{workers[i]} assigned to {tasks[j]} taking {time_matrix[i][j]} hours.')
    else:
        print('The problem does not have an optimal solution.')

if __name__ == '__main__':
    schedule_optimizer()
