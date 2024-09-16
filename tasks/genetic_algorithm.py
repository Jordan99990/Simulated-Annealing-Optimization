import numpy as np

def genetic_algorithm(objective_function, bounds, n_iterations, population_size, mutation_rate):
    def create_population(size, bounds):
        return np.random.uniform(bounds[:, 0], bounds[:, 1], (size, bounds.shape[0]))

    def select_parents(population, scores, k=3):
        selected = np.random.choice(np.arange(len(population)), size=k, replace=False)
        selected = sorted(selected, key=lambda idx: scores[idx])
        return population[selected[0]], population[selected[1]]

    def crossover(parent1, parent2):
        crossover_point = np.random.randint(1, len(parent1)-1)
        child1 = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
        child2 = np.concatenate([parent2[:crossover_point], parent1[crossover_point:]])
        return child1, child2

    def mutate(child, bounds, mutation_rate):
        for i in range(len(child)):
            if np.random.rand() < mutation_rate:
                child[i] = np.random.uniform(bounds[i, 0], bounds[i, 1])
        return child

    def elitism(population, scores, elite_size):
        elite_indices = np.argsort(scores)[:elite_size]
        return population[elite_indices]

    population = create_population(population_size, bounds)
    best, best_eval = None, float('inf')
    elite_size = max(1, population_size // 10) 

    for _ in range(n_iterations):
        scores = np.array([objective_function(ind[0], ind[1]) for ind in population])
        
        for i in range(len(population)):
            if scores[i] < best_eval:
                best, best_eval = population[i], scores[i]

        elite = elitism(population, scores, elite_size)
        selected = [select_parents(population, scores) for _ in range((population_size - elite_size) // 2)]
        children = []
        for parent1, parent2 in selected:
            for child in crossover(parent1, parent2):
                children.append(mutate(child, bounds, mutation_rate))

        population = np.vstack((elite, np.array(children)[:population_size - elite_size]))
        mutation_rate *= 0.99  

    return best, best_eval