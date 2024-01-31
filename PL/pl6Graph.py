import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow
import pandas as pd
import numpy as np

import gurobipy as gp
from gurobipy import GRB


def create_logistic_graph(transport_costs_matrix):
    G = nx.DiGraph()

    for origin, row in transport_costs_matrix.iterrows():
        for dest, cost in row.iteritems():
            if not pd.isna(cost):
                G.add_edge(origin, dest, weight=cost)

    return G


def plot_logistic_graph(G):
    fig = plt.Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    pos = nx.circular_layout(G)
    edge_labels = {(i, j): f'{G.edges[i, j]["weight"]}' for i, j in G.edges}

    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=12, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, ax=ax)

    canvas.draw()

    return canvas

def test_data(transport_costs_matrix): 
    
    G = create_logistic_graph(transport_costs_matrix)
    canvas = plot_logistic_graph(G)
    
    # Show the canvas in a new window
    app = QApplication([])
    window = QMainWindow()
    window.setCentralWidget(canvas)
    window.show()
    app.exec_()
    

"""
nb_usines=3
nb_depot=2
nb_clients=2
col = ["usine" + " " + str(i) for i in range(1, nb_usines+1)]+["Dépot" + " " + str(i) for i in range(1, nb_depot+1)]+["Client" + " " + str(i) for i in range(1, nb_clients+1)]
    
table_values=[[float('nan'), 5, 3, 5, 5, 20, 20],
            [9, float('nan'), 9, 1, 1, 8, 15],
            [0.4, 8, float('nan'), 1, 0.5, 10, 12],
            [float('nan'), float('nan'), float('nan'), float('nan'), 1.2, 2, 12],
            [float('nan'), float('nan'), float('nan'), 8, float('nan'), 2, 12],
            [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 1],
            [float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 7, float('nan')]]


    
transport_costs_matrix = pd.DataFrame(
            table_values,
            columns=col,
            index=col,
            )


print(transport_costs_matrix)

test_data(transport_costs_matrix)
"""