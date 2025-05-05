# Implementation of the ACO ant algorithm in the traveling salesman problem

## Project goal
The aim of the project is to write a web application that uses the ant algorithm to 
solve the zero traveling salesman problem (TSP). The application is to find an optimal 
route that visits all cities exactly once and returns to the starting city, minimizing 
the total distance covered in the trip.

## Description

First, I calculated the great-circle distance between two points on the Earth's surface given their latitudes and longitudes using the formula Haversine.
Read the .tsp file to extract the coordinates of the nodes (cities) in the TSP instance.
Using the build_distance_matrix function constructs a distance matrix based on the coordinates read from a .tsp file.
I define the pheromone matrix with small values. The pheromones will be updated as the ants traverse the paths.
Using the choose_next_city function I select the next city for each ant based on its pheromone trail and distance (using a probabilistic approach).
After each iteration, I call the update_pheromones function, which evaporates some pheromones and adds new pheromones to the matrix based on the ant routes.


When choosing next city, it is important raising the pheromone level to a power (using exponentiation) introduces a non-linear relationship between 
the pheromone levels and their influence on the ant’s decision. This makes the algorithm more sensitive to paths with higher pheromone concentrations, 
which helps ants converge towards the optimal path over time.

* If ALPHA = 1, the pheromone level has a linear effect on the decision-making.

* If ALPHA > 1, the pheromone influence becomes stronger, so ants are more likely to follow paths that have a higher pheromone concentration.

* If ALPHA < 1, the pheromone influence becomes weaker, making ants less sensitive to pheromones and more likely to explore other paths.

The BETA parameter controls how much influence the distance has on the ant's decision-making process.
BETA is a constant exponent that determines how strongly the ant's movement is influenced by the distance between cities.
Raising the inverse of the distance to the power of BETA introduces a non-linear relationship between distance and decision-making:

* If BETA = 1: The influence of distance is linear. The inverse distance has a direct, proportional impact on the decision.

* If BETA > 1: The influence of distance becomes stronger. Shorter distances will have a disproportionately higher probability of being chosen by the ants.

* If BETA < 1: The influence of distance becomes weaker, meaning ants may consider paths that are longer (though still influenced by the pheromone levels).

## Running project

To run backend in the terminal with argument , type ```python3 main.py 'resources/berlin52.tsp' --num_ants 20 --num_iterations 10 --rho 0.3```

To run user interface in terminal type ```python3 aco_tsp_gui.py```
A user window will appear where you can add parameters such as:
* Path to tsp file `resources/att48.tsp`
* Number of ants `50`
* Number of iterations `100`
* Pheromone evaporation rate `0.3`
* index of city `5`

After clicking the submit button, the best route is calculated. It gives the city numbers in the order the ant passed through, as well as the best route length.

Two graphs will appear under the calculated data. The first shows the best route, and the second shows how the length of the routes changed depending on the iteration performed.
