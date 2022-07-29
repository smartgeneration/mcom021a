# drawing a graph
import utilities.network as nw
import utilities.pyvis as vis

nw.load_graph(edge_file="rules.csv",
              edge_columns=['src', 'rule', 'dst'],
              node_file="nodes.csv",
              node_columns=['id', 'description', 'type', 'question', 'true_conclusion', 'false_conclusion'])

vis.draw(nw.G, edge_label_field='rule')