import random
import math

ALPHA = 1.0
BETA = 2.0
Q = 100.0


def calculate_distance(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return c * 6371


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
                if len(parts) >= 3:
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
    return [[1.0 for _ in range(n)] for _ in range(n)]


def choose_next_city(current_city, visited, n, pheromone_matrix, distance_matrix):
    probabilities = [0.0] * n
    sum_probabilities = 0.0

    for i in range(n):
        if not visited[i] and distance_matrix[current_city][i] > 0:
            pheromone = pheromone_matrix[current_city][i] ** ALPHA
            distance = (1.0 / distance_matrix[current_city][i]) ** BETA
            probabilities[i] = pheromone * distance
            sum_probabilities += probabilities[i]

    if sum_probabilities == 0.0:
        not_visited = [i for i in range(n) if not visited[i]]
        return random.choice(not_visited) if not_visited else -1

    for i in range(n):
        probabilities[i] /= sum_probabilities

    rand = random.random()
    cumulative_prob = 0.0
    for i in range(n):
        if not visited[i]:
            cumulative_prob += probabilities[i]
            if rand <= cumulative_prob:
                return i

    not_visited = [i for i in range(n) if not visited[i]]
    return random.choice(not_visited) if not_visited else -1


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
            delta = Q / length
            pheromone_matrix[current_city][next_city] += delta
            pheromone_matrix[next_city][current_city] += delta
