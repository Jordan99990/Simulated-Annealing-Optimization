import numpy as np

def parse_function(func_str):
    def objective_function(x, y):
        return eval(func_str)
    return objective_function

def simulated_annealing(objective, bounds, n_iterations, step_size, temp):
    best = bounds[:, 0] + (bounds[:, 1] - bounds[:, 0]) * np.random.rand(len(bounds))
    best_eval = objective(best[0], best[1])
    curr, curr_eval = best, best_eval
    scores = [best_eval]
    temperatures = [temp]
    for i in range(n_iterations):
        candidate = curr + np.random.randn(len(bounds)) * step_size
        candidate_eval = objective(candidate[0], candidate[1])
        if candidate_eval < best_eval:
            best, best_eval = candidate, candidate_eval
            scores.append(best_eval)
        diff = candidate_eval - curr_eval
        t = temp / float(i + 1)
        temperatures.append(t)
        metropolis = np.exp(-diff / t)
        if diff < 0 or np.random.rand() < metropolis:
            curr, curr_eval = candidate, candidate_eval
    return best, best_eval, scores, temperatures