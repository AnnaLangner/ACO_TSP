import main
from tkinter import *
from tkinter import ttk
from utils import functions
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def get_parameters():
    try:
        tsp_file = str(tsp_entry.get())
        number_of_ants = int(ants_entry.get())
        number_of_iterations = int(iterations_entry.get())
        rho = float(evaporation_entry.get())

        if not isinstance(tsp_file, str):
            print("Enter the path to the file as a string.")
            return
        if not (1 <= number_of_ants <= 100):
            print("Number of ants must be between 1 and 100.")
            return
        if not (1 <= number_of_iterations <= 1000):
            print("Number of iterations must be between 1 and 1000.")
            return
        if not (0.1 <= rho <= 1.0):
            print("Pheromone evaporation rate must be between 0.1 and 1.0.")
            return

        result = main.ant_colony_optimization(tsp_file, number_of_ants, number_of_iterations, rho)

        result_label.config(text=f"Best tour: {result['best_path']}\nBest tour length: {result['best_cost']} km")

        coords = functions.read_tsp_file(tsp_file)
        show_plot_in_tkinter(coords, result['best_path'])

    except ValueError:
        result_label.config(text="Please enter valid numbers.")
    except Exception as e:
        result_label.config(text=f"Error: {e}")


root = Tk()
canvas_widget = None
root.title("ACO TSP - Traveling Salesman Problem")

frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm, text="Implementation of the ACO ant algorithm in the traveling salesman problem").grid(column=0, row=0, columnspan=2)

ttk.Label(frm, text="Enter the selected parameters").grid(column=0, row=1, columnspan=2)

ttk.Label(frm, text="Path to tsp file:").grid(column=0, row=2)
tsp_entry = ttk.Entry(frm)
tsp_entry.grid(column=1, row=2)

ttk.Label(frm, text="Number of ants:").grid(column=0, row=3)
ants_entry = ttk.Entry(frm)
ants_entry.grid(column=1, row=3)

ttk.Label(frm, text="Number of iterations:").grid(column=0, row=4)
iterations_entry = ttk.Entry(frm)
iterations_entry.grid(column=1, row=4)

ttk.Label(frm, text="Pheromone evaporation rate:").grid(column=0, row=5)
evaporation_entry = ttk.Entry(frm)
evaporation_entry.grid(column=1, row=5)

ttk.Button(frm, text="Submit", command=get_parameters).grid(column=0, row=7, columnspan=2)
ttk.Button(frm, text="Quit", command=root.quit).grid(column=1, row=7)

result_label = ttk.Label(frm, text="", foreground="blue")
result_label.grid(column=0, row=10, columnspan=2, pady=10)


def show_plot_in_tkinter(coords, tour):
    fig = Figure(figsize=(6, 4), dpi=100)
    plot = fig.add_subplot(111)

    x = [coords[city][0] for city in tour] + [coords[tour[0]][0]]
    y = [coords[city][1] for city in tour] + [coords[tour[0]][1]]

    plot.plot(x, y, 'o-', color='blue')
    for i, city in enumerate(tour):
        plot.text(coords[city][0], coords[city][1], str(city), fontsize=8, color='red')

    plot.set_title("ACO Best Tour")
    plot.set_xlabel("X")
    plot.set_ylabel("Y")
    plot.grid(True)

    global canvas_widget
    if canvas_widget:
        canvas_widget.get_tk_widget().destroy()

    canvas_widget = FigureCanvasTkAgg(fig, master=frm)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().grid(column=0, row=11, columnspan=2, pady=10)


root.mainloop()
