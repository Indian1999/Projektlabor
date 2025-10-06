import random
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Cube:
    def __init__(self, size, x = 0, y = 0, z = 0):
        self.size = size
        self.x = x
        self.y = y
        self.z = z
        self.set_vertices()
        self.set_faces()

    def set_vertices(self):
        self.vertices = []
        deltas = [0, self.size]
        for i in deltas:
            for j in deltas:
                for k in deltas:
                    self.vertices.append((self.x + i, self.y + j, self.z + k))

    def set_faces(self):
        self.set_vertices()
        self.faces = [
        [self.vertices[j] for j in [0,1,3,2]],
        [self.vertices[j] for j in [4,5,7,6]],
        [self.vertices[j] for j in [0,1,5,4]],
        [self.vertices[j] for j in [2,3,7,6]],
        [self.vertices[j] for j in [0,2,6,4]],
        [self.vertices[j] for j in [1,3,7,5]]
    ]



class Space:
    def __init__(self, n):
        self.n = n
        self.cubes = [Cube(i) for i in range(n, 0, -1)] # n méretű az első, mert azt fixáljuk
        # A második legnagyobb kockát a legnagyobb szemközti sarkához rakjuk
        self.cubes[1].x += self.cubes[0].size
        self.cubes[1].y += self.cubes[0].size
        self.cubes[1].z += self.cubes[0].size
        self.randomize()
        self.fitness = 0

    def randomize(self):
        """Set a random position (integer) for all cubes smaller than n-1"""
        for cube in self.cubes[2:]:
            cube.x = random.randint(self.n - cube.size, self.cubes[0].size)
            cube.y = random.randint(self.n - cube.size, self.cubes[0].size)
            cube.z = random.randint(self.n - cube.size, self.cubes[0].size)

    def plot_space(self, path = "default.png", gen = 0):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        for cube in self.cubes:
            cube.set_faces()
            ax.add_collection3d(Poly3DCollection(cube.faces, facecolors="cyan", edgecolors="black", alpha=0.5))
        ax.set_xlim(0, self.n*2)
        ax.set_ylim(0, self.n*2)
        ax.set_zlim(0, self.n*2)
        ticks = [i for i in range(0, self.n*2 + 1, 2)]
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        ax.set_zticks(ticks)
        plt.title(f"Generation {gen}")
        plt.savefig(path)
        plt.close()


    def union_of_intervals(self, intervals: list[tuple[float]]) -> tuple[float]:
        intervals.sort(key=lambda x:x[0]) # Az intervallum kezdete szerint rendezünk
        union = [intervals[0]]
        for start, end in intervals[1:]:
            u_start, u_end = union[-1]
            if start <= u_end:
                union[-1] = (u_start, max(u_end, end))
            else:
                union.append((start, end))
        return union
    
    def interval_contains(self, value:list[tuple[float]], other: tuple[float]) -> bool:
        """checks if value contains the other"""
        o_start, o_end = other
        for start, end in value:
            if start <= o_start and end >= o_end:
                return True
            if start <= o_start and o_start <= end:
                o_start = end
            if o_start >= o_end:
                return True
        return False 

    def planes_part_of_cube(self, point: tuple[int])-> bool:
        """
            A point in the spaces defines 3 planes, 
                one where we lock the x coordinate and iterate the rest until they reach 0, 
                second where we lock the y coordinate and iterate the rest until 0,
                The third where we lock the z axis.
            This method finds out if all the points that are elements of these planes are part of at least one cube
        """
        x,y,z = point
        cubes_x = self.get_cubes_on_plane(x, "x")
        intervals_x_y = self.get_cube_intervals(cubes_x, "x", "y")
        intervals_x_z = self.get_cube_intervals(cubes_x, "x", "z")
        cubes_y = self.get_cubes_on_plane(y, "y")
        intervals_y_x = self.get_cube_intervals(cubes_y, "y", "x")
        intervals_y_z = self.get_cube_intervals(cubes_y, "y", "z")
        cubes_z = self.get_cubes_on_plane(z, "z")
        intervals_z_y = self.get_cube_intervals(cubes_z, "z", "y")
        intervals_z_x = self.get_cube_intervals(cubes_z, "z", "x")
        if self.interval_contains(intervals_x_y, (0, z)):
            if self.interval_contains(intervals_x_z, (0, y)):
                if self.interval_contains(intervals_y_x, (0, z)):
                    if self.interval_contains(intervals_y_z, (0, x)):
                        if self.interval_contains(intervals_z_x, (0, y)):
                            if self.interval_contains(intervals_z_y, (0, x)):
                                return True
        return False
            
    def get_cube_intervals(self, cubes:list[Cube], axis1="x", axis2="y") -> list[tuple[float]]:
        intervals = []
        if "z" not in axis1 + axis2:
            for cube in cubes:
                intervals.append((cube.z, cube.z + cube.size))
        if "y" not in axis1 + axis2:
            for cube in cubes:
                intervals.append((cube.y, cube.y + cube.size))
        if "x" not in axis1 + axis2:
            for cube in cubes:
                intervals.append((cube.x, cube.x + cube.size))
        return intervals
    
    def get_cubes_on_plane(self, value:float, axis:str = "x") -> list[Cube]:
        """
            Args: 
                value (float) - the coordinate of the plane
                axis (str) - on which axis does the axis lie
        """
        if axis == "x":
            cubes = []
            for cube in self.cubes:
                if cube.x <= value and cube.x + cube.size >= value:
                    cubes.append(cube)
        elif axis == "y":
            cubes = []
            for cube in self.cubes:
                if cube.y <= value and cube.y + cube.size >= value:
                    cubes.append(cube)
        elif axis == "z":
            cubes = []
            for cube in self.cubes:
                if cube.z <= value and cube.x + cube.size >= value:
                    cubes.append(cube)
        else:
            raise ValueError("Invalid axis value, the axis can only be 'x', 'y' or 'z'")
        return cubes

    def is_part_of_a_cube(self, point: tuple[int]) -> bool:
        x,y,z = point
        for cube in self.cubes:
            if x >= cube.x and x <= cube.x + cube.size and y >= cube.y and y <= cube.y + cube.size and z >= cube.z and z <= cube.z + cube.size:
                return True
        return False

