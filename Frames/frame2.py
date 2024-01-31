import tkinter
import customtkinter
from tableClass import CustomTable
from func import  matrix_dimensions
from PL.pl2 import optimize_petroleum_mix

class MyFrame2(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.result_label = None
        self.default_values = [[5000],[10000],[10],[5],[8],[6],[25],[20],[0.2],[0.1]]
        self.row_headers = ["Le nombre de barils de pétrole brut de type 1", 
                            "Le nombre de barils de pétrole brut de type 2", 
                            "Le niveau de qualité d'un baril de type 1", 
                            "Le niveau de qualité d'un baril de type 2", 
                            "Le niveau minimum de qualité de la gazoline", 
                            "Le niveau minimum de qualité du pétrole de chauffage", 
                            "Le prix de vente d'un baril de gazoline", 
                            "Le prix de vente d'un baril de pétrole de chauffage", 
                            "Les frais de marketing d'un baril de gazoline en dinars", 
                            "Les frais de marketing d'un baril de pétrole de chauffage en dinars"]

        self.create_labels()
        self.create_table()
        self.create_buttons()

    def create_labels(self):
        La = tkinter.StringVar(value="Veuillez entrer les données")
        L1 = customtkinter.CTkLabel(self,textvariable=La,width=120,height=25,corner_radius=8,
                                    font=("Helvetica", 32, "bold"))
        L1.grid(row=0, column=0, padx=20, pady=10,sticky="w")
        Lb = tkinter.StringVar(value="Résultats")
        L2 = customtkinter.CTkLabel(self,textvariable=Lb,width=120,height=25,corner_radius=8,
                                    font=("Helvetica", 32, "bold"))
        L2.grid(row=2, column=0, padx=20, pady=10)

    def create_table(self):
        rows, columns = matrix_dimensions(self.default_values)
        self.table = CustomTable(self, rows, columns, self.default_values, row_headers=self.row_headers)
        self.table.grid(row=1, column=0, padx=20, pady=10, sticky= "w")

    def create_buttons(self):
        self.getvals = customtkinter.CTkButton(self, text="set values",
                                                   font=("Helvetica", 16, "bold"),
                                                    command=self.get_values)
        self.getvals.grid(row=1, column=1, padx=20, pady=10, sticky="s")

        self.solvebutton = customtkinter.CTkButton(self,  text="solve",
                                                   font=("Helvetica", 16, "bold"),
                                                   fg_color=("#48ab79", "gray20"),
                                                   hover_color=("#327855","gray20"),
                                                   command=self.diplay_results)
        self.solvebutton.grid(row=3, column=1, padx=20, pady=10,sticky="n")

        self.reset_button = customtkinter.CTkButton(self, text="reset",
                                                    font=("Helvetica", 16, "bold"),
                                                    hover_color=("#8a3838", "gray20"),
                                                    fg_color=("#bf4e4e", "gray20"),
                                                    command=self.reset_frame)
        self.reset_button.grid(row=1, column=2, padx=20, pady=10,sticky="s")

    def get_values(self):
        table_values = self.table.get_table_values()
        self.vars =[float(table_values[i][0]) for i in range(10)]

    def diplay_results(self):
        try:
            self.result_label.destroy() 
        except:
            pass
        results = optimize_petroleum_mix(*self.vars)
        dict_str = "\n".join([f"{key}: {value}" for key, value in results.items()])
        results_text = tkinter.StringVar(value=dict_str)
        self.result_label = customtkinter.CTkLabel(self, textvariable=results_text,
                                                   fg_color=("white", "gray20"),
                                                   corner_radius=8,
                                                   font=("Helvetica", 16, "bold"),
                                                   justify="left",
                                                   anchor="nw"
                                                   )
        self.result_label.grid(row=3, column=0, padx=20, pady=10)

    def reset_frame(self):
        self.table.destroy()
        try:
            self.result_label.destroy() 
        except:
            pass
        self.create_table()
