# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 15:07:07 2023

@author: 21650
"""

from gurobipy import *

def pl1_gestion_optimale_d_une_zone_agricole(total_area, crop_data, total_labor, total_water, total_machine_time):
    # Initialize model
    model = Model("PL1_Gestion_optimale_d_une_zone_agricole")

    # Decision variables
    area = model.addVars(crop_data.keys(), lb=0, ub=total_area, name="area")

    # Constraints
    model.addConstr(sum(area[crop] for crop in crop_data.keys()) <= total_area, "total_area_constraint")
    model.addConstr(sum(crop_data[crop]["labor"] * area[crop] for crop in crop_data.keys()) <= total_labor, "total_labor_constraint")
    model.addConstr(sum(crop_data[crop]["water"] * area[crop] for crop in crop_data.keys()) <= total_water, "total_water_constraint")
    model.addConstr(sum(crop_data[crop]["machine_time"] * area[crop] for crop in crop_data.keys()) <= total_machine_time, "total_machine_time_constraint")

    # Objective function
    revenue = sum(crop_data[crop]["yield"] * crop_data[crop]["price"] * area[crop] for crop in crop_data.keys()) - sum((crop_data[crop]["salary"] * crop_data[crop]["labor"] * area[crop]) + (crop_data[crop]["fixed_cost"] * area[crop]) for crop in crop_data.keys())
    model.setObjective(revenue, GRB.MAXIMIZE)

    # Solve the model
    model.optimize()

    # Print results
    result = {}
    for crop in crop_data.keys():
        result[crop] = area[crop].x

    return result, model.objVal
"""

#test
table_values1 = [['75', '60', '55', '50', '60'], ['60', '50', '66', '110', '60'], ['2', '1', '2', '3', '2'], 
['30', '24', '20', '28', '25'], ['3000', '2000', '2500', '3800', '3200'], ['500', '500', '600', '700', '550'], ['250', '180', '190', '310', '320'], ['Blé', 'Orge', 'Mais', 'Bet-sucre', 'Tournesol']]

total_area = 1000
crop_names = table_values1[7]

crop_data = {}
for i, crop_name in enumerate(crop_names):
    crop_data[crop_name] = {
        "yield": int(table_values1[0][i]),
        "price": int(table_values1[1][i]),
        "labor": int(table_values1[2][i]),
        "machine_time": int(table_values1[3][i]),
        "water": int(table_values1[4][i]),
        "salary": int(table_values1[5][i]),
        "fixed_cost": int(table_values1[6][i]),
    }

total_labor = 3000
total_water = 25000000

total_machine_time = 24000

areas, revenue = pl1_gestion_optimale_d_une_zone_agricole(total_area, crop_data, total_labor, total_water, total_machine_time)

# Save the printed output to a string
output_string = "Optimal solution:\n"
for crop in crop_data.keys():
    output_string += f"Area for {crop}: {areas[crop]} hectares\n"
output_string += f"Total revenue: {revenue} UM\n"

# Print the output string
print(output_string)
"""