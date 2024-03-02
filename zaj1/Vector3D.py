import math


class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'Vector3D({self.x}, {self.y}, {self.z})'

    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3D(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)

    @staticmethod
    def are_orthogonal(v1, v2):
        if v1.dot(v2) == 0:
            return True
        return False


vector1 = Vector3D(1, 2, 3)
vector2 = Vector3D(4, 5, 6)

print(f'Print #1: {vector1}')
print(f'Print #2: {vector2}')
print(f'Norm: {vector1.norm()}')
print(f'Add: {vector1 + vector2}')
print(f'Sub: {vector1 - vector2}')
print(f'Mul(2): {vector1*2}')
print(f'Dot: {vector1.dot(vector2)}')
print(f'Cross: {vector1.cross(vector2)}')
print(f'Are orthogonal: {Vector3D.are_orthogonal(vector1, vector2)}')