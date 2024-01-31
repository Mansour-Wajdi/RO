import gurobipy as gp
from gurobipy import GRB

def optimal_electricity_supply(centrales, villes, offres, demandes, couts_transport, penalites):
    # Create model
    model = gp.Model("Probleme d'electricite")

    # Create variables
    x = model.addVars(centrales, villes, vtype=GRB.CONTINUOUS, name="x")

    # Set objective function
    obj = gp.quicksum(x[c, v] * couts_transport[c, v] for c in centrales for v in villes)
    obj += gp.quicksum((demandes[v] - gp.quicksum(x[c, v] for c in centrales)) * penalites[v] for v in villes)
    model.setObjective(obj, GRB.MINIMIZE)

    # Set constraints
    for c in centrales:
        model.addConstr(gp.quicksum(x[c, v] for v in villes) <= offres[c], name=f"Contrainte capacite {c}")

    for v in villes:
        model.addConstr(gp.quicksum(x[c, v] for c in centrales) >= demandes[v], name=f"Contrainte demande {v}")

    # Solve model
    model.optimize()

    # Print solution
    result_str = "Solution optimale :\n"
    for c in centrales:
        for v in villes:
            if x[c, v].x > 0:
                result_str += f"{x[c, v].x:.2f} millions de Kwh de la centrale {c} sont transportes a la ville {v}\n"
    result_str += f"Cout total : {obj.getValue():.2f} millions d'euros"

    unsatisfied_demand = {v: demandes[v] - sum(x[c, v].x for c in centrales) for v in villes}
    print("Demande insatisfaite :")
    for v in villes:
        if unsatisfied_demand[v] > 0:
            print(f"Il manque {unsatisfied_demand[v]:.2f} millions de Kwh a la ville {v}")
            
    return obj.getValue(), unsatisfied_demand,result_str






"""
# set data

nb_centrales = 3
offres_list = [35,50,40]
nb_villes = 4
demandes_list=[45,20,30,30]
penalites_list=[20,25,22,35]
all_couts = [[8, 6, 10, 9], [9, 12, 13, 7], [14, 9, 16, 5]]

#formate data 
string = "centrale"
centrales = [f"{string.capitalize()} {i}" for i in range(1, nb_centrales+1)]
string = "Ville"
villes = [f"{string.capitalize()} {i}" for i in range(1, nb_villes+1)]
offres = dict(zip(centrales, offres_list))
demandes = dict(zip(villes, demandes_list))
penalites = dict(zip(villes, penalites_list))
couts_transport = {}
for i, c in enumerate(centrales):
    for j, v in enumerate(villes):
        couts_transport[(c, v)] = all_couts[i][j]



# Solve problem
total_cost, unsatisfied_demand, resultat = optimal_electricity_supply(centrales, villes, offres, demandes, couts_transport, penalites)


# Print results
print(f"Cout total : {total_cost:.2f} millions d'euros")
for v in villes:
    if unsatisfied_demand[v] > 0:
        print("Demande insatisfaite :")
        break

for v in villes:
    if unsatisfied_demand[v] > 0:
        print(f"Il manque {unsatisfied_demand[v]:.2f} millions de Kwh a la ville {v}")
"""