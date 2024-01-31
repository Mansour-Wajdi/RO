
import gurobipy as gp
from gurobipy import GRB

def optimal_electricity_supply(supply, demand, transport_costs):
    # Create the model
    model = gp.Model("electricity_supply")

    # Add decision variables
    x = {}
    for i in range(len(supply)):
        for j in range(len(demand)):
            x[i, j] = model.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}_{j}")

    # Set the objective function
    model.setObjective(sum(x[i, j] * transport_costs[i][j] for i in range(len(supply)) for j in range(len(demand))), GRB.MINIMIZE)

    # Add supply constraints
    for i in range(len(supply)):
        model.addConstr(sum(x[i, j] for j in range(len(demand))) <= supply[i], f"supply_{i}")

    # Add demand constraints
    for j in range(len(demand)):
        model.addConstr(sum(x[i, j] for i in range(len(supply))) >= demand[j], f"demand_{j}")

    # Optimize the model
    model.optimize()

    # Collect the optimal solution
    if model.status == GRB.Status.OPTIMAL:
        solution = []
        for i in range(len(supply)):
            for j in range(len(demand)):
                if x[i, j].x > 0:
                    solution.append((i, j, x[i, j].x))
        return solution, model.objVal
    else:
        return None, None
"""
# Test the function with the provided data
supply = [35, 50, 40]
demand = [45, 20, 30, 30]
transport_costs = [
    [8, 6, 10, 9],
    [9, 12, 13, 7],
    [14, 9, 16, 5],
]

solution, obj_val = optimal_electricity_supply(supply, demand, transport_costs)

if solution is not None:
    print("Optimal solution found:")
    for i, j, x_val in solution:
        print(f"Supply {x_val} million KWh from Centrale {i + 1} to Ville {j + 1}")
    print("Objective value:", obj_val)
else:
    print("No optimal solution found.")

"""