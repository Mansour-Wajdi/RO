import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow
import pandas as pd
import numpy as np

import gurobipy as gp
from gurobipy import GRB


def optimize_distribution(usines, clients, depots, capacities, client_demands, transport_costs_matrix):
    # Create the model
    m = gp.Model("distribution")

    # Add decision variables
    nodes = transport_costs_matrix.index
    x = {}
    for i in nodes:
        for j in nodes:
            if not np.isnan(transport_costs_matrix.at[i, j]):
                x[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f"x_{i}_{j}")

    # Set the objective function
    m.setObjective(sum(x[i, j] * transport_costs_matrix.at[i, j] for i, j in x.keys()), GRB.MINIMIZE)

    # Add constraints
    # Capacity constraints
    for i, capacity in zip(usines, capacities):
        m.addConstr(sum(x[i, j] for j in nodes if (i, j) in x) <= capacity, f"capacity_{i}")

    # Demand constraints
    for j, demand in zip(clients, client_demands):
        m.addConstr(sum(x[i, j] for i in nodes if (i, j) in x) >= demand, f"demand_{j}")

    # Flow constraints
    for depot in depots:
        m.addConstr(sum(x[i, depot] for i in nodes if (i, depot) in x) ==
                   sum(x[depot, j] for j in nodes if (depot, j) in x), f"flow_{depot}")

    # Max transport constraints
    for i, j in x.keys():
        m.addConstr(x[i, j] <= 200, f"max_transport_{i}_{j}")

    # Optimize the model
    m.optimize()
    # Collect the optimal solution
    if m.status == GRB.Status.OPTIMAL:
        solution = []
        for i, j in x.keys():
            if x[i, j].x > 0:
                solution.append((i, j, x[i, j].x))
        return solution, m.objVal
    else:
        return None, None

"""
# Test the function with the provided data
usines = ["usine 1", "usine 2", "usine 3"]
clients = ["Client 1", "Client 2"]
depots = ["Dépot 1", "Dépot 2"]

capacities = [200, 300, 100]
client_demands = [400, 180]

transport_costs_matrix = pd.DataFrame(
    [
        [np.nan, 5, 3, 5, 5, 20, 20],
        [9, np.nan, 9, 1, 1, 8, 15],
        [0.4, 8, np.nan, 1, 0.5, 10, 12],
        [np.nan, np.nan, np.nan, np.nan, 1.2, 2, 12],
        [np.nan, np.nan, np.nan, 8, np.nan, 2, 12],
        [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 1],
        [np.nan, np.nan, np.nan, np.nan, np.nan, 7, np.nan],
    ],
    columns=usines + depots + clients,
    index=usines + depots + clients,
)

solution, obj_val = optimize_distribution(usines, clients, depots, capacities, client_demands, transport_costs_matrix)

result = ""

if solution is not None:
    result += "Optimal solution found:\n"
    for i, j, x_val in solution:
        result += f"Transport {x_val} tonnes from {i} to {j}\n"
    result += f"Objective value: {obj_val}\n"
else:
    result += "No optimal solution found.\n"

print(result)
"""