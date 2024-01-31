# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 02:37:21 2023

@author: 21650
"""

import gurobipy as gp
from gurobipy import GRB

def optimal_electricity_supply_with_penalties(supply, demand, transport_costs, penalties):
    # Create the model
    model = gp.Model("electricity_supply_with_penalties")

    # Add decision variables for electricity supply
    x = {}
    for i in range(len(supply)):
        for j in range(len(demand)):
            x[i, j] = model.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}_{j}")

    # Add decision variables for unsatisfied demand
    y = {}
    for j in range(len(demand)):
        y[j] = model.addVar(vtype=GRB.CONTINUOUS, name=f"y_{j}")

    # Set the objective function
    model.setObjective(
        sum(x[i, j] * transport_costs[i][j] for i in range(len(supply)) for j in range(len(demand)))
        + sum(y[j] * penalties[j] for j in range(len(demand))),
        GRB.MINIMIZE,
    )

    # Add supply constraints
    for i in range(len(supply)):
        model.addConstr(sum(x[i, j] for j in range(len(demand))) <= supply[i], f"supply_{i}")

    # Add modified demand constraints
    for j in range(len(demand)):
        model.addConstr(sum(x[i, j] for i in range(len(supply))) + y[j] >= demand[j], f"demand_{j}")

    # Optimize the model
    model.optimize()

    # Collect the optimal solution
    if model.status == GRB.Status.OPTIMAL:
        solution = []
        for i in range(len(supply)):
            for j in range(len(demand)):
                if x[i, j].x > 0:
                    solution.append((i, j, x[i, j].x))
        unsatisfied_demand = [y[j].x for j in range(len(demand))]
        return solution, unsatisfied_demand, model.objVal
    else:
        return None, None, None


"""
# Test the function with the updated data
supply = [35, 50, 40]
demand = [45, 20, 30, 30]
transport_costs = [
    [8, 6, 10, 9],
    [9, 12, 13, 7],
    [14, 9, 16, 5]
]

increased_demand = [d +5 for d in demand]
penalties = [20, 25, 22, 35]
#penalties = [0, 0, 0, 0]

solution, unsatisfied_demand, obj_val = optimal_electricity_supply_with_penalties(supply, increased_demand, transport_costs, penalties)

if solution is not None:
    print("Optimal solution found:")
    for i, j, x_val in solution:
        print(f"Supply {x_val} million KWh from Centrale {i + 1} to Ville {j + 1}")
    print("Unsatisfied demand:", unsatisfied_demand)
    print("Objective value:", obj_val)
else:
    print("No optimal solution found.")
"""