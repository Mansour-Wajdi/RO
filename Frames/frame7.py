
import tkinter
import customtkinter
import pandas as pd

from tableClass import CustomTable

from func import  matrix_dimensions, cast_table_to_int
from PL.pl7 import optimize_assignment


class MyFrame7(customtkinter.CTkFrame):
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

        #set the table 1 in the GUI
        row_headers1= ["nb_Entreprise", "nb_projet"]
        global default_values1 
        default_values1 = [[6],[8]]
        rows, columns = matrix_dimensions(default_values1)
        self.table1 = CustomTable(self, rows, columns, default_values1, row_headers=row_headers1)
        self.table1.grid(row=1, column=0, padx=20, pady=10)
        
        #get values from the table
        def get_values1(self):
            global table_values1
            table_values1 = self.table1.get_table_values()
            table_values1=cast_table_to_int(table_values1)
            #print(table_values1)
        #self.getvals = customtkinter.CTkButton(self, text="update", command=lambda: get_values1(self))
        #self.getvals.grid(row=2, column=1, padx=20, pady=10)

        #set the table 2 in the GUI
        row_headers= ["Entreprise 1", "Entreprise 2", "Entreprise 3", "Entreprise 4", "Entreprise 5", "Entreprise 6"]
        column_headers  = ["projet 1  ", "projet 2  ", "projet 3  ", "projet 4  ", "projet 5  ", "projet 6  ", "projet 7  ", "projet 8  "]
        global default_values 
        default_values = [
                [float('nan'), 8200, 7800, 5400, float('nan'), 3900, float('nan'), float('nan')],
                [7800, 8200, float('nan'), 6300, float('nan'), 3300, 4900, float('nan')],
                [float('nan'), 4800, float('nan'), float('nan'), float('nan'), 4400, 5600, 3600],
                [float('nan'), float('nan'), 8000, 5000, 6800, float('nan'), 6700, 4200],
                [7200, 6400, float('nan'), 3900, 6400, 2800, float('nan'), 3000],
                [7000, 5800, 7500, 4500, 5600, float('nan'), 6000, 4200]
            ]
        rows, columns = matrix_dimensions(default_values)
        self.table = CustomTable(self, rows, columns, default_values, row_headers=row_headers, column_headers=column_headers)
        self.table.grid(row=2, column=0, padx=20, pady=10,sticky="w")
        
        #get values from the table
        def get_values(self):
            global table_values
            table_values = self.table.get_table_values()
            #print(table_values)
        def get_all_values (self):
            get_values1(self)
            get_values(self)
        
        def resize(self):
            get_values1(self)
            CustomTable.resize_table(self, table_values1[0][0],table_values1[1][0],2,0,"projet","entreprise")
        self.getvals = customtkinter.CTkButton(self,text="set values",
                                                    font=("Helvetica", 16, "bold"),
                                                    command=lambda: get_all_values(self))
        self.getvals.grid(row=2, column=1, padx=20, pady=10,sticky="s")
        self.getvals = customtkinter.CTkButton(self, text="resize table",
                                                    font=("Helvetica", 16, "bold"),
                                                     command=lambda: resize(self))
        self.getvals.grid(row=2, column=2, padx=20, pady=10,sticky="s")


################ solver #####################
        def diplay_results(table_values):
            global results_label
            try:
                results_label.destroy()
            except:
                pass
            
            for i in range(len(table_values)):
               for j in range(len(table_values[i])):
                    table_values[i][j] = float(table_values[i][j])
            assignment, obj_val = optimize_assignment(table_values)
            # Create a string representation of the dictionary
            if assignment:
                optimal_solution = (
                    "Optimal solution found:\n"
                    + "\n".join(
                        [f"Assign project {j} to company {i}" for i, j in assignment]
                    )
                    + f"\nObjective value: {obj_val}"
                )
            else:
                optimal_solution = "No optimal solution found."

            results_text = tkinter.StringVar(value=optimal_solution)
            results_label = customtkinter.CTkLabel(self,textvariable=results_text,
                                                   fg_color=("white", "gray20"),
                                                   corner_radius=8,
                                                   font=("Helvetica", 16, "bold"),
                                                   justify="left",
                                                   anchor="nw"
                                                   )
            results_label.grid(row=4, column=0, padx=20, pady=10)
        self.solvebutton = customtkinter.CTkButton(self,  text="solve",
                                                   font=("Helvetica", 16, "bold"),
                                                   fg_color=("#48ab79", "gray20"),
                                                   hover_color=("#327855","gray20"),
                                                   command=lambda: diplay_results(table_values))
        self.solvebutton.grid(row=4, column=1, padx=20, pady=10,sticky="n")
        
        #self.resizeButton = customtkinter.CTkButton(self, text="resize",command=lambda: CustomTable.resize_table(self, table_values1[0][0],table_values1[1][0],3,0,"projet","entreprise"))
        #self.resizeButton.grid(row=17, column=1, padx=20, pady=10)



################reset frame#####################
        def reset_frame():
            self.table.destroy()
            self.table1.destroy()
            try :
                results_label.destroy()
            except:
                pass
            row_headers1= ["nb_Entreprise", "nb_projet"]
            global default_values1 
            default_values1 = [[6],[8]]
            rows, columns = matrix_dimensions(default_values1)
            self.table1 = CustomTable(self, rows, columns, default_values1, row_headers=row_headers1)
            self.table1.grid(row=1, column=0, padx=20, pady=10)
            #set the table 2 in the GUI
            row_headers= ["Entreprise 1", "Entreprise 2", "Entreprise 3", "Entreprise 4", "Entreprise 5", "Entreprise 6"]
            column_headers  = ["projet 1  ", "projet 2  ", "projet 3  ", "projet 4  ", "projet 5  ", "projet 6  ", "projet 7  ", "projet 8  "]
            global default_values 
            default_values = [
                    [float('nan'), 8200, 7800, 5400, float('nan'), 3900, float('nan'), float('nan')],
                    [7800, 8200, float('nan'), 6300, float('nan'), 3300, 4900, float('nan')],
                    [float('nan'), 4800, float('nan'), float('nan'), float('nan'), 4400, 5600, 3600],
                    [float('nan'), float('nan'), 8000, 5000, 6800, float('nan'), 6700, 4200],
                    [7200, 6400, float('nan'), 3900, 6400, 2800, float('nan'), 3000],
                    [7000, 5800, 7500, 4500, 5600, float('nan'), 6000, 4200]
                ]
            rows, columns = matrix_dimensions(default_values)
            self.table = CustomTable(self, rows, columns, default_values, row_headers=row_headers, column_headers=column_headers)
            self.table.grid(row=2, column=0, padx=20, pady=10)
        self.resetbutton = customtkinter.CTkButton(self, text="reset",
                                                    font=("Helvetica", 16, "bold"),
                                                    hover_color=("#8a3838", "gray20"),
                                                    fg_color=("#bf4e4e", "gray20"), command=lambda: reset_frame())
        self.resetbutton.grid(row=2, column=3, padx=20, pady=10,sticky="s")
