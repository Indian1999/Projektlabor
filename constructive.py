import random
import time
from space import Space
from cube import Cube
from cubesolver import CubeSolver
import os
import numpy as np

class Constructive:
    def __init__(self, n: int, accuracy: int = 0, reach = None, strategy: str = "corner_first", iterations: int = 100 ):
        self.n = n
        self.accuracy = accuracy
        self.reach = reach
        self.strategy = strategy
        self.iterations = iterations
        self.delta = 10 ** -self.accuracy
        self.results = []
        self.running = False
        self.best = None

    def find_gaps(self, space: Space, target_size: float) -> list[tuple]:
        gaps = []
        step = self.delta
        if step < 1:
            step = 0.5 # Nagyobb accuracy esetén csak közelítünk
        for i in np.arange(0, target_size + self.delta, step):
            for j in np.arange(0, target_size + self.delta, step):
                for k in np.arange(0, target_size + self.delta, step):
                    x = round(i, self.accuracy)
                    y = round(j, self.accuracy)
                    z = round(k, self.accuracy)
                    if not space.is_part_of_a_cube((x,y,z)):
                        gaps.append((x,y,z))
        return gaps

    def score_position(self, space: Space, cube: Cube, x: float, y: float, z: float) -> float:
        cube.set_position(x,y,z)
        if not space.is_cube_within_base_cube(cube):
            return -1000
        
        score = 0
        for i in np.arange(0, cube.size + self.delta, self.delta):
            for j in np.arange(0, cube.size + self.delta, self.delta):
                for k in np.arange(0, cube.size + self.delta, self.delta):
                    point = (round(x + i, self.accuracy), round(y + j, self.accuracy), round(z + k, self.accuracy))
                    if not space.is_part_of_a_cube(point):
                        score += 1
                    # Jutipontok minnél távolabb van a kocka bázispontjától
                    distance = np.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
                    score += distance * 0.01
        return score
    
    def corner_first_strategy(self, space: Space) -> Space:
        
        space.setup(reach=self.reach)

        target_size = self.n * 2 - 1
        for i in range(13, self.n):
            cube = space.cubes[i]
            best_score = -float("inf")
            best_pos = None
            gaps = self.find_gaps(space, target_size)
            positions_to_try = gaps[:min(50, len(gaps))]
            for j in range(20):
                x = random.randint(0, self.n-cube.size -1) / self.delta
                y = random.randint(0, self.n-cube.size -1) / self.delta
                z = random.randint(0, self.n-cube.size -1) / self.delta
                x = round(x, self.accuracy)
                y = round(y, self.accuracy)
                z = round(z, self.accuracy)
                positions_to_try.append((x,y,z))

            for pos in positions_to_try:
                x, y, z = pos
                score = self.score_position(space, cube, x, y, z)

                if score > best_score:
                    best_score = score
                    best_pos = pos
            if best_pos != None:
                cube.set_position(*best_pos)
        return space

    def layer_by_layer_strategy(self, space: Space) -> Space:
        """
        DOES NOT WORK PROPERLY, PUTS EVERYTHING ON (0,0,0)
        """
        cubes_to_place = space.cubes[1:]
        current_z = 0
        layer_height = 0
        for cube in cubes_to_place:
            placed = False
            for i in np.arange(0, self.n-cube.size +self.delta, self.delta):
                for j in np.arange(0, self.n-cube.size +self.delta, self.delta):
                    x = round(i, self.accuracy)
                    y = round(j, self.accuracy)

                    if current_z + cube.size <= self.n:
                        cube.set_position(x,y,current_z)
                        placed = True
                        layer_height = max(layer_height, cube.size)
                        break
                if placed:
                    break
            if not placed:
                current_z += layer_height
                layer_height = cube.size
                cube.set_position(0,0,current_z)
        return space
    
    def gap_filling_strategy(self, space: Space) -> Space:
        target_size = self.n*2-1
        for i in range(1, self.n):
            cube = space.cubes[i]
            gaps = self.find_gaps(space, target_size)
            if not gaps:
                cube.set_random_position(0, self.n - cube.size, self.delta)
            else:
                best_score = -float("inf")
                best_pos = None
                for gap in random.choices(gaps, k = min(40, len(gaps))):
                    x,y,z = gap
                    for i in [0, -cube.size/2, -cube.size]:
                        for j in [0, -cube.size/2, -cube.size]:
                            for k in [0, -cube.size/2, -cube.size]:
                                new_x = round(max(0, min(self.n-cube.size, x + i)), self.accuracy)
                                new_y = round(max(0, min(self.n-cube.size, y + j)), self.accuracy)
                                new_z = round(max(0, min(self.n-cube.size, z + k)), self.accuracy)
                                score = self.score_position(space, cube, new_x, new_y, new_z)
                                if score > best_score:
                                    best_score = score
                                    best_pos = (new_x, new_y, new_z)
                if best_pos != None:
                    cube.set_position(*best_pos)
        return space
    
    def hybrid_strategy(self, space:Space) -> Space:

        # Nagy kockák: az alap: sarkok, élfelező pontok
        # (Még a Space létrehozásánál be van állítva)
        mid_point = min(13 + (self.n-13)//2, self.n)
        target_size = self.n*2-1

        # Közepes kockák:
        for i in range(13, mid_point):
            cube = space.cubes[i]
            best_score = -float("inf")
            best_pos = None

            # Szélek, sarkok
            prefered_positions = [
                (0, 0, random.uniform(0, self.n - cube.size)),
                (0, random.uniform(0, self.n - cube.size), 0),
                (random.uniform(0, self.n - cube.size), 0, 0),
                (random.uniform(0, self.n - cube.size), random.uniform(0, self.n - cube.size), 0),
                (random.uniform(0, self.n - cube.size), 0, random.uniform(0, self.n - cube.size)),
                (0, random.uniform(0, self.n - cube.size), random.uniform(0, self.n - cube.size))
            ]

            for pos in prefered_positions:
                x = round(pos[0], self.accuracy)
                y = round(pos[1], self.accuracy)
                z = round(pos[2], self.accuracy)
                score = self.score_position(space, cube, x, y, z)
                if score > best_score:
                    best_score = score
                    best_pos = (x,y,z)
            if best_pos != None:
                cube.set_position(*best_pos)

        # Kis kockák: gap_filling
        for i in range(mid_point, self.n):
            cube = space.cubes[i]
            gaps = self.find_gaps(space, target_size)

            best_score = -float("inf")
            best_pos = None

            positions = random.choices(gaps, k = min(40, len(gaps)))
            for pos in positions:
                x,y,z = pos
                for i in [0, -cube.size/2, -cube.size]:
                    for j in [0, -cube.size/2, -cube.size]:
                        for k in [0, -cube.size/2, -cube.size]:
                            new_x = round(max(0, min(self.n-cube.size, x + i)), self.accuracy)
                            new_y = round(max(0, min(self.n-cube.size, y + j)), self.accuracy)
                            new_z = round(max(0, min(self.n-cube.size, z + k)), self.accuracy)

                            score = self.score_position(space, cube, new_x, new_y, new_z)
                            if score > best_score:
                                best_score = score
                                best_pos = (new_x,new_y,new_z)
            if best_pos != None:
                cube.set_position(*best_pos)
        return space

    def build_solution(self) -> Space:
        space = Space(self.n, self.accuracy, self.reach)
        if self.strategy == "corner_first":
            space = self.corner_first_strategy(space)
        elif self.strategy == "gap_filling":
            space = self.gap_filling_strategy(space)
        elif self.strategy == "layer_by_layer":
            space = self.layer_by_layer_strategy(space)
        elif self.strategy == "hybrid":
            space = self.hybrid_strategy(space)
        else:
            raise ValueError(f"Invalid strategy: {self.strategy}, available strategies: corner_first, gap_filling, layer_by_layer, hybrid")
        
        return space

    def to_json(self):
        return {
            "n": self.n,
            "accuracy": self.accuracy,
            "strategy": self.strategy,
            "iterations": self.iterations,
            "reach": self.reach
        }

    def get_params_string(self):
        """
        Returns a string that contains the parameters of the genetic algorithm.
        The string is in the format of: <date>_<n>_<strategy>_<iterations>_<accuracy>_<reach>
        This string is used to name the folder where the results of the genetic algorithm are stored.
        """
        return f"{time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())}_{self.n}_{self.strategy}_{self.iterations}_{self.accuracy}_{self.reach}"
   
    def pause(self):
        self.running = False

    def resume(self):
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        best_score = -float("inf")

        for iteration in range(self.iterations):
            if not self.running:
                break

            solution = self.build_solution()
            score = solution.evaluate()
            if score > best_score:
                best_score = score
                self.best = solution
                yield f"Iteration {iteration+1}/{self.iterations}: New best score: {score}"
            else:
                yield f"Iteration {iteration+1}/{self.iterations}: Score: {score} (best: {best_score})"

        yield f"Final best score: {best_score}"
        yield f"Exporting results..."
        self.export_results()
        yield "Done!"

    def export_results(self):
        path = os.path.dirname(__file__)
        os.makedirs(os.path.join(path, "results"), exist_ok=True)
        path = os.path.join(path, "results")
        dirname = self.get_params_string()
        os.makedirs(os.path.join(path, dirname), exist_ok=True)
        path = os.path.join(path, dirname)
        #os.makedirs(os.path.join(path, "plots"), exist_ok=True)
        os.makedirs(os.path.join(path, "spaces"), exist_ok=True)

        #self.best.plot_space(os.path.join(path, "plots", "best.png"), f"Score: {self.best.result}")
        self.best.print_space(os.path.join(path, "spaces", "best.json"))

        self.results.append(self.best.to_json())