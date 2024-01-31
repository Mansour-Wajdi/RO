import tkinter
import customtkinter
from func import  matrix_dimensions, cast_table_to_int, cast_table_to_float


class CustomTable(tkinter.Frame):
    def __init__(self, parent, rows, columns,
                  default_values=None, row_headers=None,
                    column_headers=None,widthval=50,hightval=28):
        tkinter.Frame.__init__(self, parent)
        self.entries = []

        if column_headers:
            for j, header in enumerate(column_headers):
                label = customtkinter.CTkLabel(self, text=header, padx=2, pady=2,
                                               font=("Helvetica", 16))
                label.grid(row=0, column=j+1)

        if row_headers:
            for i, header in enumerate(row_headers):
                label = customtkinter.CTkLabel(self, text=header, padx=2, pady=2,
                                               font=("Helvetica", 16))
                label.grid(row=i+1, column=0, sticky="w")

        for i in range(rows):
            current_row = []
            for j in range(columns):
                entry = customtkinter.CTkEntry(self,width=widthval,height=hightval ,
                                               font=("Helvetica", 16))
                if default_values and default_values[i][j]:
                    entry.insert(0, default_values[i][j])
                entry.grid(row=i+1, column=j+1)  # Update the row and column indices to account for headers
                current_row.append(entry)
            self.entries.append(current_row)

    def get_table_values(self):
        values = []
        for row_entries in self.entries:
            row_values = [entry.get() for entry in row_entries]
            values.append(row_values)
        return values
    def destroy_table(table):
        table.destroy()

    def resize_table(self,x,y,rgrid,cgrid,string1,string2,widthval=50,table="table"):
        CustomTable.destroy_table(self.table)
        column_headers = [string1 + " " + str(i) for i in range(1, y+1)]
        row_headers = [string2 + " " + str(i) for i in range(1, x+1)]
        default=[[float('nan') for i in range(y)] for j in range(x)]
        print(default)
        rows, columns = matrix_dimensions(default)
        self.table = CustomTable(self, rows, columns, default, row_headers=row_headers, column_headers=column_headers,widthval=widthval)
        self.table.grid(row=rgrid, column=cgrid, padx=20, pady=10,sticky="w")

    def resize_table2(self,x,y,rgrid,cgrid,string1,string2,widthval=50,table="table"):
        CustomTable.destroy_table(self.table2)
        column_headers = [string1 + " " + str(i) for i in range(1, y+1)]
        row_headers = [string2 + " " + str(i) for i in range(1, x+1)]
        default=[[float('nan') for i in range(y)] for j in range(x)]
        print(default)
        rows, columns = matrix_dimensions(default)
        self.table2 = CustomTable(self, rows, columns, default, row_headers=row_headers, column_headers=column_headers,widthval=widthval)
        self.table2.grid(row=rgrid, column=cgrid, padx=20, pady=10,sticky="w")

    def resize_table3(self,x,y,rgrid,cgrid,string1,string2,widthval=50,table="table"):
        CustomTable.destroy_table(self.table3)
        column_headers = [string1 + " " + str(i) for i in range(1, y+1)]
        row_headers = [string2 + " " + str(i) for i in range(1, x+1)]
        default=[[float('nan') for i in range(y)] for j in range(x)]
        print(default)
        rows, columns = matrix_dimensions(default)
        self.table3 = CustomTable(self, rows, columns, default, row_headers=row_headers, column_headers=column_headers,widthval=widthval)
        self.table3.grid(row=rgrid, column=cgrid, padx=20, pady=10,sticky="w")


    def resize_table6(self,x1,y1,x2,y2,x3,y3,rgrid,cgrid,string11,string12,string21,string22,string31,string32,widthval=50):
        CustomTable.destroy_table(self.table)
        column_headers = [string11 + " " + str(i) for i in range(1, y1+1)]
        row_headers = [string12 + " " + str(i) for i in range(1, x1+1)]

        column_headers=column_headers+[string21 + " " + str(i) for i in range(1, y2+1)]
        row_headers=row_headers+[string22 + " " + str(i) for i in range(1, x2+1)]

        column_headers=column_headers+[string31 + " " + str(i) for i in range(1, y3+1)]
        row_headers=row_headers+[string32 + " " + str(i) for i in range(1, x3+1)]

        default=[[float('nan') for i in range(y1+y2+y3)] for j in range(x1+x2+x3)]
        print(default)
        rows, columns = matrix_dimensions(default)
        self.table = CustomTable(self, rows, columns, default, row_headers=row_headers, column_headers=column_headers,widthval=widthval)
        self.table.grid(row=rgrid, column=cgrid, padx=20, pady=10,sticky="w")