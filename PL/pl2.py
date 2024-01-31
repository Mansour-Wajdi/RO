from gurobipy import Model, GRB

def optimize_petroleum_mix(brut1, brut2, qualite_brut1, qualite_brut2, qualite_gazoline, qualite_petrole_chauffage, prix_gazoline, prix_petrole_chauffage, frais_marketing_gazoline, frais_marketing_petrole_chauffage):
    # Modèle
    #print(brut1, brut2, qualite_brut1, qualite_brut2, qualite_gazoline, qualite_petrole_chauffage, prix_gazoline, prix_petrole_chauffage, frais_marketing_gazoline, frais_marketing_petrole_chauffage)
    model = Model("Mixage_optimal")

    # Variables de décision
    x = model.addVar(lb=0, ub=brut1, name="x")  # Quantité de brut1 utilisée pour la gazoline
    y = model.addVar(lb=0, ub=brut2, name="y")  # Quantité de brut2 utilisée pour la gazoline

    # Contraintes
    model.addConstr(qualite_brut1 * x + qualite_brut2 * y >= qualite_gazoline * (x + y), "Qualite_gazoline")
    model.addConstr(qualite_brut1 * (brut1 - x) + qualite_brut2 * (brut2 - y) >= qualite_petrole_chauffage * (brut1 + brut2 - x - y), "Qualite_petrole_chauffage")

    # Fonction objectif
    revenu_gazoline = (prix_gazoline - frais_marketing_gazoline) * (x + y)
    revenu_petrole_chauffage = (prix_petrole_chauffage - frais_marketing_petrole_chauffage) * (brut1 + brut2 - x - y)
    model.setObjective(revenu_gazoline + revenu_petrole_chauffage, GRB.MAXIMIZE)

    # Résoudre le modèle
    model.optimize()

    # Résultats
    results = {
        "brut1_gazoline": x.x,
        "brut2_gazoline": y.x,
        "brut1_petrole_chauffage": brut1 - x.x,
        "brut2_petrole_chauffage": brut2 - y.x,
        "revenu_total": model.objVal
    }
    
    return results
"""
# Example usage:
params = {
    "brut1": 5000,
    "brut2": 10000,
    "qualite_brut1": 10,
    "qualite_brut2": 5,
    "qualite_gazoline": 8,
    "qualite_petrole_chauffage": 6,
    "prix_gazoline": 25,
    "prix_petrole_chauffage": 20,
    "frais_marketing_gazoline": 0.2,
    "frais_marketing_petrole_chauffage": 0.1
}

results = optimize_petroleum_mix(**params)
print(results)
"""