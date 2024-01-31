
import tkinter
import customtkinter
import pandas as pd

from tableClass import CustomTable
from func import  matrix_dimensions, cast_table_to_float

from PL.pl8 import dijkstra
from PL.pl6Graph import test_data 


class MyFrame8(customtkinter.CTkFrame):
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

###############table 1 ###############
        row_headers=['nb_villes','ville de départ','ville d\'arrivée']
        nb_villes= [[10],[1],[10]]
        rows, columns = matrix_dimensions(nb_villes)
        self.table1 = CustomTable(self, rows, columns, nb_villes, row_headers=row_headers,widthval=150)
        self.table1.grid(row=1, column=0, padx=20, pady=10)

        #get values from the table
        def update_nb_villes(self):
            global nb_villes,nb_v,ville_depart,ville_arrivee
            nb_villes = self.table1.get_table_values()[0][0]
            ville_depart=int(self.table1.get_table_values()[1][0])
            ville_arrivee=int(self.table1.get_table_values()[2][0])
            nb_v=int(nb_villes)
            CustomTable.resize_table(self, nb_v, nb_v,2,0, "ville","ville")

        self.getvals = customtkinter.CTkButton(self, text="resize table",
                                                    font=("Helvetica", 16, "bold"),
                                                    command=lambda: update_nb_villes(self))
        self.getvals.grid(row=2, column=2, padx=20, pady=10,sticky="s")


###############
        # set table 2 and show it in the GUI
        global default_values 
        default_values = [
                    [float('nan'), 70, 63, 56, float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan')],
                    [float('nan'), float('nan'), 25, 19, 73, 50, 79, float('nan'), float('nan'), float('nan')],
                    [float('nan'), 25, float('nan'), 29, 69, 61, float('nan'), float('nan'), float('nan'), float('nan')],
                    [float('nan'), 19, 29, float('nan'), 67, 45, float('nan'), float('nan'), 85, float('nan')],
                    [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 18, 67, 69, 54, 87],
                    [float('nan'), float('nan'), float('nan'), float('nan'), 18, float('nan'), 72, 52, 51, 97],
                    [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 17, 31, 72],
                    [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 17, float('nan'), 15, float('nan')],
                    [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 31, 15, float('nan'), 69],
                    [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan')]
                ]
        row_headers = ["ville 1 ", "ville 2  ", "ville 3  ", "ville 4  ", "ville 5  ", "ville 6  ", "ville 7  ", "ville 8  ", "ville 9  ", "ville 10  "]
        column_headers = ["ville 1 ", "ville 2  ", "ville 3  ", "ville 4  ", "ville 5  ", "ville 6  ", "ville 7  ", "ville 8  ", "ville 9  ", "ville 10  "]
        rows, columns = matrix_dimensions(default_values)
        self.table = CustomTable(self, rows, columns, default_values, row_headers=row_headers, column_headers=column_headers)
        self.table.grid(row=2, column=0, padx=20, pady=10,sticky="w")

        # button to get values from the table
        def get_values(self):
            global table_values,ville_depart,ville_arrivee
            ville_arrivee=int(self.table1.get_table_values()[2][0])
            ville_depart=int(self.table1.get_table_values()[1][0])
            table_values = self.table.get_table_values()
            table_values=cast_table_to_float(table_values)
            print(table_values)
        self.getvals = customtkinter.CTkButton(self, text="set values",
                                                    font=("Helvetica", 16, "bold"),
                                                    command=lambda: get_values(self))
        self.getvals.grid(row=2, column=1, padx=20, pady=10,sticky="s")





######### graphe #########
        def diplay_graph(table_values):
            x1 = self.table1.get_table_values()
            x2=x1[0][0]
            x=int(x2)
            col=[]
            for i in range(1, x+1):
                col.append(f"ville {i}") 
            print(col)

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



################ solver #####################
        def diplay_results(table_values):
            global results_label
            try:
                results_label.destroy()
            except:
                pass
            graph = {i: {} for i in range(1, 11)}
            for i, row in enumerate(table_values, start=1):
                for j, distance in enumerate(row, start=1):
                    if not (distance != distance):  # Check if it's not nan
                        graph[i][j] = distance

            shortest_path_distance = dijkstra(graph, ville_depart, ville_arrivee)
            # Create a string representation of the dictionary
            optimal_solution=(f"The shortest path distance between city 1 and city 10 is:\n {shortest_path_distance}")

            results_text = tkinter.StringVar(value=optimal_solution)
            # Create a new CTkLabel with the string representation as the text
            results_label = customtkinter.CTkLabel(self,textvariable=results_text,
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
                                                   command=lambda : diplay_results(table_values))
        self.solvebutton.grid(row=4, column=1, padx=20, pady=10,sticky="n")





################reset frame#####################
        def reset_frame():
            self.table1.destroy()
            self.table.destroy()
            try :
                results_label.destroy()
            except:
                pass
            row_headers=['nb_villes','ville de départ','ville d\'arrivée']
            nb_villes= [[10],[1],[10]]
            rows, columns = matrix_dimensions(nb_villes)
            self.table1 = CustomTable(self, rows, columns, nb_villes, row_headers=row_headers,widthval=150)
            self.table1.grid(row=1, column=0, padx=20, pady=10)

            # set table 2 and show it in the GUI
            default_values = [
                        [float('nan'), 70, 63, 56, float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan')],
                        [float('nan'), float('nan'), 25, 19, 73, 50, 79, float('nan'), float('nan'), float('nan')],
                        [float('nan'), 25, float('nan'), 29, 69, 61, float('nan'), float('nan'), float('nan'), float('nan')],
                        [float('nan'), 19, 29, float('nan'), 67, 45, float('nan'), float('nan'), 85, float('nan')],
                        [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 18, 67, 69, 54, 87],
                        [float('nan'), float('nan'), float('nan'), float('nan'), 18, float('nan'), 72, 52, 51, 97],
                        [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 17, 31, 72],
                        [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 17, float('nan'), 15, float('nan')],
                        [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 31, 15, float('nan'), 69],
                        [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan')]
                    ]
            row_headers = ["ville 1 ", "ville 2  ", "ville 3  ", "ville 4  ", "ville 5  ", "ville 6  ", "ville 7  ", "ville 8  ", "ville 9  ", "ville 10  "]
            column_headers = ["ville 1 ", "ville 2  ", "ville 3  ", "ville 4  ", "ville 5  ", "ville 6  ", "ville 7  ", "ville 8  ", "ville 9  ", "ville 10  "]
            rows, columns = matrix_dimensions(default_values)
            self.table = CustomTable(self, rows, columns, default_values, row_headers=row_headers, column_headers=column_headers)
            self.table.grid(row=2, column=0, padx=20, pady=10)
        self.resetbutton = customtkinter.CTkButton(self, text="reset",
                                                    font=("Helvetica", 16, "bold"),
                                                    hover_color=("#8a3838", "gray20"),
                                                    fg_color=("#bf4e4e", "gray20"), command=lambda: reset_frame())
        self.resetbutton.grid(row=2, column=3, padx=20, pady=10,sticky="s")
