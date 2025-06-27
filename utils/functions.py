import random
import math

ALPHA = 1.0
BETA = 2.0
Q = 100.0


def read_tsp_file(filename):
    coordinates = []
    edge_weight_type = "EUC_2D"

    with open(filename, 'r') as f:
        lines = f.readlines()
        reading_nodes = False

        for line in lines:
            line = line.strip()
            if line.startswith("EDGE_WEIGHT_TYPE"):
                edge_weight_type = line.split(":")[1].strip().upper()
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

    return coordinates, edge_weight_type


def calculate_att_distance(x1, y1, x2, y2):
    xd = x1 - x2
    yd = y1 - y2
    rij = math.sqrt((xd * xd + yd * yd) / 10.0)
    tij = int(round(rij))
    return tij + 1 if tij < rij else tij


def build_distance_matrix(coords, distance_type="EUC_2D"):
    n = len(coords)
    matrix = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = coords[i]
            x2, y2 = coords[j]

            if distance_type == "ATT":
                dist = calculate_att_distance(x1, y1, x2, y2)
            elif distance_type == "EUC_2D":
                dist = math.hypot(x1 - x2, y1 - y2)
            else:
                raise ValueError(f"Unsupported distance type: {distance_type}")

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


def polar_sort(coords):
    center_lat = sum(lat for lat, lon in coords) / len(coords)
    center_lon = sum(lon for lat, lon in coords) / len(coords)

    def angle(point):
        lat, lon = point
        return math.atan2(lat - center_lat, lon - center_lon)

    sorted_coords = sorted(enumerate(coords), key=lambda x: angle(x[1]))
    sorted_indices = [index for index, _ in sorted_coords]
    return sorted_indices
