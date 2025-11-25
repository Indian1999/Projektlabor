import numpy as np
from cube import Cube
import random
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Space:
    optimal_reaches = {}

    def __init__(self, n:int, accuracy = 0, reach = None, do_setup = True):
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
        """
        Sets up the space with the optimal reach value. If the optimal reach value is not known, it will be calculated.
        The optimal reach value is the minimal reach value that still results in a filled space when the space is constructed with the given number of cubes.
        The optimal reach value is stored in the Space.optimal_reaches dictionary for later use.
        """
        if self.n in Space.optimal_reaches.keys():
            self.reach = Space.optimal_reaches[self.n]
            self.setup(reach=self.reach)
            return
        reach_value = self.n
        reach_to_test = self.n*2-1
        while reach_value == self.n:
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
                if cube.size == 1 and self.accuracy == 0:
                    # 0-s accuracy esetén az 1-es kockánál a randint low>= high hibát dob
                    cube.set_position(0, self.n, self.n)
                else:
                    cube.x = 0
                    cube.y = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
                    cube.z = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
            elif random_path == 2:
                if cube.size == 1 and self.accuracy == 0:
                    # 0-s accuracy esetén az 1-es kockánál a randint low>= high hibát dob
                    cube.set_position(0, self.n, self.n)
                else:
                    cube.x = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
                    cube.y = 0
                    cube.z = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
            elif random_path == 3:
                if cube.size == 1 and self.accuracy == 0:
                    # 0-s accuracy esetén az 1-es kockánál a randint low>= high hibát dob
                    cube.set_position(0, self.n, self.n)
                else:
                    cube.x = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
                    cube.y = np.random.randint((self.n - cube.size + self.delta) * 10**self.accuracy, self.cubes[0].size * 10**self.accuracy) / 10**self.accuracy
                    cube.z = 0

    def randomize(self):
        """
        Randomizes the position of all cubes except the first two.
        The randomization is done in a way that the first two cubes are not
        influenced. The position of each cube is chosen randomly from the
        possible positions, where the size of the cube is taken into account.
        """
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
        """
        Plots the space in a 3D plot

        Args:
            path (str): The path to save the plot. Defaults to "default.png".
            title (str): The title of the plot. Defaults to None
        """
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
        """
        Converts the space to a JSON format.

        Returns:
            dict: A dictionary containing the result and the cubes in the space in JSON format.
        """
        root = {}
        if self.result == None:
            self.evaluate()
        root["result"] = self.result
        root["n"] = self.n
        root["accuracy"] = self.accuracy
        root["cubes"] = []
        for cube in self.cubes:
            cubeDict = {}
            cubeDict["size"] = cube.size
            cubeDict["x"] = cube.x
            cubeDict["y"] = cube.y
            cubeDict["z"] = cube.z
            center = cube.get_center()
            cubeDict["x_center"] = center[0]
            cubeDict["y_center"] = center[1]
            cubeDict["z_center"] = center[2]
            root["cubes"].append(cubeDict)
        return root

    def print_space(self, path = "default.json", gen = None):
        """
        Prints the space to a JSON file.

        Args:
            path (str): The path to the JSON file to write to. Defaults to "default.json".
        """
        payload = self.to_json()

        # NumPy int típusától kicrashel a json dump, ezért kell
        def convert(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj

        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4, ensure_ascii=True, default=convert)

    def union_of_intervals(self, intervals: list[tuple[float]]) -> tuple[float]:
        """
        Returns the union of the given intervals. The intervals are sorted by their start points, and then the union is calculated by merging the overlapping intervals.
        Args:
            intervals (list[tuple[float]]): A list of intervals to calculate the union of.

        Returns:
            tuple[float]: The union of the given intervals as a tuple of (start, end) pairs.
        """
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
        """
        Checks whether a given interval is fullycontained in the union of the intervals in a given list

        Args:
            value (list[tuple[float]]): A list of intervals to check against
            other (tuple[float]): The interval to check for containment

        Returns:
            bool: True if the given interval is fully contained in the union of the intervals in the list, False otherwise
        """
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
        Checks whether 3 seperate planes derived from a given point have all the points within at least one of the cubes in the space
        
        An example of how the planes are created:
            point = (2, 3, 4)
            plane1 = (x=2, y=[0, 3], z=[0, 4])
            plane2 = (x=[0, 2], y=3, z=[0, 4])
            plane3 = (x=[0, 2], y=[0, 3], z=4)

        Returns True if all 3 planes have at least one point in the space
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
        """
        Returns a list of intervals where each interval represents the range of the NOT given axis that the cubes occupy.

        Args:
            cubes (list[Cube]): A list of Cube objects
            axis1 (str): The first axis to exclude. Defaults to "x".
            axis2 (str): The second axis to exclude. Defaults to "y".
        Returns:
            list[tuple[float]]: A list of tuples where each tuple contains the start and end of an interval (inclusive).
        """
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
        Returns all the cubes that have a point on the plane with the given value in the given axis.

        Args:
            value (float): The value of the plane in the given axis.
            axis (str): The axis of the plane. Can be 'x', 'y' or 'z'.

        Returns:
            list[Cube]: A list of all the cubes that have a point on the plane.

        Raises:
            ValueError: If the axis is not 'x', 'y' or 'z'.
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
        """
        Checks whether a given point is part of any cube in the space.

        Args:
            point (tuple[int]): The coordinates of the point to check.

        Returns:
            bool: True if the point is part of at least one cube, False otherwise.
        """
        x,y,z = point
        for cube in self.cubes:
            if x >= cube.x and x <= cube.x + cube.size and y >= cube.y and y <= cube.y + cube.size and z >= cube.z and z <= cube.z + cube.size:
                return True
        return False
    
    def is_cube_within_base_cube(self, cube: Cube) -> bool:
        """
        Checks whether a cube is completely within the base (largest) cube of the space.

        Args:
            cube (Cube): The cube to check.

        Returns:
            bool: True if the cube is within the base cube, False otherwise.
        """
        if cube.x >= 0 and cube.x + cube.size <= self.n:
            if cube.y >= 0 and cube.y + cube.size <= self.n:
                if cube.z >= 0 and cube.z + cube.size <= self.n:
                    return True
        return False

    def has_two_cubes_on_all_zeros(self):
        """
        Checks whether there are at least two cubes on each of the three axes (x,y,z) with value 0.

        Returns:
            bool: True if there are at least two cubes on each of the three axes with value 0, False otherwise.
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
        """
        Estimates the ratio of the points that are part of a cube in the given range

        Parameters:
            goal_size (float): the size of the cube that we want to fill
            sample_size (int): the number of points to generate randomly
            mode (None | str): if "strict", the function returns 0 if any of the checked points are not part of a cube

        Returns:
            float: the estimated ratio of the points that are part of a cube in the given range
        """
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
                return 0
        return counter / (sample_size * 3)

    def check_grid_coverage(self, goal_size):
        """
        Checks whether the space has a full grid coverage of the given size, by checking all the possible points.

        Parameters:
            goal_size (float): the size of the grid to check

        Returns:
            bool: True if the space has a full grid coverage of the given size, False otherwise
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
                    if not self.is_part_of_a_cube((z,x,y)):
                        return False
        return True
    
    def next_size_filled_ratio(self, current_size, goal_size):
        """
        This function calculates the ratio of the points that are part of a cube
        in the given range. It checks all possible points in the range and counts
        how many of them are part of a cube. The result is then divided by the
        maximum possible number of points in the given range.

        Parameters:
            current_size (float): the size of the cube that is already filled
            goal_size (float): the size of the cube that we want to fill

        Returns:
            float: the ratio of the points that are part of a cube in the given range
        """
        total = 0
        points_to_check = []
        for i in np.arange(current_size+self.delta, goal_size + self.delta, self.delta):
            for j in np.arange(0, goal_size + self.delta, self.delta):
                for k in np.arange(0, goal_size + self.delta, self.delta):
                    x, y, z = round(i, self.accuracy), round(j, self.accuracy), round(k, self.accuracy)
                    if (x,y,z) not in points_to_check:
                        points_to_check.append((x,y,z))
        for i in np.arange(current_size+self.delta, goal_size + self.delta, self.delta):
            for j in np.arange(0, goal_size + self.delta, self.delta):
                for k in np.arange(0, goal_size + self.delta, self.delta):
                    x, y, z = round(i, self.accuracy), round(j, self.accuracy), round(k, self.accuracy)
                    if (y,x,z) not in points_to_check:
                        points_to_check.append((y,x,z))
        for i in np.arange(current_size+self.delta, goal_size + self.delta, self.delta):
            for j in np.arange(0, goal_size + self.delta, self.delta):
                for k in np.arange(0, goal_size + self.delta, self.delta):
                    x, y, z = round(i, self.accuracy), round(j, self.accuracy), round(k, self.accuracy)
                    if (y,z,x) not in points_to_check:
                        points_to_check.append((y,z,x))
        for point in points_to_check:
            if self.is_part_of_a_cube(point):
                total += 1
        maximum = (goal_size-current_size) * (goal_size+1) * (goal_size+1) / (self.delta ** 3) * 3
        maximum -= 2 * ((goal_size-current_size) / self.delta)**3
        maximum -= 3 * (goal_size/self.delta)
        maximum = round(maximum, self.accuracy)
        return total/maximum

    def evaluate(self):
        """
        Evaluates the space by finding the largest size of a cube that can be fit
        into the space without any gaps.

        Returns:
            float: the size of the largest cube that can be fit into the space
        """
        value = self.n * 2
        while not self.check_grid_coverage(value):
            value -= self.delta
            value = round(value, self.accuracy)
        self.result = value
        return value