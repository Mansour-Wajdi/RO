import tkinter
import customtkinter
from tableClass import CustomTable
from func import matrix_dimensions
from PL.pl44 import pl4_gestion_de_la_production

class MyFrame4(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs) 

        self.create_labels()
        self.create_table()
        self.create_buttons()

    def create_labels(self):
        La = tkinter.StringVar(value="Veuillez entrer les données")
        L1 = customtkinter.CTkLabel(self, textvariable=La, width=120, height=25, corner_radius=8, font=("Helvetica", 32, "bold"))
        L1.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        Lb = tkinter.StringVar(value="Résultats")
        L2 = customtkinter.CTkLabel(self, textvariable=Lb, width=120, height=25, corner_radius=8, font=("Helvetica", 32, "bold"))
        L2.grid(row=2, column=0, padx=20, pady=10)

    def create_table(self):
        row_headers=['months', 'demands', 'initial_stock', 'initial_workers', 'worker_monthly_wage', 'regular_hours_per_worker', 'max_overtime_hours', 'overtime_hourly_wage', 'production_time_per_pair', 'raw_material_cost', 'recruitment_cost', 'layoff_cost', 'raw_material_cost', 'stock_cost_per_pair']
        default_values= [[4], ["3000,5000,2000,1000"], [500], [100], [1500], [160], [20], [13], [4], [15], [1600], [2000], [15], [3]]
        rows, columns = matrix_dimensions(default_values)
        self.table = CustomTable(self, rows, columns, default_values, row_headers=row_headers, widthval=200)
        self.table.grid(row=1, column=0, padx=20, pady=10, sticky="w")

    def create_buttons(self):
        self.getvals = customtkinter.CTkButton(self, text="set values", font=("Helvetica", 16, "bold"), command=self.get_values)
        self.getvals.grid(row=1, column=1, padx=20, pady=10, sticky="s")

        self.solvebutton = customtkinter.CTkButton(self, text="solve", font=("Helvetica", 16, "bold"), fg_color=("#48ab79", "gray20"), hover_color=("#327855","gray20"), command=self.diplay_results)
        self.solvebutton.grid(row=3, column=1, padx=20, pady=10, sticky="n")

        self.resetbutton = customtkinter.CTkButton(self, text="reset", font=("Helvetica", 16, "bold"), hover_color=("#8a3838", "gray20"), fg_color=("#bf4e4e", "gray20"), command=self.reset_frame)
        self.resetbutton.grid(row=1, column=2, padx=20, pady=10, sticky="s")

    def get_values(self):
        table_values = self.table.get_table_values()
        vars = [int(table_values[i][0]) if i != 1 else [int(x) for x in table_values[i][0].split(",")] for i in range(len(table_values))]

        self.months, self.demand, self.initial_stock, self.initial_workers, self.worker_monthly_wage, self.regular_hours_per_worker, self.max_overtime_hours, self.overtime_hourly_wage, self.production_time_per_pair, self.raw_material_cost, self.recruitment_cost, self.layoff_cost, self.raw_material_cost, self.stock_cost_per_pair = vars

    def diplay_results(self):
        try:
            self.resultTable.destroy()
        except:
            pass

        try:
            self.results_label1.destroy()
        except:
            pass

        tab, total_cost = pl4_gestion_de_la_production(self.months, self.demand,
                                        self.initial_stock, self.initial_workers,
                                          self.worker_monthly_wage, self.regular_hours_per_worker,
                                            self.max_overtime_hours, self.overtime_hourly_wage,
                                              self.production_time_per_pair, self.raw_material_cost,
                                                self.recruitment_cost, self.layoff_cost,
                                                  self.stock_cost_per_pair)
        
        rows=['production', 'stock', 'workers', 'overtime', 'recruitment', 'layoff']
        month_list=["month " + str(i) for i in range(1, self.months+1)]
        self.resultTable = CustomTable(self, 6, self.months, tab, row_headers=rows, column_headers=month_list, widthval=100)
        self.resultTable.grid(row=10, column=0, padx=20, pady=10, sticky="w")

        self.results_label1 = customtkinter.CTkLabel(self, text=total_cost,
                                                   fg_color=("white", "gray20"),
                                                   corner_radius=8,
                                                   font=("Helvetica", 16, "bold"),
                                                   justify="left",
                                                   anchor="nw"
                                                   )
        self.results_label1.grid(row=3, column=0, padx=20, pady=10)

    def reset_frame(self):
        self.table.destroy()
        try:
            self.results_label1.destroy()
        except:
            pass    

        try:
            self.resultTable.destroy()
        except:
            pass    

        row_headers, default_values = self.get_row_headers_and_default_values()
        rows, columns = matrix_dimensions(default_values)
        self.table = CustomTable(self, rows, columns, default_values, row_headers=row_headers, widthval=200)
        self.table.grid(row=1, column=0, padx=20, pady=10, sticky="w")

    def get_row_headers_and_default_values(self):
        row_headers=['months', 'demands', 'initial_stock', 'initial_workers', 'worker_monthly_wage', 'regular_hours_per_worker', 'max_overtime_hours', 'overtime_hourly_wage', 'production_time_per_pair', 'raw_material_cost', 'recruitment_cost', 'layoff_cost', 'raw_material_cost', 'stock_cost_per_pair']
        default_values= [[4], ["3000,5000,2000,1000"], [500], [100], [1500], [160], [20], [13], [4], [15], [1600], [2000], [15], [3]]
        return row_headers, default_values
