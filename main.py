import random
from utils import functions

NUM_ANTS = 10
NUM_ITERATIONS = 50


def ant_colony_optimization(filename):
    coords = functions.read_tsp_file(filename)
    n = len(coords)
    distance_matrix = functions.build_distance_matrix(coords)

    pheromone_matrix = functions.initialize_pheromones(n)

    best_length = float('inf')
    best_tour = None

    for iteration in range(NUM_ITERATIONS):
        ants = []
        lengths = []

        for ant in range(NUM_ANTS):
            visited = [False] * n
            tour = []
            total_length = 0.0

            start_city = random.randint(0, n - 1)
            visited[start_city] = True
            tour.append(start_city)

            for step in range(1, n):
                current_city = tour[step - 1]
                next_city = functions.choose_next_city(current_city, visited, n, pheromone_matrix, distance_matrix)
                visited[next_city] = True
                tour.append(next_city)
                total_length += distance_matrix[current_city][next_city]

            ants.append(tour)
            lengths.append(total_length)

            if total_length < best_length:
                best_length = total_length
                best_tour = tour

        functions.update_pheromones(ants, lengths, pheromone_matrix, distance_matrix, n)

        print(f"Iteration {iteration + 1}: Best Length = {best_length:.2f} km")

    return best_tour, best_length


if __name__ == '__main__':
    tsp_file = 'resources/berlin52.tsp'
    best_tour, best_length = ant_colony_optimization(tsp_file)

    print("\nBest tour:", best_tour)
    print("Best tour length:", best_length, "km")
