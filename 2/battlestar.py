def dfs(dag: dict, starting_node: str, end_node: str) -> int:
    """
    Returns number of different paths in a DAG from starting_node to end_node
      Variation of Depth First Search algorithm for a Directed Acyclic Graph
        The number of paths from s to t in a DAG can be calculated with the following recursion
        Paths(s) = 1                              if s == t
                   sum(Paths[children of s])      otherwise
        Implemented using dynamic programming, so the cost of the algorithm growths linearly with the graph size
    :param dag: dict Directed Acyclic Graph for which the namber of paths is to be calculated
                Each node of the graph is represented as a key:value pair. Key is the name of the planet
                and value is an object with two properties
                    children: list[str] names of the node's children
                    npaths: int number of different paths to the end_node, is None if not computed yet
    :param starting_node:
    :param end_node:
    :return: int number of paths
    """
    if starting_node == end_node:
        return 1
    else:
        if dag[starting_node]["npaths"] is None:  # Apply dinamic programming to avoid computing npaths more than once
            dag[starting_node]["npaths"] = sum(map(
                lambda child: dfs(dag, child, end_node),
                dag[starting_node]["children"]))
        return dag[starting_node]["npaths"]


def build_dag(file) -> dict:
    """
    Parses input into a Directed Acyclic Graph
    :param file: filePointer file that contains the case
    :return: dict Directed acyclic graph which contains the nodes and their children
    """
    nodes = {}
    n_planets = int(file.readline())
    for planet in range(n_planets):
        planet_info = file.readline().strip().split(':')
        nodes[planet_info[0]] = {
            "children": planet_info[1].split(','),
            "npaths": None
        }

    return nodes


input_file = "testInput.txt"
output_file = input_file.replace("Input", "Output")

f_in = open(input_file, 'r')
n_cases = int(f_in.readline())

with open(output_file, "w+") as f:
    for index, case in enumerate(range(n_cases)):
        dag = build_dag(f_in)
        paths = dfs(dag, "Galactica", "New Earth")
        f.write(f'Case #{index + 1}: {paths}\n')
