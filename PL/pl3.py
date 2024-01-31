# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 05:25:22 2023

@author: 21650
"""

from gurobipy import *
def pl3_planification(days, min_required, work_days, rest_days):
    # Initialize model
    model = Model("PL3_Planification_des_besoins_en_ressources_humaines")
    # Decision variables
    employees = model.addVars(days, lb=0, vtype=GRB.INTEGER, name="employees")
    # Constraints
    for i in range(days):
        model.addConstr(quicksum(employees[(i - j) % days] for j in range(work_days)) >= min_required[i], f"staffing_constraint_{i}")
    # Objective function
    total_employees = quicksum(employees[i] for i in range(days))
    model.setObjective(total_employees, GRB.MINIMIZE)
    # Solve the model
    model.optimize()
    # Print results
    output_str = "Optimal solution :\n"
    for i in range(days):
        output_str += f"Employees starting on day {i + 1}: {employees[i].x}\n"
    output_str += f"Total number of employees = {model.objVal}"

    return(output_str)

"""
# Example usage
days = 7
min_required = [17, 13, 15, 19, 14, 16, 11]
work_days=5
rest_days=2
pl3_planification(days, min_required,work_days,rest_days)
"""