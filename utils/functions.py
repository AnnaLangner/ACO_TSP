import math
import random
import matplotlib.pyplot as plt

ALPHA = 1.0   # Influence of pheromone
BETA = 2.0    # Influence of distance
Q = 100.0     # Constant for pheromone deposition


def calculate_distance(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return c


def read_tsp_file(filename):
    coordinates = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        reading_nodes = False
        for line in lines:
            if "NODE_COORD_SECTION" in line:
                reading_nodes = True
                continue
            if "EOF" in line:
                break
            if reading_nodes:
                parts = line.split()
                lat = float(parts[1])
                lon = float(parts[2])
                coordinates.append((lat, lon))
    return coordinates


def build_distance_matrix(coords):
    n = len(coords)
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            lat1, lon1 = coords[i]
            lat2, lon2 = coords[j]
            dist = calculate_distance(lat1, lon1, lat2, lon2)
            matrix[i][j] = matrix[j][i] = dist
    return matrix


def initialize_pheromones(n):
    pheromone_matrix = [[1.0 for _ in range(n)] for _ in range(n)]
    return pheromone_matrix


def choose_next_city(current_city, visited, n, pheromone_matrix, distance_matrix):
    probabilities = [0.0] * n
    sum_probabilities = 0.0

    for i in range(n):
        if not visited[i]:
            pheromone = pheromone_matrix[current_city][i] ** ALPHA
            distance = (1.0 / distance_matrix[current_city][i]) ** BETA
            probabilities[i] = pheromone * distance
            sum_probabilities += probabilities[i]

    for i in range(n):
        probabilities[i] /= sum_probabilities

    rand = random.random()
    cumulative_prob = 0.0
    for i in range(n):
        if not visited[i]:
            cumulative_prob += probabilities[i]
            if rand <= cumulative_prob:
                return i
    return -1


def update_pheromones(ants, lengths, pheromone_matrix, distance_matrix, n, rho, num_ants):
    for i in range(n):
        for j in range(n):
            pheromone_matrix[i][j] *= (1 - rho)

    for k in range(num_ants):
        ant = ants[k]
        length = lengths[k]
        for i in range(len(ant) - 1):
            current_city = ant[i]
            next_city = ant[i + 1]
            pheromone_matrix[current_city][next_city] += Q / length
            pheromone_matrix[next_city][current_city] += Q / length


# for version in CLI
def plot_tour(coords, tour, title="Best Tour"):
    x = [coords[city][0] for city in tour] + [coords[tour[0]][0]]
    y = [coords[city][1] for city in tour] + [coords[tour[0]][1]]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'o-', color='blue', label='Path')
    for i, city in enumerate(tour):
        plt.text(coords[city][0], coords[city][1], str(city), fontsize=9, color='red')
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
