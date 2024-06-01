import os
import re
import sys
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.patches import Circle

from decentralizepy.graphs.MobilityGraph import MobilityGraph
from decentralizepy.graphs.MobilityNode import Direction


def find_last_graph_file(directory_path):
    pattern = re.compile(r'graph_(\d+).txt')

    files = os.listdir(directory_path)

    numbers = []
    for file in files:
        match = pattern.match(file)
        if match:
            numbers.append(int(match.group(1)))

    if numbers:
        last_file_number = max(numbers)
    else:
        last_file_number = None

    return last_file_number


def find_most_recent_experiment(base_directory):
    subfolders = [f.path for f in os.scandir(base_directory) if f.is_dir()]
    timestamps = []

    for folder in subfolders:
        try:
            folder_name = os.path.basename(folder)
            timestamp = datetime.strptime(folder_name, "%Y-%m-%dT%H:%M")
            timestamps.append((timestamp, folder))
        except ValueError:
            pass  # Ignore folders that don't match the timestamp format

    if timestamps:
        most_recent_folder = max(timestamps, key=lambda x: x[0])[1]
        return most_recent_folder
    else:
        return None


def read_coordinates_and_velocity(graph: MobilityGraph) -> tuple[
    list[tuple[float, float]], list[tuple[float, float]], list[float]]:
    positions = []
    mobility_vecs = []
    coverage_radii = [node.coverage_area_radius for node in graph.nodes]

    for node in graph.nodes:
        positions.append(node.pos_vec)

        m = node.mobility_prob_vec
        resultant_mobility_vec: tuple[float, float] = (m[Direction.RIGHT.value] - m[Direction.LEFT.value],
                                                       m[Direction.UP.value] - m[Direction.DOWN.value])
        unit_resultant_mobility_vec = np.array(resultant_mobility_vec) / np.linalg.norm(resultant_mobility_vec)

        mobility_vecs.append(unit_resultant_mobility_vec * node.velocity)

    return positions, mobility_vecs, coverage_radii


def update_plot(frame_number, data, scatter_plot, quiver_plot, circles, ax, colors):
    positions, _, coverage_radii = data[frame_number]

    scatter_plot.set_color(colors)
    scatter_plot.set_offsets(positions)
    quiver_plot.set_offsets(positions)

    for circle in circles:
        circle.remove()
    circles.clear()

    for pos, radius in zip(positions, coverage_radii):
        circle = Circle(pos, radius, fill=False, edgecolor='b')
        ax.add_patch(circle)
        circles.append(circle)

    return scatter_plot, quiver_plot, circles


def animate_graphs(graphs: list[MobilityGraph]):
    data = []
    for graph in graphs:
        positions, velocity_vectors, coverage_radii = read_coordinates_and_velocity(graph)
        data.append((positions, np.array(velocity_vectors), coverage_radii))
    if not data:
        print("No data found in the directory.")
        sys.exit(1)
    # Generate a list of colors
    positions, velocity_vectors, _ = data[0]
    positions = np.array(positions)
    num_points = len(positions)
    colors = np.random.rand(num_points, 3)
    fig, ax = plt.subplots()
    scatter_plot = ax.scatter([], [], c=[])
    quiver_plot = ax.quiver(positions[:, 0], positions[:, 1], velocity_vectors[:, 0], velocity_vectors[:, 1],
                            [i for i in range(num_points)])
    size = 500
    ax.set_xlim(-50, size + 50)
    ax.set_ylim(-50, size + 50)
    ani = animation.FuncAnimation(
        fig, update_plot, frames=len(data), fargs=(data, scatter_plot, quiver_plot, [], ax, colors), interval=1000,
        repeat=False
    )
    plt.show()
    return ani


def main(graphs_dir):
    last_graph_file_number = find_last_graph_file(graphs_dir)
    if last_graph_file_number is None:
        print("No graph files found in the directory.")
        sys.exit(1)

    graphs: list[MobilityGraph] = []
    for i in range(1, last_graph_file_number + 1):
        file_path = os.path.join(graphs_dir, f"graph_{i}.txt")
        if os.path.exists(file_path):
            g = MobilityGraph()
            g.read_graph_from_file(file_path)
            graphs.append(g)
        else:
            print(f"File graph_{i}.txt does not exist in the directory.")
            sys.exit(1)

    animate_graphs(graphs)


if __name__ == "__main__":
    directory_path = sys.argv[1]
    if (len(sys.argv) < 2):
        print("Usage: python animate_graph.py <directory_path>")
        sys.exit(1)

    main(directory_path)
