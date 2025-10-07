class Cube:
    def __init__(self, size, x = 0, y = 0, z = 0):
        self.size = size
        self.x = x
        self.y = y
        self.z = z
        self.set_vertices()
        self.set_faces()

    def set_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

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
