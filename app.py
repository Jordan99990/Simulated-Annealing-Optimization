import numpy as np
import plotly.graph_objects as go
from dash import Dash, no_update
from dash.dependencies import Input, Output, State
from tasks.genetic_algorithm import genetic_algorithm

from tasks.simulated_annealing import parse_function, simulated_annealing
from tasks.ui import layout
from tasks.genetic_algorithm import genetic_algorithm

app = Dash(__name__)
app.layout = layout

@app.callback(
    [Output('annealing-graph', 'figure'),
     Output('iterations-graph', 'figure'),
     Output('temperature-graph', 'figure'),
     Output('optima-info', 'children')],
    [Input('update-button', 'n_clicks')],
    [State('function-input', 'value'),
     State('n-iterations-input', 'value'),
     State('step-size-input', 'value'),
     State('temp-input', 'value')]
)
def update_graph(n_clicks, func_str, n_iterations, step_size, temp):
    objective_function = parse_function(func_str)
    
    bounds = np.array([[-5.0, 5.0], [-5.0, 5.0]])
    best, best_eval, scores, temperatures = simulated_annealing(objective_function, bounds, n_iterations, step_size, temp)
    
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    x, y = np.meshgrid(x, y)
    z = objective_function(x, y)

    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
    fig.add_trace(go.Scatter3d(x=[best[0]], y=[best[1]], z=[best_eval], mode='markers', marker=dict(size=5, color='red')))

    fig.update_layout(title={'text': 'Simulated Annealing Optimization', 'font': {'weight': 'bold'}}, autosize=True,
                      scene=dict(xaxis_title='X Axis',
                                 yaxis_title='Y Axis',
                                 zaxis_title='Z Axis'),
                      dragmode='orbit',
                      height=800)  

    iterations_fig = go.Figure(data=[go.Scatter(y=scores, mode='lines')])
    iterations_fig.update_layout(title={'text': 'Objective Function Value Over Iterations', 'font': {'weight': 'bold'}}, xaxis_title='Iteration', yaxis_title='Objective Function Value', height=400) 

    temperature_fig = go.Figure(data=[go.Scatter(y=temperatures, mode='lines')])
    temperature_fig.update_layout(title={'text': 'Temperature Over Iterations', 'font': {'weight': 'bold'}}, xaxis_title='Iteration', yaxis_title='Temperature', height=400) 

    optima_info = f"Optima: x = {best[0]:.2f}, y = {best[1]:.2f}, z = {best_eval:.2f}"
    
    return fig, iterations_fig, temperature_fig, optima_info

@app.callback(
    [Output('n-iterations-input', 'value'),
     Output('step-size-input', 'value'),
     Output('temp-input', 'value')],
    [Input('optimize-button', 'n_clicks')],
    [State('function-input', 'value')]
)

def optimize_hyperparameters(n_clicks, func_str):
    if n_clicks > 0:
        objective_function = parse_function(func_str)
        bounds = np.array([[500, 2000], [0.01, 0.1], [5.0, 20.0]])
        best, _ = genetic_algorithm(objective_function, bounds, n_iterations=100, population_size=50, mutation_rate=0.05)
        optimized_params = {
            'n_iterations': int(best[0]),
            'step_size': best[1],
            'temp': best[2]
        }
        return optimized_params['n_iterations'], optimized_params['step_size'], optimized_params['temp']
    return no_update, no_update, no_update

if __name__ == '__main__':
    app.run_server(debug=True)