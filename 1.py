import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import random

def objective_function(x, y):
    return np.sin(np.sqrt(x**2 + y**2))

def simulated_annealing(objective, bounds, n_iterations, step_size, temp):
    best = bounds[:, 0] + (bounds[:, 1] - bounds[:, 0]) * np.random.rand(len(bounds))
    best_eval = objective(best[0], best[1])
    curr, curr_eval = best, best_eval
    scores = [best_eval]
    for i in range(n_iterations):
        candidate = curr + np.random.randn(len(bounds)) * step_size
        candidate_eval = objective(candidate[0], candidate[1])
        if candidate_eval < best_eval:
            best, best_eval = candidate, candidate_eval
            scores.append(best_eval)
        diff = candidate_eval - curr_eval
        t = temp / float(i + 1)
        metropolis = np.exp(-diff / t)
        if diff < 0 or np.random.rand() < metropolis:
            curr, curr_eval = candidate, candidate_eval
    return best, best_eval, scores

bounds = np.array([[-5.0, 5.0], [-5.0, 5.0]])
n_iterations = 1000
step_size = 0.1
temp = 10.0
best, best_eval, scores = simulated_annealing(objective_function, bounds, n_iterations, step_size, temp)

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='annealing-graph', style={'height': '80vh'}),
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0),
    html.Div(id='optima-info', style={'marginTop': 20})
])

@app.callback(
    [Output('annealing-graph', 'figure'),
     Output('optima-info', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    x, y = np.meshgrid(x, y)
    z = objective_function(x, y)
    
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
    fig.add_trace(go.Scatter3d(x=[best[0]], y=[best[1]], z=[best_eval], mode='markers', marker=dict(size=5, color='red')))
    
    fig.update_layout(title='Simulated Annealing Optimization', autosize=True,
                      scene=dict(xaxis_title='X Axis',
                                 yaxis_title='Y Axis',
                                 zaxis_title='Z Axis'),
                      dragmode='orbit') 
    
    optima_info = f"Optima: x = {best[0]:.2f}, y = {best[1]:.2f}, z = {best_eval:.2f}"
    
    return fig, optima_info

if __name__ == '__main__':
    app.run_server(debug=True)