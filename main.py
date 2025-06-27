import os
from flask import Flask, render_template, request
from utils.functions import draw_chart, draw_path_plot, ant_colony_optimization


app = Flask(__name__)
RESOURCES_FOLDER = 'resources'


@app.route("/", methods=["GET", "POST"])
def index():
    tsp_files = os.listdir(RESOURCES_FOLDER)

    if request.method == "POST":
        selected_filename = request.form.get("selected_file")

        if not selected_filename:
            return render_template("index.html", tsp_files=tsp_files, error="No file selected.")

    if request.method == "POST":
        selected_filename = request.form.get("selected_file")
        num_ants = int(request.form.get("num_ants", 50))
        num_iterations = int(request.form.get("num_iterations", 100))
        rho = float(request.form.get("rho", 0.3))

        filepath = os.path.join(RESOURCES_FOLDER, selected_filename)

        if os.path.exists(filepath):
            result = ant_colony_optimization(filepath, num_ants, num_iterations, rho)
            draw_chart(result["lengths_over_time"], filename="static/chart.png")
            draw_path_plot(result["best_path"], result["coordinates"], filename="static/path.png")

            return render_template(
                "index.html",
                tsp_files=tsp_files,
                result=result,
                best_cost=round(result["best_cost"], 2),
                best_path=result["best_path"],
                chart_path="static/chart.png",
                path_image="static/path.png"
            )
        else:
            return render_template("index.html", tsp_files=tsp_files, error="The file does not exist.")

    return render_template("index.html", tsp_files=tsp_files)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

