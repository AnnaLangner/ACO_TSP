import random
import argparse
from utils import functions


def ant_colony_optimization(filename, num_ants, num_iterations, rho, start_city=None):
    coords = functions.read_tsp_file(filename)
    n = len(coords)
    distance_matrix = functions.build_distance_matrix(coords)
    pheromone_matrix = functions.initialize_pheromones(n)

    best_length = float('inf')
    best_tour = None
    iteration_lengths = []

    for iteration in range(num_iterations):
        ants = []
        lengths = []

        for ant in range(num_ants):
            visited = [False] * n
            tour = []
            total_length = 0.0

            sc = start_city - 1 if start_city is not None else random.randint(0, n - 1)
            visited[sc] = True
            tour.append(sc)

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

        iteration_lengths.append(best_length)
        functions.update_pheromones(ants, lengths, pheromone_matrix, distance_matrix, n, rho, num_ants)

        # Left for debugging purposes
        # print(f"Iteration {iteration + 1}: Best Length = {best_length:.2f} km")

    return {
        'best_path': best_tour,
        'best_cost': best_length,
        'progress': iteration_lengths
    }


if __name__ == '__main__':
    tsp_file = 'resources/berlin52.tsp'
    parser = argparse.ArgumentParser(description="Ant Colony Optimization for TSP")
    parser.add_argument("tsp_file", type=str, help="Path to the TSP file")
    parser.add_argument("--num_ants", type=int, default=50, help="Number of ants (default: 50)")
    parser.add_argument("--num_iterations", type=int, default=100, help="Number of iterations (default: 100)")
    parser.add_argument("--rho", type=float, default=0.3, help="Number of rho between 0.1 and 1")
    parser.add_argument("--start_city", type=int, default=1, help="A number describing the starting city for the berlin52.tsp file, values from 1 to 52, for the att48.tsp file, values from 1 to 48")
    args = parser.parse_args()

    result = ant_colony_optimization(
        args.tsp_file,
        args.num_ants,
        args.num_iterations,
        args.rho,
        args.start_city
    )

    coords = functions.read_tsp_file(args.tsp_file)
    print("\nBest tour:", result['best_path'])
    print("Best tour length:", result['best_cost'], "km")

    functions.plot_tour(coords, result['best_path'], title="ACO Best Tour")
