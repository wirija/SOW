
stylesheet = [
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)',
            'font-size': '12px',
            'background-color': '#ADD8E6', # Light Blue
            'border-width': 2,
            'border-color': '#555',
            'width': 'mapData(size, 40, 100, 40, 100)', # Map 'size' attribute to actual node width/height
            'height': 'mapData(size, 40, 100, 40, 100)',
            'text-valign': 'center',
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
            'background-color': '#FFD700' # Gold
        }
    },
    {
        'selector': '.Company',
        'style': {
            'background-color': '#FF6347' # Tomato
        }
    },
    {
        'selector': '.Product',
        'style': {
            'background-color': '#90EE90' # Light Green
        }
    },
    # Styling for relationships
    {
        'selector': '.works_for',
        'style': {
            'line-color': '#4682B4' # Steel Blue
        }
    },
    {
        'selector': '.sells',
        'style': {
            'line-color': '#DAA520' # Goldenrod
        }
    },
    {
        'selector': '.friends',
        'style': {
            'line-color': '#8A2BE2' # Blue Violet
        }
    }
]