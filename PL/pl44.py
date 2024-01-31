from gurobipy import Model, GRB

def pl4_gestion_de_la_production(months, demand, initial_stock, initial_workers, worker_monthly_wage, regular_hours_per_worker, max_overtime_hours, overtime_hourly_wage, production_time_per_pair, raw_material_cost, hired_cost, laid_off_cost, stock_cost_per_pair):
    # Initialize model
    model = Model("PL4_Gestion_de_la_production")

    # Decision variables
    production = [model.addVar(lb=0, vtype=GRB.INTEGER, name=f"production_{month}") for month in range(months)]
    stock = [model.addVar(lb=0, vtype=GRB.INTEGER, name=f"stock_{month}") for month in range(months)]
    workers = [model.addVar(lb=0, vtype=GRB.INTEGER, name=f"workers_{month}") for month in range(months)]
    overtime = [model.addVar(lb=0, vtype=GRB.INTEGER, name=f"overtime_{month}") for month in range(months)]
    hired = [model.addVar(lb=0, vtype=GRB.INTEGER, name=f"hired_{month}") for month in range(months)]
    laid_off = [model.addVar(lb=0, vtype=GRB.INTEGER, name=f"laid_off_{month}") for month in range(months)]
    

    # Constraints
    model.addConstr(stock[0] == initial_stock)
    model.addConstr(workers[0] == initial_workers)

    for month in range(months):
        # Production constraint
        model.addConstr(production[month] ==  (regular_hours_per_worker * workers[month] + overtime[month]) / production_time_per_pair)
        
        # Overtime constraint
        model.addConstr(overtime[month] <= max_overtime_hours * workers[month])
        
        # Stock and demand constraints
        if month > 0:
            model.addConstr(stock[month] == stock[month - 1] + production[month] - demand[month])
            model.addConstr(workers[month] == workers[month - 1] + hired[month] - laid_off[month])


    # Objective function
    cost = (
        sum((worker_monthly_wage * workers[month]) + (overtime[month] * overtime_hourly_wage) + (raw_material_cost * production[month]) + (stock_cost_per_pair * stock[month]) + (hired_cost * hired[month]) + (laid_off_cost * laid_off[month]) for month in range(months))
    )
    model.setObjective(cost, GRB.MINIMIZE)

    # Solve the model
    model.optimize()
    
    # save results
    output_str = "Optimal solution:\n"
    """
    for month in range(months):
        #output_str += f"Month {month + 1}:\n"
        output_str += f"  Production: {production[month].x}\n"
        output_str += f"  Stock: {stock[month].x}\n"
        output_str += f"  Workers: {workers[month].x}\n"
        output_str += f"  Overtime: {overtime[month].x}\n"
        output_str += f"  Hired: {hired[month].x}\n"
        output_str += f"  laid_off : {laid_off [month].x}\n"
        tab.append(output_str)
        output_str=""
    """
    
    tab = [[0 for j in range(months)] for i in range(6)]

    for month in range(months):
        
        tab[0][month]= production[month].x
        tab[1][month]= stock[month].x
        tab[2][month]= workers[month].x
        tab[3][month]= overtime[month].x
        tab[4][month]= hired[month].x
        tab[5][month]= laid_off[month].x
    
    output_str += f"Total cost = {model.objVal}"
    #print(output_str)
        
    return tab,output_str



"""
months = 3
demand = [3000, 5000, 2000]
initial_stock = 500
initial_workers = 100
worker_monthly_wage = 1500
regular_hours_per_worker = 160
max_overtime_hours = 20
overtime_hourly_wage = 13
production_time_per_pair = 4
raw_material_cost = 15
hired_cost = 1600
laid_off_cost = 2000
stock_cost_per_pair = 3

tab, total_cost = pl4_gestion_de_la_production(months, demand, initial_stock, initial_workers, worker_monthly_wage, regular_hours_per_worker, max_overtime_hours, overtime_hourly_wage, production_time_per_pair, raw_material_cost, hired_cost, laid_off_cost, stock_cost_per_pair)
print(tab)
"""


"""
# Example usage
months = 5
demand = [3000, 5000, 2000, 1000,1000]
initial_stock = 500
initial_workers = 100
worker_monthly_wage = 1500
regular_hours_per_worker = 160
max_overtime_hours = 20
overtime_hourly_wage = 13
production_time_per_pair = 4
raw_material_cost = 15
hired_cost = 1600
laid_off_cost = 2000
stock_cost_per_pair = 3

tab, total_cost = pl4_gestion_de_la_production(months, demand, initial_stock, initial_workers, worker_monthly_wage, regular_hours_per_worker, max_overtime_hours, overtime_hourly_wage, production_time_per_pair, raw_material_cost, hired_cost, laid_off_cost, stock_cost_per_pair)
for x in tab:
    print(x)
print("Total cost =", total_cost)

"""