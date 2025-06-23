import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_cytoscape as cyto
import networkx as nx

# 1. Create a NetworkX graph
G = nx.DiGraph()

# Add nodes with 'type' attributes
G.add_nodes_from([
    ('Alice', {'type': 'Person', 'label': 'Alice', 'size': 50, 'concentric': 2}),
    ('Bob', {'type': 'Person', 'label': 'Bob', 'size': 50, 'concentric': 2}),
    ('CompanyA', {'type': 'Company', 'label': 'Company A', 'size': 50, 'concentric': 2}),
    ('CompanyB', {'type': 'Company', 'label': 'Company B', 'size': 50, 'concentric': 2}),
    ('Charlie', {'type': 'Person', 'label': 'Charlie', 'size': 50, 'concentric': 2}),
    ('William', {'type': 'Person', 'label': 'William', 'size': 50, 'concentric': 2}),
    ('Tim', {'type': 'Person', 'label': 'Tim', 'size': 50, 'concentric': 2}),
    ('CompanyC', {'type': 'Company', 'label': 'Company C', 'size': 50, 'concentric': 2}),
    ('CompanyD', {'type': 'Company', 'label': 'Company D', 'size': 50, 'concentric': 2}),
    ('CompanyE', {'type': 'Company', 'label': 'Company E', 'size': 50, 'concentric': 2}),
])

# Add edges with 'relationship' attributes
G.add_edges_from([
    ('CompanyE', 'CompanyA', {'relationship': 'Transfers'}),
    ('CompanyA', 'CompanyB', {'relationship': 'Transfers'}),
    ('CompanyA', 'CompanyC', {'relationship': 'Transfers'}),
    ('CompanyA', 'CompanyD', {'relationship': 'Transfers'}),
    # ('CompanyA', 'William', {'relationship': 'Transfers'}),
    ('Alice', 'CompanyE', {'relationship': 'Transfers'}),
    ('Charlie', 'CompanyE', {'relationship': 'Transfers'}),
    # ('Tim', 'CompanyE', {'relationship': 'Transfers'}),
    # ('Bob', 'CompanyE', {'relationship': 'Transfers'}),
])

# Convert NetworkX graph to Cytoscape.js elements format
# This is crucial for dash-cytoscape

def nx_to_cytoscape_elements(graph):
    cy_elements = []
    for node, data in graph.nodes(data=True):
        cy_elements.append({
            'data': {'id': str(node), 'label': data.get('label', str(node)), **data}, # Use str(node) for IDs
            'classes': data.get('type', '') # Use 'type' as a class for styling/filtering
        })
    for source, target, data in graph.edges(data=True):
        # print (f"source ={source}, target = {target}")
        cy_elements.append({
            'data': {'source': str(source), 'target': str(target), 'label': data.get('relationship', ''), **data}, # Use str(source/target) for IDs
            'classes': data.get('relationship', '') # Use 'relationship' as a class for styling/filtering
        })
    return cy_elements

initial_elements = nx_to_cytoscape_elements(G)

