import networkx as nx
import pandas as pd

G = nx.DiGraph()
all_rules = {}

ISOLATED_NODE =0
LEAF_NODE = 1
INTERMEDIATE_NODE = 2
ROOT_NODE = 3

# ops = ['', 'n', 'a', 'o', 'na', 'no']
ops = ['', 'n', 'a', 'o', 'an', 'on']
exs = ['f"{value}"', 'f"not {value}"', 'f" and {value}"', 'f" or {value}"', 'f" and not {value}"', 'f" or not {value}"']


def get_node_type(id):
    in_degree  = G.in_degree(id)
    out_degree = G.out_degree(id)
    if in_degree==0 and out_degree==0:
        return ISOLATED_NODE # isolated node (nut co lap)
    elif in_degree==0 and out_degree>0:
        return LEAF_NODE # leaf node
    elif in_degree>0 and out_degree>0:
        return INTERMEDIATE_NODE # intermediate node (nut trung gian)
    else:
        return ROOT_NODE # root (nut goc) (nut ket luan)

def load_graph(edge_file, edge_columns, node_file=None, node_columns=None):
    df_edges = pd.read_csv(edge_file, names=edge_columns, sep=',', comment='#')
    attrs = [attr for attr in edge_columns if attr not in ['src','dst']]
    has_weight = 'weight' in attrs
    for index, row in df_edges.iterrows():
        G.add_edge(row['src'], row['dst'])
        edge = G.edges[row['src'], row['dst']]
        for attr in attrs:
            edge[attr]=row[attr]
        if not has_weight:
            edge['weight'] = 1

    if node_file != None and node_columns != None:
        df_nodes = pd.read_csv(node_file, names=node_columns, sep=',', comment='#')
        attrs = [attr for attr in node_columns if attr not in ['id']]
        for index, row in df_nodes.iterrows():
            G.add_node(row['id'])
            for attr in attrs:
                G.nodes[row['id']][attr] = row[attr]

def get_nodes(node_type: int):
    lst = []
    for node in G.nodes():
        if get_node_type(node[0]) == node_type:
            lst.append(node)
    return lst

def load_all_rules():
    rules = {}
    for u,v,data in G.edges(data=True):
        r, n, op = data['rule'].split(';')
        rule_data = rules.get(r, [])
        rule_data.append((n, op, u, v))
        rules[r] = rule_data

    keys = sorted(rules.keys())
    for key in keys:
        all_rules[key] = sorted(rules[key], key=lambda x: x[0])

def evaluate_rule(key):
    exp = ""
    for (n, op, u, v) in all_rules[key]:
        index = ops.index(op)
        node = G.nodes[u]
        value = node.get('value')
        if value == None:
            if get_node_type(u) == LEAF_NODE:
                des = node['description']
                question = f"{u}: {node['question']} (Y/N): "
                value=node['value'] = input(question).lower()=='y'
            else:
                pass
                # return False
        result = eval(exs[index])
        # print(result)
        exp += result
    # print("Exp:", exp)
    # print(v)
    # print("Exp:", eval(exp))
    conclusion_node = G.nodes[v]
    conclusion_node['value']=eval(exp)
    # print(v, conclusion_node['value'])
    # return True

#------------------------------------------------------------
# BACKWARD REASONING
#------------------------------------------------------------
def get_rule_keys(source_list:list, v):
    keys = []
    for u in source_list:
        data = G.edges[u,v]
        r, n, op = data['rule'].split(';')
        if r not in keys:
            keys.append(r)
    return keys


def execute_backward_reasoning(chosen_id):
    # backward
    # print('Backward processing...')
    stack = []
    queue = [chosen_id]
    id_set = {chosen_id} #set of processed nodes

    while queue:
        id = queue.pop(0) #dequeue
        predecessors = list(G.predecessors(id))
        # queue.enqueu(predecessors not in id_set)
        for predecessor in predecessors:
            if predecessor not in id_set:
                queue.append(predecessor) #enqueue
        # id_set.add(predecessors)
        id_set.update(predecessors)
        # rule_keys = get keys of rules from predecessors to id
        rule_keys = get_rule_keys(predecessors, id)
        # stack.push(rules)
        stack.extend(rule_keys)
    # forward
    # print('Forward processing...')
    print('-' * 60, '\nVui lòng trả lời các câu hỏi:')
    while stack:
        rule_key = stack.pop()
        evaluate_rule(rule_key)
    # Conclusion
    # show conclusion of G.nodes[chosen_id]
    print('-' * 60, '\nKết luận:')
    node = G.nodes[chosen_id]
    conclusion = node['true_conclusion'] if node['value'] else node['false_conclusion']
    print(f"[{id}:{str(node['value'])}]: {conclusion}")

#------------------------------------------------------------
# FORWARD REASONING
#------------------------------------------------------------
def get_base_rule_keys(leaf_nodes):
    base_rules_keys = set()
    for key in all_rules:
        flag = True
        value = all_rules[key]
        for (n,op,u,v) in value:
            if u not in leaf_nodes:
                flag = False
                break
        if flag:
            base_rules_keys.add(key)
    return base_rules_keys

def evaluate_rules(keys: set):
    for key in keys:
        evaluate_rule(key)

def is_ready_rule(key):
    rule_value = all_rules[key]
    for (n, op, u, v) in rule_value:
        node = G.nodes[u]
        if get_node_type(u) != LEAF_NODE and G.nodes[u].get('value') is None:
            return False
    return True

def execute_forward_reasoning():
    leaf_nodes = get_nodes(LEAF_NODE)
    base_rule_keys = get_base_rule_keys(leaf_nodes)
    evaluate_rules(base_rule_keys)
    not_evaluated_rule_keys = all_rules.keys() - base_rule_keys
    while not_evaluated_rule_keys:
        for key in not_evaluated_rule_keys.copy():
            rule = all_rules[key]
            if is_ready_rule(key):
                evaluate_rule(key)
                not_evaluated_rule_keys.remove(key)
            # print(not_evaluated_rule_keys)

    print('-' * 60, '\nKết luận:')
    conclusion_nodes = get_nodes(ROOT_NODE)
    for id in conclusion_nodes:
        node = G.nodes[id]
        conclusion = node['true_conclusion'] if node['value'] else node['false_conclusion']
        print(f"[{id}:{str(node['value']):<5}]: {conclusion}")

#------------------------------------------------------------
# UTILITIES
#------------------------------------------------------------
def split_rule(original_rule):
    # original_rule = "4,~A^~F^G,H"
    id, premise, dst = original_rule.split(',')
    queue = []
    for i in range(len(premise)):
        c = premise[i]
        if c == '^':
            queue.append('a') # enqueue
            premise = str(premise).replace(c,',',1)
        elif c == 'v':
            queue.append('o')  # enqueue
            premise = str(premise).replace(c, ',', 1)

    lst = []
    ps = premise.split(',')
    r = f"r{id}"
    n = 0
    for p in ps:
        n += 1
        op = ''
        if n > 1:
            op = queue.pop(0)  # dequeue
        src = p
        if p[0]=='~':
            op += 'n'
            src = p[1:]
        rule_n = f"{src},{r};{n};{op},{dst}"
        print(rule_n)
        lst.append(rule_n)
    return lst




