import tkinter
import customtkinter
from tableClass import CustomTable

from func import  matrix_dimensions,cast_table_to_int
from PL.pl5 import optimal_electricity_supply 




class MyFrame5(customtkinter.CTkFrame):
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

################ table 1 #####################
        row_headers=['nb_centrales', 'offres','nb_villes', 'demandes','penalites']
        global default_values
        default_values= [[3], ["35,50,40"], [4], ["45,20,30,30"], ["20, 25, 22, 35"]]
        rows, columns = matrix_dimensions(default_values)
        self.table = CustomTable(self, rows, columns, default_values, row_headers=row_headers,widthval=150)
        self.table.grid(row=1, column=0, padx=20, pady=10,sticky="w")

    ################ getter 1 #####################
        def get_values(self):
            global table_values
            table_values = self.table.get_table_values()
            global nb_centrales, offres_list, nb_villes, demandes_list , penalites_list
            vars =[]
            for i in range(len(table_values)):
                vars.append(table_values[i][0])
            for i in range(len(vars)):
                if i != 1 and i != 3 and i != 4:
                    vars[i]= int(vars[i])
                else:
                    vars[i]=[int(x) for x in vars[i].split(",")]
            nb_centrales=vars[0]
            offres_list=vars[1]
            nb_villes=vars[2]
            demandes_list=vars[3]
            penalites_list=vars[4]
        #self.getvals = customtkinter.CTkButton(self, text="set vals ", command=lambda: get_values(self))
        #self.getvals.grid(row=1, column=1, padx=20, pady=10)
    

################ table 2 #####################
        row_headers1= ["Centrale 1", "Centrale 2", "Centrale 3"]
        column_headers1  = ["Ville  1  ", "Ville 2  ", "Ville 3  ", "Ville 4  "]
        global default_values1 
        default_values1 = [[8,6,10,9],[9,12,13,7],[14,9,16,5],]
        rows1, columns1 = matrix_dimensions(default_values1)
        self.table1 = CustomTable(self, rows1, columns1, default_values1, row_headers=row_headers1, column_headers=column_headers1)
        self.table1.grid(row=2, column=0, padx=20, pady=10,sticky="w")
        
    ################ getter 2 #####################
        def get_values1(self):
            global table_values1
            table_values1 = self.table1.get_table_values()
            print(table_values1)
            table_values1=cast_table_to_int(table_values1)
        def get_all(self): 
            get_values(self)
            get_values1(self)
        self.getvals1 = customtkinter.CTkButton(self, text="set values",
                                                    font=("Helvetica", 16, "bold"),
                                                    command=lambda: get_all(self))
        self.getvals1.grid(row=2, column=1, padx=20, pady=10,sticky="s")

    ################ resize #####################
        def get_values1(self):
            global table_values1
            table_values1 = self.table1.get_table_values()
            print(table_values1)
            table_values1=cast_table_to_int(table_values1)
        def get_all(self): 
            get_values(self)
            get_values1(self)
        self.getvals1 = customtkinter.CTkButton(self, text="resize table",
                                                    font=("Helvetica", 16, "bold"),
                                                    command=lambda: get_all(self))
        self.getvals1.grid(row=2, column=2, padx=20, pady=10,sticky="s")


################ solver #####################
        def diplay_results():
            global results_label
            try:
                results_label.destroy()
            except:
                pass
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
                    couts_transport[(c, v)] = table_values1[i][j]
            total_cost, unsatisfied_demand,resultat = optimal_electricity_supply(centrales, villes, offres, demandes, couts_transport, penalites)



            output_string = f"Cout total : {total_cost:.2f} millions d'euros\n"
            for v in villes:
                if unsatisfied_demand[v] > 0:
                    output_string += "Demande insatisfaite :\n"
                    break
            for v in villes:
                if unsatisfied_demand[v] > 0:
                    output_string += f"Il manque {unsatisfied_demand[v]:.2f} millions de Kwh a la ville {v}\n"
            print(output_string)


            results_label = customtkinter.CTkLabel(self, text=resultat+output_string,
                                                   fg_color=("white", "gray20"),
                                                   corner_radius=8,
                                                   font=("Helvetica", 16, "bold"),
                                                   justify="left",
                                                   anchor="nw"
                                                   )
            results_label.grid(row=20, column=0, padx=20, pady=10)
        self.solvebutton = customtkinter.CTkButton(self,  text="solve",
                                                   font=("Helvetica", 16, "bold"),
                                                   fg_color=("#48ab79", "gray20"),
                                                   hover_color=("#327855","gray20"),
                                                   command=diplay_results)
        self.solvebutton.grid(row=4, column=1, padx=20, pady=10,sticky="n")



################ reset frame #####################
        def reset_frame():
            self.table.destroy()
            self.table1.destroy()
            try:
                results_label.destroy()
            except:
                pass    

            self.table = CustomTable(self, rows, columns, default_values, row_headers=row_headers,widthval=150)
            self.table.grid(row=1, column=0, padx=20, pady=10,sticky="w")
            self.table1 = CustomTable(self, rows1, columns1, default_values1, row_headers=row_headers1, column_headers=column_headers1)
            self.table1.grid(row=2, column=0, padx=20, pady=10,sticky="w")
        self.resetbutton = customtkinter.CTkButton(self, text="reset",
                                                    font=("Helvetica", 16, "bold"),
                                                    hover_color=("#8a3838", "gray20"),
                                                    fg_color=("#bf4e4e", "gray20"), command=reset_frame)
        self.resetbutton.grid(row=2, column=3, padx=20, pady=10,sticky="s")