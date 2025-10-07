import random
import time
from space import Space
import os
from copy import deepcopy

class Genetic:
    def __init__(self, n:int, population_size:int = 50, 
                 generations:int = 10000, mutation_rate:float = 0.1, 
                 accuracy:int = 3, reach = 1):
        self.n = n
        self.reach = reach
        self.accuracy = accuracy
        self.delta = 10 ** -self.accuracy
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = [Space(n, self.accuracy, self.reach) for i in range(self.population_size)] 

    def get_params_string(self):
        return f"{time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())}_{self.n}_{self.population_size}_{self.generations}_{self.mutation_rate}_{self.accuracy}_{self.reach}"
   
    def crossover(self, individual1: Space, individual2: Space):
        index = random.randint(2, self.n - 1)
        child = Space(self.n, self.accuracy)
        child.cubes = individual1.cubes[:index] + individual2.cubes[index:]
        return child
    
    def mutation(self, individual):
        mutated_cubes = [individual.cubes[0]]
        for cube in individual.cubes[1:]:
            if random.random() < self.mutation_rate:
                cube.x += round(random.random()-0.5, self.accuracy)
                cube.x = max(0, cube.x) 
                cube.x = min(self.n, cube.x) #Semmi értelme ha nem ér hozzá a base kockához
            if random.random() < self.mutation_rate:
                cube.y += round(random.random()-0.5, self.accuracy)
                cube.y = max(0, cube.y)
                cube.y = min(self.n, cube.y)
            if random.random() < self.mutation_rate:
                cube.z += round(random.random()-0.5, self.accuracy)
                cube.z = max(0, cube.z)
                cube.z = min(self.n, cube.z)
            cube.x = round(cube.x, self.accuracy) # Ha ez nincs, akkor a floatok nem megfelelő értéken lesznek
            cube.y = round(cube.y, self.accuracy)
            cube.z = round(cube.z, self.accuracy)
            mutated_cubes.append(cube)
        mutated = Space(self.n, self.accuracy)
        mutated.cubes = mutated_cubes
        return mutated
    
    def fitness(self, individual, mode = 1):
        """
        Args:
            individual (Space): duh..
            mode (int): 
                1 - monte carlo becslés (Pontatlan)
                2 - full grid coverage (Számításigényes)
        """
        for cube in individual.cubes[1:]:
            if individual.is_cube_within_base_cube(cube):
                return -1 # Ha legalább egy kocka értelmetlen, büntetünk
            if not individual.has_two_cubes_on_all_zeros():
                return -1 # Ha nincsen minden 0-s koordináta lefedve, büntetünk
        if mode == 1:
            value = self.n*2 -1
            while 1.0 != individual.monte_carlo_filled_ratio(value, mode = "strict", sample_size = 5000):
                value -= self.delta
            return value + individual.monte_carlo_filled_ratio(value + self.delta)
        elif mode == 2:
            value = 2*individual.n - 1   # ezt tuti nem fedjük le    
            while not individual.check_grid_coverage(value + self.delta):
                value = value - self.delta
            return value
        else:
            raise ValueError("Invalid mode, valid modes: 1, 2")
    
    def selection(self, k = 5):
        individuals = random.choices(self.population, k = k)
        return max(individuals, key=lambda x: x.fitness)
    
    def run(self):
        for generation in range(self.generations):
            self.best = self.population[0]
            self.best.fitness = self.fitness(self.best)
            for individual in self.population[1:]:
                individual.fitness = self.fitness(individual)
                if individual.fitness > self.best.fitness:
                    self.best = individual
            print(f"Generation {generation}: The score of the best individual: {self.best.fitness}")
            #if generation % 10 == 0:
            #    self.best.plot_space(f"plots/{generation}_gen_best.png", generation)
            #    self.best.print_space(f"spaces/{generation}_gen_best.json", generation)

            new_population = [deepcopy(self.best)]
            while len(new_population) != self.population_size:
                child = self.crossover(self.selection(), self.selection())
                child = self.mutation(child)
                new_population.append(child)
            self.population = new_population

        # Ha a monte carlo szerint haszontalan, nem vesződünk a pontos ellenőrzésével
        # Legalább 95%-ban legyen olyan jó mint a legjobb
        indeces = [i for i in range(self.population_size) if self.population[i].fitness > self.best.fitness * 0.95]
        self.export_results(indeces)

    def export_results(self, indeces:list[int] = None):
        path = os.path.dirname(__file__)
        os.makedirs(os.path.join(path, "results"), exist_ok=True)
        path = os.path.join(path, "results")
        dirname = self.get_params_string()
        os.makedirs(os.path.join(path, dirname), exist_ok=True)
        path = os.path.join(path, dirname)
        os.makedirs(os.path.join(path, "plots"), exist_ok=True)
        os.makedirs(os.path.join(path, "spaces"), exist_ok=True)
        if indeces == None:
            indeces = range(self.population_size)
        for i in indeces:
            appendix = ""
            if self.population[i] == self.best:
                appendix = "_best"
            self.population[i].plot_space(os.path.join(path, "plots", f"space_{i+1}{appendix}.png"), f"Solution {i+1}")
            self.population[i].print_space(os.path.join(path, "spaces", f"space_{i+1}{appendix}.json"), f"Solution {i+1}")

genetic = Genetic(n=13, population_size=10,  generations=20,
                   mutation_rate=0.1, accuracy=1, reach=2.1)
genetic.run()


