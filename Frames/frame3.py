import tkinter
import customtkinter
from tableClass import CustomTable
from func import  matrix_dimensions
from PL.pl3 import pl3_planification 

class MyFrame3(customtkinter.CTkFrame):
    DEFAULT_VALUES = [[7], ["17,13,15,19,14,16,11"], [5], [2]]
    ROW_HEADERS = ['days', 'min_required', 'work_days', 'rest_days']

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.init_labels()
        self.init_table()
        self.init_buttons()

    def init_labels(self):
        self.create_label("Veuillez entrer les données", 0)
        self.create_label("Résultats", 2)

    def create_label(self, text, row):
        label_text = tkinter.StringVar(value=text)
        label = customtkinter.CTkLabel(self, textvariable=label_text, width=120, height=25, corner_radius=8, font=("Helvetica", 32, "bold"))
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")

    def init_table(self):
        rows, columns = matrix_dimensions(self.DEFAULT_VALUES)
        self.table = CustomTable(self, rows, columns, self.DEFAULT_VALUES, row_headers=self.ROW_HEADERS, widthval=150)
        self.table.grid(row=1, column=0, padx=20, pady=10, sticky="w")

    def init_buttons(self):
        self.init_get_values_button()
        self.init_solve_button()
        self.init_reset_button()

    def init_get_values_button(self):
        get_values_button = customtkinter.CTkButton(self, text="set values", font=("Helvetica", 16, "bold"), command=self.get_values)
        get_values_button.grid(row=1, column=1, padx=20, pady=10, sticky="s")

    def init_solve_button(self):
        solve_button = customtkinter.CTkButton(self, text="solve", font=("Helvetica", 16, "bold"), fg_color=("#48ab79", "gray20"), hover_color=("#327855","gray20"), command=self.display_results)
        solve_button.grid(row=3, column=1, padx=20, pady=10, sticky="n")

    def init_reset_button(self):
        reset_button = customtkinter.CTkButton(self, text="reset", font=("Helvetica", 16, "bold"), hover_color=("#8a3838", "gray20"), fg_color=("#bf4e4e", "gray20"), command=self.reset_frame)
        reset_button.grid(row=1, column=2, padx=20, pady=10, sticky="s")

    def get_values(self):
        table_values = self.table.get_table_values()
        vars = [table_value[0] for table_value in table_values]
        vars[0] = int(vars[0])
        vars[1] = [int(x) for x in vars[1].split(",")]
        vars[2] = int(vars[2])
        vars[3] = int(vars[3])
        self.days, self.min_required, self.work_days, self.rest_days = vars

    @staticmethod
    def process_table_values(table_values):
        vars = [table_value[0] for table_value in table_values]
        vars[1] = [int(x) for x in vars[1].split(",")]
        return [int(var) for var in vars]

    def display_results(self):
        if hasattr(self, 'days'):  # Checking if 'days' attribute exists
            try:
                self.results_label.destroy()
            except AttributeError:
                pass

            results = pl3_planification(self.days, self.min_required, self.work_days, self.rest_days)
            results_text = tkinter.StringVar(value=results)
            self.results_label = customtkinter.CTkLabel(self, textvariable=results_text, fg_color=("white", "gray20"), corner_radius=8, font=("Helvetica", 16, "bold"), justify="left", anchor="nw")
            self.results_label.grid(row=20, column=0, padx=20, pady=10)
        else:
            print("Please set the values before attempting to display results.")

    def reset_frame(self):
        self.table.destroy()
        try:
            self.results_label.destroy()
        except AttributeError:
            pass
        self.init_table()
