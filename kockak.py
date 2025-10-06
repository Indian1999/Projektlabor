class Cube:
    def __init__(self, size, x = 0, y = 0, z = 0):
        self.size = size
        self.x = x
        self.y = y
        self.z = z

    
class Space:
    def __init__(self, n):
        self.n = n
        self.cubes = [Cube(i) for i in range(n, 0, -1)] # n méretű az első, mert azt fixáljuk

    def fitness(self):
        value = self.n    # n*n-es kockát biztos le tudunk fedni

    def planes_part_of_cube(self, point: tuple[int])-> bool:
        """
            A point in the spaces defines 3 planes, 
                one where we lock the x coordinate and iterate the rest until they reach 0, 
                second where we lock the y coordinate and iterate the rest until 0,
                The third where we lock the z axis.
            This method finds out if all the points that are elements of these planes are part of at least one cube
        """

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
        for cube in self.subes:
            if x >= cube.x and x <= cube.x + cube.size and y >= cube.y and y <= cube.y + cube.size and z >= cube.z and z <= cube.z + cube.size:
                return True
        return False


    
def volume_sum(n:int) -> int:
    """
        Returns the sum of the volumes of n cubes, each cube has a sidelength of 1, 2, 3, ... n
        Args: n (int) - The number of cubes
    """
    total = 0
    for i in range(1, n+1):
        total += i**3
    return total

print([volume_sum(i) for i in range(5, 20)])



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

print(volumes_slided_big_cubes(5, 3))