import random
import argparse
from utils import functions


def ant_colony_optimization(filename, num_ants, num_iterations, rho):
    import matplotlib.pyplot as plt
    coords = functions.read_tsp_file(filename)
    n = len(coords)
    distance_matrix = functions.build_distance_matrix(coords)
    pheromone_matrix = functions.initialize_pheromones(n)

    best_length = float('inf')
    best_tour = None
    best_lengths_over_time = []

    for iteration in range(num_iterations):
        ants = []
        lengths = []

        for _ in range(num_ants):
            visited = [False] * n
            tour = []
            total_length = 0.0

            start_city = random.randint(0, n - 1)
            visited[start_city] = True
            tour.append(start_city)

            for step in range(1, n):
                current_city = tour[-1]
                next_city = functions.choose_next_city(current_city, visited, n, pheromone_matrix, distance_matrix)
                if next_city == -1:
                    break
                visited[next_city] = True
                tour.append(next_city)
                total_length += distance_matrix[current_city][next_city]

            ants.append(tour)
            lengths.append(total_length)

            if total_length < best_length:
                best_length = total_length
                best_tour = tour

        best_lengths_over_time.append(best_length)
        functions.update_pheromones(ants, lengths, pheromone_matrix, distance_matrix, n, rho, num_ants)

        # Debug output
        # print(f"Iteration {iteration + 1}: Best Length = {best_length:.2f} km")

    return {
        'best_path': best_tour,
        'best_cost': best_length,
        'lengths_over_time': best_lengths_over_time,
        'coordinates': coords
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ant Colony Optimization for TSP")
    parser.add_argument("tsp_file", type=str, help="Path to the TSP file")
    parser.add_argument("--num_ants", type=int, default=50, help="Number of ants (default: 50)")
    parser.add_argument("--num_iterations", type=int, default=100, help="Number of iterations (default: 100)")
    parser.add_argument("--rho", type=float, default=0.3, help="Pheromone evaporation rate (0 < rho < 1)")
    args = parser.parse_args()

    result = ant_colony_optimization(args.tsp_file, args.num_ants, args.num_iterations, args.rho)
    print("\nBest tour:", result['best_path'])
    print("Best tour length:", round(result['best_cost'], 2), "km")
