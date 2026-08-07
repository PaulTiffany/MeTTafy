COLORS = ("red", "green", "blue", "yellow")


def valid_color(vertex, color, graph, coloring):
    return all(coloring.get(neighbor) != color for neighbor in graph[vertex])


def color_graph(graph):
    vertices = list(graph)
    coloring = {}

    def search(index):
        if index == len(vertices):
            return True

        vertex = vertices[index]
        for color in COLORS:
            if valid_color(vertex, color, graph, coloring):
                coloring[vertex] = color
                if search(index + 1):
                    return True
                coloring[vertex] = None

        return False

    return coloring if search(0) else None


if __name__ == "__main__":
    graph = {
        "A": {"B", "C"},
        "B": {"A", "C", "D"},
        "C": {"A", "B", "D"},
        "D": {"B", "C"},
    }
    print(color_graph(graph))
