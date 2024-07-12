import networkx as nx
import matplotlib.pyplot as plt
from tabulate import tabulate

def calculate_flows(process_flow, initial_flow=1000):
    G = nx.DiGraph()
    flows = {}

    # Add nodes and edges to the graph
    for node in process_flow['nodes']:
        G.add_node(node['id'], name=node['name'])

    for edge in process_flow['edges']:
        G.add_edge(edge['from'], edge['to'], stream=edge['stream'])

    # Calculate flows
    flows[process_flow['streams'][0]['variable_name']] = initial_flow

    for node in process_flow['nodes']:
        local_vars = flows.copy()
        for param in node['parameters']:
            local_vars[param['name']] = param['value']

        # Execute auxiliary calculations first
        for calc in node['auxiliary_calculations']:
            exec(calc['formula'], globals(), local_vars)

        # Then execute main calculations
        for calc in node['main_calculations']:
            exec(calc['formula'], globals(), local_vars)

        flows.update(local_vars)

    return G, flows

def generate_flow_table(process_flow, flows):
    table_data = []
    for node in process_flow['nodes']:
        for input_stream in node['inputs']:
            table_data.append([
                node['name'],
                input_stream['variable_name'],
                flows.get(input_stream['variable_name'], 'N/A'),
                'Input',
                node['name'],
                input_stream['type']
            ])
        for output_stream in node['outputs']:
            table_data.append([
                node['name'],
                output_stream['variable_name'],
                flows.get(output_stream['variable_name'], 'N/A'),
                node['name'],
                'Output',
                output_stream['type']
            ])

    headers = ['Unit Operation', 'Stream', 'Flow (kg/hr)', 'Source', 'Destination', 'Type']
    return tabulate(table_data, headers=headers, tablefmt='grid')

def visualize_flow_diagram(G, flows, process_flow, ax):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue', node_size=3000, font_size=8, font_weight='bold')

    edge_labels = {}
    for u, v, data in G.edges(data=True):
        stream = data['stream']
        flow = flows.get(stream['variable_name'], 'N/A')
        edge_labels[(u, v)] = f"{stream['variable_name']}\n{flow:.2f} kg/hr\n({stream['type']})"

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, ax=ax)

    ax.set_title(f"{process_flow['name']} Flow Diagram")
    ax.axis('off')

# Ensure the function is available for import
__all__ = ['calculate_flows', 'generate_flow_table', 'visualize_flow_diagram']