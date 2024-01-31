import gurobipy as gp
from gurobipy import GRB
import numpy as np

def optimize_assignment(costs):
    num_companies = len(costs)
    num_projects = len(costs[0])

    # Create a model
    model = gp.Model("assignment")

    # Add binary decision variables
    x = model.addVars(num_companies, num_projects, vtype=GRB.BINARY, name="x")

    # Set the objective function
    model.setObjective(gp.quicksum(costs[i][j] * x[i, j] for i in range(num_companies) for j in range(num_projects) if not np.isnan(costs[i][j])), GRB.MINIMIZE)

    # Add constraints: exactly one company per project
    for j in range(num_projects):
        model.addConstr(gp.quicksum(x[i, j] for i in range(num_companies) if not np.isnan(costs[i][j])) == 1, f"project_{j}")

    # Add constraints: a company can take on at most two projects
    for i in range(num_companies):
        model.addConstr(gp.quicksum(x[i, j] for j in range(num_projects) if not np.isnan(costs[i][j])) <= 2, f"company_{i}")

    # Optimize the model
    model.optimize()

    # Collect the optimal solution
    if model.status == GRB.Status.OPTIMAL:
        assignment = []
        for i in range(num_companies):
            for j in range(num_projects):
                if not np.isnan(costs[i][j]) and x[i, j].x > 0.5:
                    assignment.append((i+1, j+1))
        return assignment, model.objVal
    else:
        return None, None

"""
# Test the function with the provided cost data
costs = [
    [np.nan, 8200, 7800, 5400, np.nan, 3900, np.nan, np.nan],
    [7800, 8200, np.nan, 6300, np.nan, 3300, 4900, np.nan],
    [np.nan, 4800, np.nan, np.nan, np.nan, 4400, 5600, 3600],
    [np.nan, np.nan, 8000, 5000, 6800, np.nan, 6700, 4200],
    [7200, 6400, np.nan, 3900, 6400, 2800, np.nan, 3000],
    [7000, 5800, 7500, 4500, 5600, np.nan, 6000, 4200]
]

assignment, obj_val = optimize_assignment(costs)
if assignment:
    optimal_solution = (
        "Optimal solution found:\n"
        + "\n".join(
            [f"Assign project {j} to company {i}" for i, j in assignment]
        )
        + f"\nObjective value: {obj_val}"
    )
else:
    optimal_solution = "No optimal solution found."

print(optimal_solution)
"""