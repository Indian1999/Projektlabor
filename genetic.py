import random
import time
from space import Space
import os
import threading
from copy import deepcopy
from cubesolver import CubeSolver

class Genetic(CubeSolver):
    def __init__(self, n:int, population_size:int = 50, 
                 generations:int = None, mutation_rate:float = 0.1, 
                 accuracy:int = 0, reach = None, fitness_mode: int = 1):
        self.n = n
        self.reach = reach
        self.accuracy = accuracy
        self.pause_event = threading.Event()
        self.pause_event.clear()
        self.delta = 10 ** -self.accuracy
        self.population_size = population_size     
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = [Space(n, self.accuracy, self.reach) for i in range(self.population_size)] 
        self.running = False
        self.fitness_mode = fitness_mode
        self.results = []

    def pause(self):
        self.pause_event.clear()

    def resume(self):
        self.pause_event.set()

    def to_json(self):
        return {
            "n": self.n,
            "population_size": self.population_size,
            "generations": self.generations,
            "mutation_rate": self.mutation_rate,
            "accuracy": self.accuracy,
            "reach": self.reach,
            "fitness_mode": self.fitness_mode
        }

    def get_params_string(self):
        """
        Returns a string that contains the parameters of the genetic algorithm.
        The string is in the format of: <date>_<n>_<population_size>_<generations>_<mutation_rate>_<accuracy>_<reach>
        This string is used to name the folder where the results of the genetic algorithm are stored.
        """
        return f"{time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())}_{self.n}_{self.population_size}_{self.generations}_{self.mutation_rate}_{self.accuracy}_{self.reach}"
   
    def crossover(self, individual1: Space, individual2: Space):
        index = random.randint(2, self.n - 1)
        child = Space(self.n, self.accuracy, do_setup = False)
        child.cubes = individual1.cubes[:index] + individual2.cubes[index:]
        return child
    
    def mutation(self, individual):
        mutated_cubes = [individual.cubes[0]]
        for cube in individual.cubes[1:]:
            if random.random() < self.mutation_rate:
                if self.accuracy != 0:
                    # Ha 0 az accuracy akkor ez nem csinál semmit
                    cube.x += round(random.random()-0.5, self.accuracy)
                else:
                    cube.x += random.randint(-1,1)
                cube.x = max(0, cube.x) 
                cube.x = min(self.n, cube.x) #Semmi értelme ha nem ér hozzá a base kockához
            if random.random() < self.mutation_rate:
                if self.accuracy != 0:
                    # Ha 0 az accuracy akkor ez nem csinál semmit
                    cube.y += round(random.random()-0.5, self.accuracy)
                else:
                    cube.y += random.randint(-1,1)
                cube.y = max(0, cube.y)
                cube.y = min(self.n, cube.y)
            if random.random() < self.mutation_rate:
                if self.accuracy != 0:
                    # Ha 0 az accuracy akkor ez nem csinál semmit
                    cube.z += round(random.random()-0.5, self.accuracy)
                else:
                    cube.z += random.randint(-1,1)
                cube.z = max(0, cube.z)
                cube.z = min(self.n, cube.z)
            cube.x = round(cube.x, self.accuracy) # Ha ez nincs, akkor a floatok nem megfelelő értéken lesznek
            cube.y = round(cube.y, self.accuracy)
            cube.z = round(cube.z, self.accuracy)
            mutated_cubes.append(cube)
        mutated = Space(self.n, self.accuracy, do_setup=False)
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
            while not individual.check_grid_coverage(value):
                value = value - self.delta
            value += individual.next_size_filled_ratio(value, value + self.delta)
            return value
        else:
            raise ValueError("Invalid mode, valid modes: 1, 2")
    
    def selection(self, k = 5):
        individuals = random.choices(self.population, k = k)
        return max(individuals, key=lambda x: x.fitness)
    
    def stop(self):
        self.running = False

    def run(self, fitness_mode = None, plot_space = False):
        if fitness_mode != None:
            print("genetic.run(): fitness_mode is a deprecated parameter, the fitness mode is automaticly set to self.fitness_mode")
        fitness_mode = self.fitness_mode
        for space in self.population:
            space.setup(reach=self.reach)
            # Eddig a space létrehozásánál csináltuk ezt, de kifagyasztja a gunicornt ha a kunstruktorban van.
        generation = 1
        self.running = True
        while self.running:
            self.pause_event.wait()
            self.best = self.population[0]
            self.best.fitness = self.fitness(self.best, mode = fitness_mode)
            for individual in self.population[1:]:
                individual.fitness = self.fitness(individual, mode = fitness_mode)
                if individual.fitness > self.best.fitness:
                    self.best = individual
            yield f"Generation {generation}: The score of the best individual: {self.best.fitness}"
            #if generation % 5 == 0:
            #    os.makedirs("plots", exist_ok=True)
            #    os.makedirs("spaces", exist_ok=True)
            #    self.best.plot_space(f"plots/{generation}_gen_best.png", generation)
            #    self.best.print_space(f"spaces/{generation}_gen_best.json", generation)

            new_population = [deepcopy(self.best)]
            while len(new_population) != self.population_size:
                child = self.crossover(self.selection(), self.selection())
                child = self.mutation(child)
                new_population.append(child)
            self.population = new_population
            if generation == self.generations:
                self.running = False
                break
            generation += 1

        yield "Exporting results..."
        indeces = [i for i in range(self.population_size) if self.population[i].fitness > self.best.fitness * 0.95]
        self.export_results(indeces, plot_space)
        yield "Done!"

    def export_results(self, indeces:list[int] = None, plot_space = False):
        path = os.path.dirname(__file__)
        os.makedirs(os.path.join(path, "results"), exist_ok=True)
        path = os.path.join(path, "results")
        dirname = self.get_params_string()
        os.makedirs(os.path.join(path, dirname), exist_ok=True)
        path = os.path.join(path, dirname)
        if plot_space:
            os.makedirs(os.path.join(path, "plots"), exist_ok=True)
        os.makedirs(os.path.join(path, "spaces"), exist_ok=True)
        if indeces == None:
            indeces = range(self.population_size)
        for i in indeces:
            appendix = ""
            if self.population[i] == self.best:
                appendix = "_best"
            #if plot_space:
            #    self.population[i].plot_space(os.path.join(path, "plots", f"space_{i+1}{appendix}.png"), f"Solution {i+1}")
            self.population[i].print_space(os.path.join(path, "spaces", f"space_{i+1}{appendix}.json"), f"Solution {i+1}")
            self.results.append(self.population[i].to_json())

