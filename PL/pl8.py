import heapq

def dijkstra(graph, start, end):
    queue = [(0, start)]
    visited = set()
    while queue:
        (cost, current) = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        if current == end:
            return cost
        for neighbor, edge_cost in graph[current].items():
            if neighbor not in visited:
                heapq.heappush(queue, (cost + edge_cost, neighbor))
    return -1

"""
table = [
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

graph = {i: {} for i in range(1, 11)}

for i, row in enumerate(table, start=1):
    for j, distance in enumerate(row, start=1):
        if not (distance != distance):  # Check if it's not nan
            graph[i][j] = distance

shortest_path_distance = dijkstra(graph, 1, 10)
print(f"The shortest path distance between city 1 and city 10 is: {shortest_path_distance}")
"""
