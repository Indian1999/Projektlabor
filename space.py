import numpy as np
from cube import Cube
import random
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Space:
    optimal_reaches = {}

    def __init__(self, n:int, accuracy = 1, reach = None, do_setup = True):
        if n < 8:
            raise ValueError("There has to be at least 8 cubes!")
        self.n = n
        self.accuracy = accuracy
        self.delta = 10**-accuracy
        self.cubes = [Cube(i) for i in range(n, 0, -1)] # n méretű az első, mert azt fixáljuk
        # A második legnagyobb kockát a legnagyobb szemközti sarkához rakjuk
        if do_setup and reach != None:
            self.setup(reach=reach)
        elif do_setup:
            self.setup_with_optimal_reach()
        self.fitness = 0
        self.result = None

    def setup_with_optimal_reach(self):
        if self.n in Space.optimal_reaches.keys():
            self.reach = Space.optimal_reaches[self.n]
            self.setup(reach=self.reach)
            return
        reach_value = self.n
        reach_to_test = self.n*2-1
        while reach_value == self.n:
            print(reach_to_test)
            self.reach = reach_to_test
            self.setup(reach=reach_to_test)
            value = self.n*2 -1
            while 1.0 != self.monte_carlo_filled_ratio(value, mode = "strict", sample_size = 5000):
                value -= self.delta
                value = round(value,self.accuracy)
            reach_value = round(value, self.accuracy)
            reach_to_test -= self.delta
            reach_to_test = round(reach_to_test, self.accuracy)
            
        # Itt szándékosan csinálom újra, különben nagyon a határon táncolunk és nem lesz jó a végkimenetel (a monte carlo miatt lehetnek apró lyukak a nagy kockában)
        self.reach = reach_to_test
        self.setup(self.reach)
        Space.optimal_reaches[self.n] = self.reach
         

    @classmethod
    def from_json(cls, json, accuracy = 1):
        n = len(json["cubes"])
        space = cls(n, accuracy = accuracy, do_setup = False)
        space.cubes = [Cube(c["size"], c["x"], c["y"], c["z"]) for c in json["cubes"]]
        return space

    def setup(self, reach = 1):
        # A cruical points sorrendje egy egyenlet alapján lett meghatározva, AI által lett megkeresve az optimális sorrend, bővebb infoért: resources/egyenlet_megoldás.txt
        cruical_points = ["buffer", (1,1,1), (0,1,0), (1,0,0), (0,0,1), (1,1,0), (1,0,1), (0,1,1), (0, 1, 0.5), (0, 0.5, 1), (0.5, 0, 1), (1, 0, 0.5), (1, 0.5, 0), (0.5, 1, 0)] # 13 crucial points in total
        for i in range(1, min(len(cruical_points), self.n)):
            cube = self.cubes[i]
            offset = self.n - cube.size + reach
            position = (cruical_points[i][0]*offset, cruical_points[i][1]*offset, cruical_points[i][2]*offset)
            cube.set_position(*position)
        
        for i in range(len(cruical_points), self.n):
            cube = self.cubes[i]
            random_path = random.randint(1,4)
            if random_path == 1:
                cube.x = 0
                cube.y = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
                cube.z = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
            elif random_path == 2:
                cube.x = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
                cube.y = 0
                cube.z = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
            elif random_path == 3:
                cube.x = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
                cube.y = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
                cube.z = 0

    def randomize(self):
        """Set a random position (integer) for all cubes smaller than n-1"""
        for cube in self.cubes[2:]:
            random_path = random.randint(1,4)
            if random_path == 1:
                cube.x = 0
                cube.y = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
                cube.z = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
            elif random_path == 2:
                cube.x = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
                cube.y = 0
                cube.z = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
            elif random_path == 3:
                cube.x = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
                cube.y = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
                cube.z = 0
            else:
                cube.x = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
                cube.y = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
                cube.z = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy

    def plot_space(self, path = "default.png", title = None):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        for cube in self.cubes[1:]:
            cube.set_faces()
            ax.add_collection3d(Poly3DCollection(cube.faces, facecolors="cyan", edgecolors="black", alpha=0.5))
        cube = self.cubes[0]
        cube.set_faces()
        ax.add_collection3d(Poly3DCollection(cube.faces, facecolors="red", edgecolors="black", alpha=0.7))
        ax.set_xlim(0, self.n*2)
        ax.set_ylim(0, self.n*2)
        ax.set_zlim(0, self.n*2)
        ticks = [i for i in range(0, self.n*2 + 1, 2)]
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        ax.set_zticks(ticks)
        if title:
            plt.title(title)
        plt.savefig(path)
        plt.close()

    def to_json(self):
        root = {}
        if self.result == None:
            self.evaluate()
        root["result"] = self.result
        root["cubes"] = []
        for cube in self.cubes:
            cubeDict = {}
            cubeDict["size"] = cube.size
            cubeDict["x"] = cube.x
            cubeDict["y"] = cube.y
            cubeDict["z"] = cube.z
            root["cubes"].append(cubeDict)
        return root

    def print_space(self, path = "default.json", gen = 0):
        payload = self.to_json()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4, ensure_ascii=True)

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
    
    def is_cube_within_base_cube(self, cube: Cube) -> bool:
        if cube.x >= 0 and cube.x + cube.size <= self.n:
            if cube.y >= 0 and cube.y + cube.size <= self.n:
                if cube.z >= 0 and cube.z + cube.size <= self.n:
                    return True
        return False

    def has_two_cubes_on_all_zeros(self):
        """
        Determines wheter the space has at least one non-base cube on each of the 0 coordinates
        """
        x_0, y_0, z_0 = 0, 0, 0
        for cube in self.cubes[1:]:
            if cube.x == 0:
                x_0 += 1
            if cube.y == 0:
                y_0 += 1
            if cube.z == 0:
                z_0 += 1
            if x_0 >= 2 and y_0 >= 2 and z_0 >= 2:
                return True
        return False

    def monte_carlo_filled_ratio(self, goal_size, sample_size = 2000, mode: None | str = None):
        counter = 0
        goal_size = round(goal_size, self.accuracy)
        random_path = random.randint(1, 3)
        points = np.zeros((sample_size*3, 3))
        restricted = np.random.uniform(self.n, np.nextafter(goal_size, float("inf")), sample_size)
        whole1 = np.random.uniform(0, np.nextafter(goal_size, float("inf")), sample_size)
        whole2 = np.random.uniform(0, np.nextafter(goal_size, float("inf")), sample_size)
        points[:sample_size, 0] = restricted
        points[:sample_size, 1] = whole1
        points[:sample_size, 2] = whole2
        points[sample_size:2*sample_size, 0] = whole1
        points[sample_size:2*sample_size, 1] = restricted
        points[sample_size:2*sample_size, 2] = whole2
        points[2*sample_size:, 0] = whole1
        points[2*sample_size:, 1] = whole2
        points[2*sample_size:, 2] = restricted
        points = np.round(points, self.accuracy)
        for point in points:
            if self.is_part_of_a_cube(point):
                counter += 1
            elif mode == "strict":
                if goal_size < 16.1:
                    print(self.cubes[0].x,self.cubes[0].y,self.cubes[0].z)
                    print(point, goal_size)
                return 0
        return counter / (sample_size * 3)

    def check_grid_coverage(self, goal_size):
        """
        Megnézi, hogy a goal_size méretű kocka le van-e fedve. Síralmasan lassú :'(
        """
        for i in np.arange(goal_size, -self.delta/2, -self.delta):
            for j in np.arange(goal_size, -self.delta/2, -self.delta):
                for k in np.arange(goal_size, self.n-self.delta, -self.delta):
                    x, y, z = round(i, self.accuracy), round(j, self.accuracy), round(k, self.accuracy)
                    if not self.is_part_of_a_cube((x,y,z)):
                        return False
        for i in np.arange(goal_size, -self.delta/2, -self.delta):
            for j in np.arange(goal_size, -self.delta/2, -self.delta):
                for k in np.arange(goal_size, self.n-self.delta, -self.delta):
                    x, y, z = round(i, self.accuracy), round(j, self.accuracy), round(k, self.accuracy)
                    if not self.is_part_of_a_cube((x,z,y)):
                        return False
        for i in np.arange(goal_size, -self.delta/2, -self.delta):
            for j in np.arange(goal_size, -self.delta/2, -self.delta):
                for k in np.arange(goal_size, self.n-self.delta, -self.delta):
                    x, y, z = round(i, self.accuracy), round(j, self.accuracy), round(k, self.accuracy)
                    if not self.is_part_of_a_cube((k,x,y)):
                        return False
        return True
    
    def evaluate(self):
        value = self.n * 2
        while not self.check_grid_coverage(value):
            value -= self.delta
            value = round(value, self.accuracy)
        self.result = value
        return value