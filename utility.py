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