# forward reasoning example
import utilities.network as nw
import utilities.pyvis as vis

# load the graph from files
nw.load_graph(edge_file="rules.csv",
              edge_columns=['src', 'rule', 'dst'],
              node_file="nodes.csv",
              node_columns=['id', 'description', 'type', 'question', 'true_conclusion', 'false_conclusion'])

# load all rules
nw.load_all_rules()

# execute backward reasoning
nw.execute_forward_reasoning()

# vis.draw(nw.G, edge_label_field='rule')
