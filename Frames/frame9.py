import tkinter
import customtkinter

from tableClass import CustomTable
from PL.pl9 import tomo_optimization
from func import  matrix_dimensions, cast_table_to_int, cast_table_to_float

class MyFrame9(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        La = tkinter.StringVar(value="Veuillez entrer les données")
        L1 = customtkinter.CTkLabel(self,textvariable=La,width=120,height=25,corner_radius=8,
                                    font=("Helvetica", 32, "bold"))
        L1.grid(row=0, column=0, padx=20, pady=10,sticky="w")
        Lb = tkinter.StringVar(value="Résultats")
        L2 = customtkinter.CTkLabel(self,textvariable=Lb,width=120,height=25,corner_radius=8,
                                    font=("Helvetica", 32, "bold"))
        L2.grid(row=4, column=0, padx=20, pady=10)

        # table 1 inputs 
        row_headers=['nb_usines', 'offres','couts_usines_fixe','nb_depot', 'couts_depot_fixe', 'nb_clients','demandes']
        global default_values
        default_values= [[5], ["300,200,300,200,400"], ["35000,45000,40000,42000,40000"],[3],['40000,20000,60000'],[4], ["200,300,150,250"]]
        rows, columns = matrix_dimensions(default_values)
        self.table = CustomTable(self, rows, columns, default_values, row_headers=row_headers,widthval=250)
        self.table.grid(row=1, column=0, padx=20, pady=10,sticky="w")
        
        #get values from the table 1 
        def get_values(self):
            global table_values
            table_values = self.table.get_table_values()
            global nb_usines, offres, couts_usines_fixe, nb_depot, couts_depot_fixe, nb_clients, demandes
            vars =[]
            for i in range(len(table_values)):
                vars.append(table_values[i][0])
            for i in range(len(vars)):
                if i != 1 and i != 2 and i != 4 and i != 6 :
                    vars[i]= int(vars[i])
                else:
                    vars[i]=[int(x) for x in vars[i].split(",")]
            #print(vars)
            nb_usines=vars[0]
            offres=vars[1]
            couts_usines_fixe=vars[2]
            nb_depot=vars[3]
            couts_depot_fixe=vars[4]
            nb_clients=vars[5]
            demandes=vars[6]


# table inputs 2
        column_headers=["Dépôt 1","Dépôt 2","Dépôt 3"]
        row_headers=["Usine 1", "Usine 2", "Usine 3", "Usine 4", "Usine 5"]
        global default_values2
        default_values2 = [[800,1000,1200],[700 ,500,700 ],
                    [800 ,600,500],[500 ,600,700],
                    [700,600,500]]
        rows, columns = matrix_dimensions(default_values2)
        self.table2 = CustomTable(self, rows, columns, default_values2, row_headers=row_headers, column_headers=column_headers)
        self.table2.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        def get_values2(self):
            global table_values2
            table_values2 = self.table2.get_table_values()
            table_values2=cast_table_to_float(table_values2)
            #print(table_values2)
        #self.getvals = customtkinter.CTkButton(self, text="set values tab 2",font=("Helvetica", 16, "bold"),command=lambda: get_values2(self))
        #self.getvals.grid(row=2, column=1, padx=20, pady=10)


# table inputs 3
        column_headers=["Client 1", "Client 2", "Client 3", "Client 4"]
        row_headers=["Dépot 1","Dépot 2","Dépot 3"]
        global default_values3
        default_values3 = [[40, 80, 90, 50],[70, 40, 60, 80],[80, 30, 50, 60]]
        rows, columns = matrix_dimensions(default_values3)
        self.table3 = CustomTable(self, rows, columns, default_values3, row_headers=row_headers, column_headers=column_headers)
        self.table3.grid(row=1, column=2, padx=20, pady=10, sticky="w")

        def get_values3(self):
            global table_values3
            table_values3 = self.table3.get_table_values()
            #cast table_values2 to int
            table_values3=cast_table_to_float(table_values3)
            #print(table_values3)
        def get_all_values(self):
            get_values(self)
            get_values2(self)
            get_values3(self)
        
        self.getvals = customtkinter.CTkButton(self, text="set values",
                                                    font=("Helvetica", 16, "bold"),
                                                    command=lambda: get_all_values(self))
        self.getvals.grid(row=3, column=1, padx=20, pady=10,sticky="s")

########### resize tables ################
        def resize_tables(self):
            get_all_values(self)
            CustomTable.resize_table2(self, int(nb_usines), int(nb_depot),1,1, "Dépôt","Usine",table="table2")
            CustomTable.resize_table3(self, int(nb_depot), int(nb_clients),1,2, "client","Dépôt",table="table3")

        self.getvals = customtkinter.CTkButton(self, text="resize tables",
                                                    font=("Helvetica", 16, "bold"),
                                                    command=lambda: resize_tables(self))
        self.getvals.grid(row=3, column=2, padx=20, pady=10,sticky="s")

################ solver #####################
        def diplay_results(nb_usines, nb_depot, clients, production_capacity, prod_to_depot_cost, depot_to_client_cost, client_demand, couts_usines_fixe, couts_depot_fixe):
            global results_label
            try:
                results_label.destroy()
            except:
                pass  
            # Define data
            Usines = ["Usine" + " " + str(i) for i in range(1, nb_usines+1)]
            depots = ["Depot" + " " + str(i) for i in range(1, nb_depot+1)]
            clients= ["Client" + " " + str(i) for i in range(1, nb_clients+1)]
            production_capacity = offres 
            prod_to_depot_cost = table_values2
            depot_to_client_cost = table_values3
            client_demand = demandes
            fixed_costs = couts_usines_fixe + couts_depot_fixe

            results = tomo_optimization(Usines, depots, clients,
                                        production_capacity, prod_to_depot_cost,
                                        depot_to_client_cost, client_demand, fixed_costs)
            results_text = tkinter.StringVar(value=results)
            results_label = customtkinter.CTkLabel(self,textvariable=results_text,
                                                   fg_color=("white", "gray20"),
                                                   corner_radius=8,
                                                   font=("Helvetica", 16, "bold"),
                                                   justify="left",
                                                   anchor="nw"
                                                   )
            results_label.grid(row=5, column=0, padx=20, pady=10)
        self.solvebutton = customtkinter.CTkButton(self,  text="solve",
                                                   font=("Helvetica", 16, "bold"),
                                                   fg_color=("#48ab79", "gray20"),
                                                   hover_color=("#327855","gray20"),
                                                   command=lambda:diplay_results(nb_usines, nb_depot, nb_clients, offres, table_values2, table_values3, demandes, couts_usines_fixe,couts_depot_fixe))
        self.solvebutton.grid(row=5, column=1, padx=20, pady=10,stick="n")







################reset frame#####################
        def reset():
            self.table.destroy()
            self.table2.destroy()
            self.table3.destroy()
            try:
                results_label.destroy()
            except:
                pass    
        # table reset 
            row_headers=['nb_usines', 'offres','couts_usines_fixe','nb_depot', 'couts_depot_fixe', 'nb_clients','demandes']
            default_values= [[5], ["300,200,300,200,400"], ["35000,45000,40000,42000,40000"],[3],['40000,20000,60000'],[4], ["200,300,150,250"]]
            rows, columns = matrix_dimensions(default_values)
            self.table = CustomTable(self, rows, columns, default_values, row_headers=row_headers,widthval=250)
            self.table.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        # table2 reset 
            column_headers=["Dépôt 1","Dépôt 2","Dépôt 3"]
            row_headers=["Usine 1", "Usine 2", "Usine 3", "Usine 4", "Usine 5"]
            default_values2 = [[800,1000,1200],[700 ,500,700 ],
                        [800 ,600,500],[500 ,600,700],
                        [700,600,500]]
            rows, columns = matrix_dimensions(default_values2)
            self.table2 = CustomTable(self, rows, columns, default_values2, row_headers=row_headers, column_headers=column_headers)
            self.table2.grid(row=1, column=1, padx=20, pady=10,sticky="w")
        # table3 reset
            column_headers=["Client 1", "Client 2", "Client 3", "Client 4"]
            row_headers=["Dépot 1","Dépot 2","Dépot 3"]
            global default_values3
            default_values3 = [[40, 80, 90, 50],[70, 40, 60, 80],
                    [80, 30, 50, 60]]
            rows, columns = matrix_dimensions(default_values3)
            self.table3 = CustomTable(self, rows, columns, default_values3, row_headers=row_headers, column_headers=column_headers)
            self.table3.grid(row=1, column=2, padx=20, pady=10, sticky="w")
        self.resetbutton = customtkinter.CTkButton(self, text="reset",
                                                    font=("Helvetica", 16, "bold"),
                                                    hover_color=("#8a3838", "gray20"),
                                                    fg_color=("#bf4e4e", "gray20"), command=lambda: reset())
        self.resetbutton.grid(row=3, column=3, padx=20, pady=10,stick="s")

