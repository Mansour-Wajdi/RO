
def matrix_dimensions(matrix):
    if not matrix or not isinstance(matrix, list):
        raise ValueError("Invalid input: Expected a non-empty 2D matrix (list of lists).")
    rows = len(matrix)
    columns = len(matrix[0])
    return rows, columns

def cast_table_to_int(table):
    #cast table_values2 to int
    for i in range(len(table)):
        for j in range(len(table[i])):
            table[i][j] = int(table[i][j])
    print(table)
    return(table)

def cast_table_to_float(table):
    #cast table_values2 to int
    for i in range(len(table)):
        for j in range(len(table[i])):
            table[i][j] = float(table[i][j])
    print(table)
    return(table)