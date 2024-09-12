from dash import dcc, html

layout = html.Div([
    dcc.Graph(id='annealing-graph', style={'height': '800px'}), 
    dcc.Graph(id='iterations-graph', style={'height': '400px'}), 
    dcc.Graph(id='temperature-graph', style={'height': '400px'}), 
    
    html.Label('Objective Function:', style={'fontWeight': 'bold'}),
    dcc.Input(id='function-input', type='text', value='np.sin(np.sqrt(x**2 + y**2))', style={
        'width': '100%',  
        'padding': '12px 20px',  
        'margin': '8px 0',  
        'boxSizing': 'border-box',  
        'border': '2px solid #ccc',  
        'borderRadius': '4px',  
        'fontSize': '16px',  
        'backgroundColor': '#f8f8f8',  
        'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)'  
    }),
    
    html.Label('Number of Iterations:', style={'fontWeight': 'bold'}),
    dcc.Input(id='n-iterations-input', type='number', value=1000, style={
        'width': '100%',  
        'padding': '12px 20px',  
        'margin': '8px 0',  
        'boxSizing': 'border-box',  
        'border': '2px solid #ccc',  
        'borderRadius': '4px',  
        'fontSize': '16px',  
        'backgroundColor': '#f8f8f8',  
        'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)'  
    }),
    
    html.Label('Step Size:', style={'fontWeight': 'bold'}),
    dcc.Input(id='step-size-input', type='number', value=0.1, style={
        'width': '100%',  
        'padding': '12px 20px',  
        'margin': '8px 0',  
        'boxSizing': 'border-box',  
        'border': '2px solid #ccc',  
        'borderRadius': '4px',  
        'fontSize': '16px',  
        'backgroundColor': '#f8f8f8',  
        'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)'  
    }),
    
    html.Label('Initial Temperature:', style={'fontWeight': 'bold'}),
    dcc.Input(id='temp-input', type='number', value=10.0, style={
        'width': '100%',  
        'padding': '12px 20px',  
        'margin': '8px 0',  
        'boxSizing': 'border-box',  
        'border': '2px solid #ccc',  
        'borderRadius': '4px',  
        'fontSize': '16px',  
        'backgroundColor': '#f8f8f8',  
        'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)'  
    }),
    
    html.Button('Update Function', id='update-button', n_clicks=0, style={
        'backgroundColor': '#6348e8',  
        'color': 'white',  
        'padding': '15px 32px',  
        'textAlign': 'center',  
        'textDecoration': 'none',  
        'display': 'inline-block',  
        'fontSize': '16px',  
        'margin': '4px 2px',  
        'cursor': 'pointer',  
        'border': 'none',  
        'borderRadius': '12px'  
    }),
    
    html.Div(id='optima-info', style={
        'marginTop': '20px',
        'padding': '10px',  
        'border': '1px solid #ddd',  
        'borderRadius': '5px',  
        'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',  
        'backgroundColor': '#f9f9f9'  
    })
])