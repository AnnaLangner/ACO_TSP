import main
from tkinter import *
import matplotlib.pyplot as plt
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


selected_file_path = ""


def choose_file():
    global selected_file_path
    file_path = filedialog.askopenfilename(
        title="Select a TSP file",
        filetypes=[("TSP files", "*.tsp"), ("All files", "*.*")]
    )
    if file_path:
        selected_file_path = file_path
        file_label.config(text=f"Selected file: {file_path}")


def draw_chart(lengths):
    for widget in chart_frame.winfo_children():
        widget.destroy()

    fig = plt.Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(range(1, len(lengths) + 1), lengths, marker='')
    ax.set_title("Best Tour Length Over Iterations")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Length (km)")
    ax.grid(True)

    chart = FigureCanvasTkAgg(fig, master=chart_frame)
    chart.draw()
    chart.get_tk_widget().pack()


def get_parameters():
    global selected_file_path
    try:
        if not selected_file_path:
            result_label.config(text="Please select a .tsp file first.")
            return

        number_of_ants = int(ants_entry.get())
        number_of_iterations = int(iterations_entry.get())
        rho = float(evaporation_entry.get())

        if not (1 <= number_of_ants <= 100):
            result_label.config(text="Number of ants must be between 1 and 100.")
            return
        if not (1 <= number_of_iterations <= 1000):
            result_label.config(text="Number of iterations must be between 1 and 1000.")
            return
        if not (0.1 <= rho <= 1.0):
            result_label.config(text="Evaporation rate must be between 0.1 and 1.0.")
            return

        result = main.ant_colony_optimization(selected_file_path, number_of_ants, number_of_iterations, rho)

        result_label.config(
            text=f"Best tour: {result['best_path']}\nBest tour length: {round(result['best_cost'], 2)} km"
        )

        draw_chart(result["lengths_over_time"])

    except ValueError:
        result_label.config(text="Please enter valid numbers.")
    except Exception as e:
        result_label.config(text=f"Error: {e}")


root = Tk()
root.title("ACO TSP - Traveling Salesman Problem")

frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm, text="Ant Colony Optimization for the Traveling Salesman Problem").grid(
    column=0, row=0, columnspan=2, pady=5)

ttk.Button(frm, text="Choose TSP File", command=choose_file).grid(column=0, row=1, columnspan=2)
file_label = ttk.Label(frm, text="No file selected")
file_label.grid(column=0, row=2, columnspan=2, pady=5)

ttk.Label(frm, text="Number of ants:").grid(column=0, row=3)
ants_entry = ttk.Entry(frm)
ants_entry.grid(column=1, row=3)

ttk.Label(frm, text="Number of iterations:").grid(column=0, row=4)
iterations_entry = ttk.Entry(frm)
iterations_entry.grid(column=1, row=4)

ttk.Label(frm, text="Pheromone evaporation rate (rho):").grid(column=0, row=5)
evaporation_entry = ttk.Entry(frm)
evaporation_entry.grid(column=1, row=5)

ttk.Button(frm, text="Run", command=get_parameters).grid(column=0, row=7, columnspan=2, pady=10)
ttk.Button(frm, text="Quit", command=root.quit).grid(column=1, row=7)

result_label = ttk.Label(frm, text="", foreground="blue")
result_label.grid(column=0, row=8, columnspan=2, pady=10)
chart_frame = ttk.Frame(frm)
chart_frame.grid(column=0, row=10, columnspan=2, pady=10)


root.mainloop()
