import gurobipy as gp
from gurobipy import GRB

def tomo_optimization(Usines, depots, clients, production_capacity, prod_to_depot_cost, depot_to_client_cost, client_demand, fixed_costs):

    # Create model
    model = gp.Model("Tomo")

    # Add variables
    x = model.addVars(Usines, depots, obj=prod_to_depot_cost, name="x")
    y = model.addVars(depots, clients, obj=depot_to_client_cost, name="y")
    z = model.addVars(Usines + depots, obj=fixed_costs, vtype=GRB.BINARY, name="z")

    # Add constraints
    model.addConstrs((gp.quicksum(x[p, d] for p in Usines) == gp.quicksum(y[d, c] for c in clients) for d in depots), name="DepotBalance")
    model.addConstrs((gp.quicksum(x[p, d] for d in depots) <= production_capacity[Usines.index(p)] * z[p] for p in Usines), name="ProductionCapacity")
    model.addConstrs((gp.quicksum(y[d, c] for d in depots) >= client_demand[clients.index(c)] for c in clients), name="DemandSatisfaction")

    # Set objective
    model.setObjective(gp.quicksum(z[p] * fixed_costs[Usines.index(p)] for p in Usines) + gp.quicksum(z[d] * fixed_costs[len(Usines) + depots.index(d)] for d in depots) + gp.quicksum(x[p, d] * prod_to_depot_cost[Usines.index(p)][depots.index(d)] for p in Usines for d in depots) + gp.quicksum(y[d, c] * depot_to_client_cost[depots.index(d)][clients.index(c)] for d in depots for c in clients), GRB.MINIMIZE)

    # Optimize model
    model.optimize()

    # Store the results in a string variable
    if model.status == GRB.Status.OPTIMAL:
        results = "Optimal solution found:\n"
        for p, d in x.keys():
            if x[p, d].x > 1e-6:
                results += f"Produce and transport {x[p, d].x:.2f} tons from {p} to {d}\n"
        for d, c in y.keys():
            if y[d, c].x > 1e-6:
                results += f"Transport {y[d, c].x:.2f} tons from {d} to {c}\n"
        for p in Usines:
            if z[p].x > 1e-6:
                results += f"{p} is open\n"
        for d in depots:
            if z[d].x > 1e-6:
                results += f"{d} is open\n"
        results += f"Objective value: {model.objVal:.2f}"
    else:
        results = "No optimal solution found."

    return results
"""
# Define data
nb_usines = 5
Usines = ["Usine" + " " + str(i) for i in range(1, nb_usines+1)]
nb_depot = 3
depots = ["Depot" + " " + str(i) for i in range(1, nb_depot+1)]
nb_clients = 4
clients = ["Client" + " " + str(i) for i in range(1, nb_clients+1)]


production_capacity = [300, 200, 300, 200, 400]
prod_to_depot_cost = [
    [800, 1000, 1200],
    [700, 500, 700],
    [800, 600, 500],
    [500, 600, 700],
    [700, 600, 500]
]
depot_to_client_cost = [
    [40, 80, 90, 50],
    [70, 40, 60, 80],
    [80, 30, 50, 60]
]
client_demand = [200, 300, 150, 250]
fixed_costs = [35000, 45000, 40000, 42000, 40000, 40000, 20000, 60000]

# Call the function and print the results
results = tomo_optimization(Usines, depots, clients,
                             production_capacity, prod_to_depot_cost,
                               depot_to_client_cost, client_demand, fixed_costs)
print(results)
"""