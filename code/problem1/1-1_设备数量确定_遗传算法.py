import numpy as np
import random
from itertools import combinations
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 定义点的坐标
coordinates = {
    'A': (110.241, 27.204, 824),
    'B': (110.780, 27.456, 727),
    'C': (110.712, 27.785, 742),
    'D': (110.251, 27.825, 850),
    'E': (110.524, 27.617, 786),
    'F': (110.467, 27.921, 678),
    'G': (110.047, 27.121, 575)
}

# 计算两点间的距离
def calculate_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

# 适应度函数
def fitness(chromosome):
    points = [coordinates[key] for key, val in zip(coordinates.keys(), chromosome) if val == 1]
    if len(points) < 2:
        return 0
    return sum(calculate_distance(p1, p2) for p1, p2 in combinations(points, 2))

# 选择函数
def select(population, fitnesses):
    total_fitness = sum(fitnesses)
    selection_probs = [f / total_fitness for f in fitnesses]
    return random.choices(population, weights=selection_probs, k=2)

# 交叉函数
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

# 变异函数
def mutate(chromosome, mutation_rate=0.05):
    return [gene if random.random() > mutation_rate else 1-gene for gene in chromosome]

# 遗传算法主体
def genetic_algorithm(coordinates, target_point_count=4, population_size=7, generations=100, mutation_rate=0.05):
    population = [[random.randint(0, 1) for _ in coordinates] for _ in range(population_size)]
    for _ in range(generations):
        fitnesses = [fitness(chromo) for chromo in population]
        new_population = []
        while len(new_population) < population_size:
            parents = select(population, fitnesses)
            for parent1, parent2 in zip(*[iter(parents)]*2):
                child1, child2 = crossover(parent1, parent2)
                child1, child2 = mutate(child1, mutation_rate), mutate(child2, mutation_rate)
                new_population.extend([child1, child2])
        population = new_population
    best_chromosome = max(population, key=fitness)
    return best_chromosome

# 执行算法，获取最佳染色体
best_solution = genetic_algorithm(coordinates)
selected_points = [key for key, val in zip(coordinates.keys(), best_solution) if val == 1]
print("Selected points:", selected_points)

# 可视化结果
fig = plt.figure()