# Define default stylesheet for nodes and edges
stylesheet = [
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)',
            'font-size': '12px',
            'background-color': '#ADD8E6', # Light Blue
            'border-width': 2,
            'border-color': '#555',
            'width': 'mapData(size, 40, 100, 20, 50)', # Map 'size' attribute to actual node width/height
            'height': 'mapData(size, 40, 100, 20, 50)',
            'text-valign': 'bottom',
            'text-halign': 'center',
            'color': 'black'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'label': 'data(label)',
            'font-size': '10px',
            'line-color': '#ccc',
            'target-arrow-color': '#ccc',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier'
        }
    },
    # Specific styling for node types (classes)
    {
        'selector': '.Company',
        'style': {
            'background-color': 'white', # Set background to white
            'shape': 'square', # Keep shape if desired, or change to 'ellipse' for cir
            'background-image': r'/assets/Company.png',
            'background-width': '50%', # Adjust icon size relative to node
            'background-height': '50%',
            'background-position-x': '50%', # Center the icon
            'background-position-y': '50%',
            'background-fit': 'contain',
            'background-clip': 'node',
            'background-repeat': 'no-repeat',
            'border-width': 0, # Set border width to 0
            'border-color': 'transparent' # Ensure no visible border color
        }
    },
        {
        'selector': '.Person',
        'style': {
            'background-color': 'white', # Set background to white
            'shape': 'square', # Keep shape if desired, or change to 'ellipse' for cir
            'background-image': r'/assets/Person.svg',
            'background-width': '50%', # Adjust icon size relative to node
            'background-height': '50%',
            'background-position-x': '50%', # Center the icon
            'background-position-y': '50%',
            'background-fit': 'contain',
            'background-clip': 'node',
            'background-repeat': 'no-repeat',
            'border-width': 0, # Set border width to 0
            'border-color': 'transparent' # Ensure no visible border color
        }
    },
        {
        'selector': '.PhoneNumber',
        'style': {
            'background-color': 'white', # Set background to white
            'shape': 'square', # Keep shape if desired, or change to 'ellipse' for cir
            'background-image': r'/assets/Phone.png',
            'background-width': '50%', # Adjust icon size relative to node
            'background-height': '50%',
            'background-position-x': '50%', # Center the icon
            'background-position-y': '50%',
            'background-fit': 'contain',
            'background-clip': 'node',
            'background-repeat': 'no-repeat',
            'border-width': 0, # Set border width to 0
            'border-color': 'transparent' # Ensure no visible border color
        }
    },
        {
        'selector': '.Email',
        'style': {
            'background-color': 'white', # Set background to white
            'shape': 'square', # Keep shape if desired, or change to 'ellipse' for cir
            'background-image': r'/assets/Email.png',
            'background-width': '50%', # Adjust icon size relative to node
            'background-height': '50%',
            'background-position-x': '50%', # Center the icon
            'background-position-y': '50%',
            'background-fit': 'contain',
            'background-clip': 'node',
            'background-repeat': 'no-repeat',
            'border-width': 0, # Set border width to 0
            'border-color': 'transparent' # Ensure no visible border color
        }
    },
]

# Initialize Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1("Dynamic Network Visualization with Dash Cytoscape", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Filter Nodes by Type:"),
        dcc.Dropdown(
            id='node-type-filter',
            options=[
                {'label': 'All', 'value': 'all'},
                {'label': 'Person', 'value': 'Person'},
                {'label': 'Company', 'value': 'Company'},
                {'label': 'Product', 'value': 'Product'}
            ],
            value='all', # Default value
            clearable=False,
            style={'width': '200px'}
        )
    ], style={'padding': '20px', 'display': 'flex', 'alignItems': 'center'}),

    cyto.Cytoscape(
        id='cytoscape-graph',
        #layout={'name': 'cose'}, # Other options: 'grid', 'circle', 'concentric', 'breadthfirst', 'random', 'preset'
        layout={
            'name': 'cose',
            # 'concentric': 'function(node){ return node.data("concentric"); }', # Tell it to use our custom level attribute
            # 'levelWidth': 70,
            # 'minNodeSpacing': 15,
            # 'equidistant': False,
            # 'startAngle': 3/2 * 3.14159,
            # 'sweep': None,
            # 'clockwise': True,
            # 'animate': True,
            # 'animationDuration': 500
        },
        style={'width': '100%', 'height': '600px', 'border': '1px solid #ddd'},
        elements=initial_elements,
        stylesheet=stylesheet,
        # Allow user interaction
        zoom=1,
        minZoom=0.1,
        maxZoom=2,
        boxSelectionEnabled=True,
        autoungrabify=False, # Allows nodes to be dragged even if grabbed
        autounselectify=False # Allows nodes to be selected without automatically unselecting others
    )
])

# Define callback for dynamic filtering
@app.callback(
    Output('cytoscape-graph', 'elements'),
    Input('node-type-filter', 'value')
)
def update_graph_elements(selected_type):
    if selected_type == 'all':
        return initial_elements
    else:
        filtered_elements = []
        for element in initial_elements:
            if 'data' in element and 'id' in element['data']: # It's a node
                if 'classes' in element and selected_type in element['classes']:
                    filtered_elements.append(element)
            elif 'data' in element and 'source' in element['data'] and 'target' in element['data']: # It's an edge
                # Check if both connected nodes are in the filtered set
                source_node_id = element['data']['source']
                target_node_id = element['data']['target']

                # Find if source and target are in the currently filtered nodes
                is_source_visible = any(
                    e['data'].get('id') == source_node_id and selected_type in e.get('classes', '')
                    for e in initial_elements if 'id' in e.get('data', {})
                )
                is_target_visible = any(
                    e['data'].get('id') == target_node_id and selected_type in e.get('classes', '')
                    for e in initial_elements if 'id' in e.get('data', {})
                )

                if is_source_visible and is_target_visible:
                    filtered_elements.append(element)
        return filtered_elements

# Run the app
if __name__ == '__main__':
    app.run(debug=True)