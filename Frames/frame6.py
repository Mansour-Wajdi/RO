import tkinter
import customtkinter
import pandas as pd
import numpy as np
from tableClass import CustomTable

from func import  matrix_dimensions

from PL.pl66 import optimize_distribution 
from PL.pl6Graph import test_data 


class MyFrame6(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        La = tkinter.StringVar(value="Veuillez entrer les données")
        L1 = customtkinter.CTkLabel(self,textvariable=La,width=120,height=25,corner_radius=8,
                                    font=("Helvetica", 32, "bold"))
        L1.grid(row=0, column=0, padx=20, pady=10,sticky="w")
        Lb = tkinter.StringVar(value="Résultats")
        L2 = customtkinter.CTkLabel(self,textvariable=Lb,width=120,height=25,corner_radius=8,
                                    font=("Helvetica", 32, "bold"))
        L2.grid(row=3, column=0, padx=20, pady=10)

######### table 1 #########
        row_headers=['nb_usines', 'capacité de production','nb_clients','demandes', 'nombres dépôts','max_transport']
        global default_values1
        default_values1= [[3], ["200,300,100"],[2],['400,180'],[2],[200]]
        rows1, columns1 = matrix_dimensions(default_values1)
        self.table1 = CustomTable(self, rows1, columns1, default_values1, row_headers=row_headers,widthval=250)
        self.table1.grid(row=1, column=0, padx=20, pady=10,sticky="w")
    ################ getter 1 #####################
        def get_values1(self):
            global nb_usines, capacite_production, nb_clients, demandes, nb_depot,max_transport
            table_values1 = self.table1.get_table_values()
            vars =[]
            for i in range(len(table_values1)):
                vars.append(table_values1[i][0])
            for i in range(len(vars)):
                if i != 1 and i != 3:
                    vars[i]= int(vars[i])
                else:
                    vars[i]=[int(x) for x in vars[i].split(",")]
            print(vars)
            nb_usines=vars[0]
            capacite_production=vars[1]
            nb_clients=vars[2]
            demandes=vars[3]
            nb_depot=vars[4]
            max_transport=vars[5]

######### table 2 #########
        column_headers=["usine 1", "usine 2", "usine 3", "Dépot 1", "Dépot 2", "Client 1", "Client 2"]
        row_headers=["usine 1", "usine 2", "usine 3", "Dépot 1", "Dépot 2", "Client 1", "Client 2"]
        global default_values 
        default_values = [
            [float('nan'), 5, 3, 5, 5, 20, 20],
            [9, float('nan'), 9, 1, 1, 8, 15],
            [0.4, 8, float('nan'), 1, 0.5, 10, 12],
            [float('nan'), float('nan'), float('nan'), float('nan'), 1.2, 2, 12],
            [float('nan'), float('nan'), float('nan'), 8, float('nan'), 2, 12],
            [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 1],
            [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 7, float('nan')]
        ]
        rows, columns = matrix_dimensions(default_values)
        self.table = CustomTable(self, rows, columns, default_values, row_headers=row_headers, column_headers=column_headers)
        self.table.grid(row=2, column=0, padx=20, pady=10,sticky="w")
        
    ######### getter 2 #########
        def get_values(self):
            global table_values
            table_values = self.table.get_table_values()
            for i in range(len(table_values)):
                for j in range(len(table_values[i])):
                    table_values[i][j]=float(table_values[i][j])
        def get_all_values(self):
            get_values(self)
            get_values1(self)
        self.getvals = customtkinter.CTkButton(self, text="set values",
                                                    font=("Helvetica", 16, "bold"),
                                                     command=lambda: get_all_values(self))
        self.getvals.grid(row=2, column=1, padx=20, pady=10,sticky="s")


######### graphe #########
        def diplay_graph(table_values):

            col = ["usine" + " " + str(i) for i in range(1, nb_usines+1)]+["Dépot" + " " + str(i) for i in range(1, nb_depot+1)]+["Client" + " " + str(i) for i in range(1, nb_clients+1)]

            transport_costs_matrix = pd.DataFrame(
            table_values,
            columns=col,
            index=col,
            )
            test_data(transport_costs_matrix)
        self.graphbutton = customtkinter.CTkButton(self, text="graph",
                                                    font=("Helvetica", 16, "bold"),
                                                    command=lambda: diplay_graph(table_values))
        self.graphbutton.grid(row=4, column=2, padx=20, pady=10,sticky="n")

        def resize(self):
            get_all_values(self)

            CustomTable.resize_table6(self, nb_usines, nb_usines,nb_depot,nb_depot,nb_clients,nb_clients,
                                      2,0,"usine" ,"usine","depot" ,"depot","client","client")


################ resize #####################

        self.getvals = customtkinter.CTkButton(self, text="resize table",
                                                    font=("Helvetica", 16, "bold"),
                                                    command=lambda: resize(self))
        self.getvals.grid(row=2, column=2, padx=20, pady=10,sticky="s")

################ solver #####################
        def diplay_results(table_values):
            global results_label1
            try: 
                results_label1.destroy()
            except:
                pass


            # Test the function with the provided data
            usines = ["usine" + " " + str(i) for i in range(1, nb_usines+1)]
            clients = ["Client" + " " + str(i) for i in range(1, nb_clients+1)]
            depots = ["Dépot" + " " + str(i) for i in range(1, nb_depot+1)]
            
            capacities = capacite_production
            client_demands = demandes

            transport_costs_matrix = pd.DataFrame(
                table_values,
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




            # Create a new CTkLabel with the string representation as the text
            results_label1 = customtkinter.CTkLabel(self,text=result,
                                                   fg_color=("white", "gray20"),
                                                   corner_radius=8,
                                                   font=("Helvetica", 16, "bold"),
                                                   justify="left",
                                                   anchor="nw"
                                                   )
            results_label1.grid(row=4, column=0, padx=20, pady=10)
        self.solvebutton = customtkinter.CTkButton(self,  text="solve",
                                                   font=("Helvetica", 16, "bold"),
                                                   fg_color=("#48ab79", "gray20"),
                                                   hover_color=("#327855","gray20"),
                                                   command=lambda: diplay_results(table_values))
        self.solvebutton.grid(row=4, column=1, padx=20, pady=10,sticky="n")



################reset frame#####################
        def reset():
            self.table.destroy()
            self.table1.destroy()
            try:
                results_label1.destroy()
            except:
                pass    

            row_headers1=['nb_usines', 'capacité de production','nb_clients','demandes', 'nombres dépôts','max_transport']
            global default_values1
            default_values1= [[3], ["200,300,100"],[2],['400,180'],[2],[200]]
            rows1, columns1 = matrix_dimensions(default_values1)
            self.table1 = CustomTable(self, rows1, columns1, default_values1, row_headers=row_headers1,widthval=250)
            self.table1.grid(row=1, column=0, padx=20, pady=10)

            column_headers=["usine 1", "usine 2", "usine 3", "Dépot 1", "Dépot 2", "Client 1", "Client 2"]
            row_headers=["usine 1", "usine 2", "usine 3", "Dépot 1", "Dépot 2", "Client 1", "Client 2"]
            global default_values 
            default_values = [
                [float('nan'), 5, 3, 5, 5, 20, 20],
                [9, float('nan'), 9, 1, 1, 8, 15],
                [0.4, 8, float('nan'), 1, 0.5, 10, 12],
                [float('nan'), float('nan'), float('nan'), float('nan'), 1.2, 2, 12],
                [float('nan'), float('nan'), float('nan'), 8, float('nan'), 2, 12],
                [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 1],
                [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 7, float('nan')]
            ]
            rows, columns = matrix_dimensions(default_values)
            self.table = CustomTable(self, rows, columns, default_values, row_headers=row_headers, column_headers=column_headers)
            self.table.grid(row=2, column=0, padx=20, pady=10)
        self.resetbutton = customtkinter.CTkButton(self, text="reset",
                                                    font=("Helvetica", 16, "bold"),
                                                    hover_color=("#8a3838", "gray20"),
                                                    fg_color=("#bf4e4e", "gray20"), command=lambda: reset())
        self.resetbutton.grid(row=2, column=3, padx=20, pady=10,sticky="s")