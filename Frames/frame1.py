import tkinter
import customtkinter
from tableClass import CustomTable
from func import matrix_dimensions
from PL.pl1 import pl1_gestion_optimale_d_une_zone_agricole
from Frames.default_data1 import COLUMN_HEADERS, DEFAULT_VALUES1, DEFAULT_VALUES2

class MyFrame1(customtkinter.CTkFrame):
    COLUMN_HEADERS = COLUMN_HEADERS
    DEFAULT_VALUES1 = DEFAULT_VALUES1
    DEFAULT_VALUES2 = DEFAULT_VALUES2
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.init_labels()
        self.reset_frame()
        self.init_buttons()

    def init_labels(self):
        self.create_label("Veuillez entrer les données", 0)
        self.create_label("Résultats", 3)

    def create_label(self, text, row):
        text_var = tkinter.StringVar(value=text)
        label = customtkinter.CTkLabel(
            self, textvariable=text_var, width=120, height=25, corner_radius=8,
            font=("Helvetica", 32, "bold")
        )
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")

    def reset_frame(self):
        # Destroy existing tables and results label if they exist
        try:
            self.table1.destroy()
        except AttributeError:
            pass

        try:
            self.table2.destroy()
        except AttributeError:
            pass

        try:
            self.results_label.destroy()
        except AttributeError:
            pass

        # Recreate the tables with the default values
        self.create_table1()
        self.create_table2()

    def create_table1(self):
        self.table1 = self.create_table(self.DEFAULT_VALUES1, "w", 1, self.COLUMN_HEADERS, self.get_row_headers1())

    def create_table2(self):
        self.table2 = self.create_table(self.DEFAULT_VALUES2, "w", 2, [], self.get_row_headers2())

    def create_table(self, default_values, sticky, row, column_headers, row_headers):
        rows, columns = matrix_dimensions(default_values)
        table = CustomTable(self, rows, columns, default_values, row_headers=row_headers, column_headers=column_headers)
        table.grid(row=row, column=0, padx=20, pady=10, sticky=sticky)
        return table

    def get_row_headers1(self):
        return ["Rendement Q/ha", "Prix de vente UMJ", "M.O.Ouvriers/ha", "Temps machine Wha", "Eau m³/Iha", "Salaire annuel/ouvrier", "Frais fixe de gestion"]

    def get_row_headers2(self):
        return ["total_area", "total_labor", "total_water", "Bet-total_machine_time"]

    def get_all(self):
        table_values1 = self.get_table_values(self.table1)
        table_values2 = self.get_table_values(self.table2)
        return self.process_values(table_values1, table_values2)

    def get_table_values(self, table):
        table_values = table.get_table_values()
        table_values.append(self.COLUMN_HEADERS)
        return table_values

    def process_values(self, table_values1, table_values2):
        total_area = float(table_values2[0][0])
        total_labor = float(table_values2[1][0])
        total_water = float(table_values2[2][0])
        total_machine_time = float(table_values2[3][0])
        crop_names = table_values1[7]
        crop_data = {
            crop_name: {
                "yield": int(table_values1[0][i]),
                "price": int(table_values1[1][i]),
                "labor": int(table_values1[2][i]),
                "machine_time": int(table_values1[3][i]),
                "water": int(table_values1[4][i]),
                "salary": int(table_values1[5][i]),
                "fixed_cost": int(table_values1[6][i]),
            }
            for i, crop_name in enumerate(crop_names)
        }
        return total_area, crop_data, total_labor, total_water, total_machine_time

    def diplay_results(self):
        total_area, crop_data, total_labor, total_water, total_machine_time = self.get_all()
        areas, revenue = pl1_gestion_optimale_d_une_zone_agricole(total_area, crop_data, total_labor, total_water, total_machine_time)
        self.display_output(areas, revenue)

    def display_output(self, areas, revenue):
        output_string = "Optimal solution:\n"
        for crop, area in areas.items():
            output_string += f"Area for {crop}: {area} hectares\n"
        output_string += f"Total revenue: {revenue} UM\n"
        results_text = tkinter.StringVar(value=output_string)
        self.results_label = self.create_output_label(results_text)
        self.results_label.grid(row=4, column=0, padx=20, pady=10)

    def create_output_label(self, results_text):
        return customtkinter.CTkLabel(
            self, textvariable=results_text, fg_color=("white", "gray20"), corner_radius=8,
            font=("Helvetica", 16, "bold"), justify="left", anchor="nw"
        )

    def init_buttons(self):
        self.init_get_values_button()
        self.init_solve_button()
        self.init_reset_button()

    def init_get_values_button(self):
        get_values_button = self.create_button("set data", self.get_all)
        get_values_button.grid(row=2, column=1, padx=20, pady=10, sticky="s")

    def init_solve_button(self):
        solve_button = self.create_button("solve", self.diplay_results)
        solve_button.grid(row=4, column=1, padx=20, pady=10, sticky="n")

    def init_reset_button(self):
        reset_button = self.create_button("reset", self.reset_frame)
        reset_button.grid(row=2, column=2, padx=20, pady=10, sticky="sw")

    def create_button(self, text, command):
        return customtkinter.CTkButton(
            self, text=text, font=("Helvetica", 16, "bold"), command=command
        )
