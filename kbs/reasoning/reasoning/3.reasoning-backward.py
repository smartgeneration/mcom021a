# backward reasoning example
import utilities.network as nw

# load the graph from files
nw.load_graph(edge_file="rules.csv",
              edge_columns=['src', 'rule', 'dst'],
              node_file="nodes.csv",
              node_columns=['id', 'description', 'type', 'question', 'true_conclusion', 'false_conclusion'])

# display menu
root_nodes = nw.get_nodes(nw.ROOT_NODE)
print("Bạn muốn kiểm tra nội dung gì?")
for id in root_nodes:
    des = nw.G.nodes[id]['description']
    print(f"{id}. {des}")
chosen_id = input("Nhập chọn lựa của bạn: ").upper()
if chosen_id not in root_nodes:
    print("Bạn đã nhập chọn lựa ngoài danh mục")
    quit(0)

# load all rules
nw.load_all_rules()

# execute backward reasoning
nw.execute_backward_reasoning(chosen_id)