class Genetic:
    def __init__(self, n:int, population_size:int = 50, generations:int = 10000, mutation_rate:float = 0.1, accuracy:int = 3):
        self.n = n
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = [Space(n) for i in range(self.population_size)] 
        self.accuracy = accuracy
        self.delta = 10 ** -self.accuracy

    def crossover(self, individual1: Space, individual2: Space):
        index = random.randint(2, self.n - 1)
        child = Space(self.n)
        child.cubes = individual1.cubes[:index] + individual2.cubes[index:]
        return child
    
    def mutation(self, individual):
        mutated_cubes = []
        for cube in individual.cubes[1:]:
            if random.random() < self.mutation_rate:
                cube.x += round(random.random()-0.5, self.accuracy)
                cube.x = max(0, cube.x)
                cube.x = min(self.n, cube.x)
            if random.random() < self.mutation_rate:
                cube.y += round(random.random()-0.5, self.accuracy)
                cube.y = max(0, cube.y)
                cube.y = min(self.n, cube.y)
            if random.random() < self.mutation_rate:
                cube.z += round(random.random()-0.5, self.accuracy)
                cube.z = max(0, cube.z)
                cube.z = min(self.n, cube.z)
            mutated_cubes.append(cube)
        mutated = Space(self.n)
        mutated.cubes = mutated_cubes
        return mutated
    
    def fitness(self, individual):
        value = individual.n    # n*n-es kockát biztos le tudunk fedni
        
        while individual.planes_part_of_cube((value + self.delta, value + self.delta, value + self.delta)):
            value = value + self.delta
        total = 0
        goal = value + self.delta
        bins = int(round(goal/self.delta))
        for x in np.linspace(0, goal, bins):
            for y in np.linspace(0, goal, bins):
                if individual.is_part_of_a_cube((x, y, goal)):
                    total += 1
        for x in np.linspace(0, goal, bins):
            for z in np.linspace(0, goal, bins):
                if individual.is_part_of_a_cube((x, goal, z)):
                    total += 1
        for y in np.linspace(0, goal, bins):
            for z in np.linspace(0, goal, bins):
                if individual.is_part_of_a_cube((goal, y, z)):
                    total += 1
        percentage = round(total / (3 * bins**2) * 100, 2)
        return value * 1000 + percentage # A lefedett kocka hatalmas bónusz, a bővítés lefedettsége kisebb

    def selection(self, k = 5):
        individuals = random.choices(self.population, k = k)
        return max(individuals, key=lambda x: x.fitness)
    
    def run(self):
        for generation in range(self.generations):
            best = self.population[0]
            best.fitness = self.fitness(best)
            for individual in self.population[1:]:
                individual.fitness = self.fitness(individual)
                if individual.fitness > best.fitness:
                    best = individual
            print(f"Generation {generation}: The score of the best individual: {best.fitness}")
            if generation % 10 == 0:
                best.plot_space(f"plots/{generation}_gen_best.png", generation)

            new_population = [best]
            while len(new_population) != self.population_size:
                child = self.crossover(self.selection(), self.selection())
                child = self.mutation(child)
                new_population.append(child)
            self.population = new_population

genetic = Genetic(n=12, population_size=50,  generations=2000, mutation_rate=0.1, accuracy=1)
genetic.run()

def volume_sum(n:int) -> int:
    """
        Returns the sum of the volumes of n cubes, each cube has a sidelength of 1, 2, 3, ... n
        Args: n (int) - The number of cubes
    """
    total = 0
    for i in range(1, n+1):
        total += i**3
    return total

def volumes_slided_big_cubes(n:int, overlap:float) -> tuple[float]:
    """
        Checks the volume requirements for a double cube composition of a cube with n sidelengths and another with (n-1) sidelengths where the 2 cubes are 'touched' together at a corner with a possible cube shaped overlap.
        Args:
            n (int) - the side of the bigger cube
            overlap (float) - how much of an overlap do the 2 cubes have (it is a sidelength, the overlap each other in a cube shape which's sidelang is the value of the overlap)
        Returns:
            A 3 element tuple containing:
                The volume taken up by the 2 big cubes
                The volume needed to fill tha space 'between' the 2 cubes (so it makes a cube again)
                The total volume of the ramining cubes (n-2, n-3, n-4, ..., 1 sidelengths)
    """
    occupied_volume = n**3 + (n-1)**3 - overlap**3
    new_big_cube_volume = (n + n - 1 - overlap)**3
    missing_volume = new_big_cube_volume - occupied_volume
    remaining_total = volume_sum(n-2)
    return (occupied_volume, missing_volume, remaining_total)
