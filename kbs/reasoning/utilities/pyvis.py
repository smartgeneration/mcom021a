import networkx as nx
from pyvis.network import Network
from . import network as nw

def draw(G: nx.DiGraph, edge_label_field=None, node_type=None, output_file='graph.html'):
    '''
    Drawing a networkx graph
    :param G: the graph
    :param edge_label_field: an edge attribute is used as the edge label
    :param node_type: a node attribute is used as the node type
    :param output_file: a file name is used to output the graph
    :return: none
    '''
    g = Network(height='100%', width='100%', bgcolor='white', directed=True)
    g.force_atlas_2based(spring_length=100)
    node_size = 16
    node_font = "16px sans-serif maroon"
    edge_font = "16px sans-serif navy"
    for (src,dst,data) in G.edges(data=True):
        edge_label = data[edge_label_field] if edge_label_field else f"{src}-{dst}"
        if node_type:
            src_node_type = G.nodes[src][node_type]
            dst_node_type = G.nodes[dst][node_type]
        else:
            src_node_type = nw.get_node_type(src)
            dst_node_type = nw.get_node_type(dst)
        src_node_value = G.nodes[src].get('value', '')
        dst_node_value = G.nodes[dst].get('value', '')
        g.add_node(src, label=f"{src}:{src_node_type}:{src_node_value}", size=node_size, group=src_node_type, font=node_font)
        g.add_node(dst, label=f"{dst}:{dst_node_type}:{dst_node_value}", size=node_size, group=dst_node_type, font=node_font)
        g.add_edge(src, dst, label=edge_label, font=edge_font)

    g.set_edge_smooth('dynamic')
    g.show(output_file)
