## References
# https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
# https://graphics.stanford.edu/courses/cs348a-17-winter/Papers/quaternion.pdf
# https://courses.cs.duke.edu/compsci344/spring15/classwork/11_rotations/UnderstandingQuat.pdf
# https://www.anyleaf.org/blog/quaternions:-a-practical-guide
# https://www.cprogramming.com/tutorial/3d/quaternions.html

import math

class Quaternion:
    def __init__(self, w = 0, x = 0, y = 0, z = 0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Quaternion({self.w}, {self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        return Quaternion(self.w + other.w,
                          self.x + other.x,
                          self.y + other.y,
                          self.z + other.z)

    def __mul__(self, other):
        return Quaternion(
            self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z,
            self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y,
            self.w*other.y - self.x*other.z + self.y*other.w + self.z*other.x,
            self.w*other.z + self.x*other.y - self.y*other.x + self.z*other.w)

    def conjugate(self):
        return Quaternion(+self.w,
                          -self.x,
                          -self.y,
                          -self.z)

    def magnitude(self):
        return math.sqrt(self.w**2 +
                         self.x**2 +
                         self.y**2 +
                         self.z**2)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero-magnitude Quaternion.")
        return Quaternion(self.w/mag,
                          self.x/mag,
                          self.y/mag,
                          self.z/mag)

    def inverse(self):
        # q^{-1} = frac{q^*}{|q|^2}
        mag_sq = self.magnitude()**2
        if mag_sq == 0:
            raise ValueError("Cannot invert a zero-magnitude quaternion.")
        conjugate = self.conjugate()
        return Quaternion(conjugate.w/mag_sq,
                          conjugate.x/mag_sq,
                          conjugate.y/mag_sq,
                          conjugate.z/mag_sq)

    def rotate_vector(self, vector):
        vec_quat = Quaternion(0, *vector)
        result = self*vec_quat*self.inverse()
        return (result.x, result.y, result.z)

    def to_rotation_matrix(self):
        w, x, y, z = self.w, self.x, self.y, self.z
        return [
            [1 - 2*(y*y + z*z),     2*(x*y - z*w),     2*(x*z + y*w)],
            [    2*(x*y + z*w), 1 - 2*(x*x + z*z),     2*(y*z - x*w)],
            [    2*(x*z - y*w),     2*(y*z + x*w), 1 - 2*(x*x + y*y)],
        ]

    @staticmethod
    def from_axis_angle(axis, angle):
        half_angle = angle/2
        sin_half_angle = math.sin(half_angle)
        return Quaternion(math.cos(half_angle),
                          axis[0]*sin_half_angle,
                          axis[1]*sin_half_angle,
                          axis[2]*sin_half_angle)

if __name__ == "__main__":
    print(f"{Quaternion(1, 2, 3, 4) + Quaternion(3, 2, 4, 1) = }\n")
    print(f"{Quaternion(1, 2, 3, 4)*Quaternion(3, 2, 4, 1) = }\n")
    print(f"{Quaternion.from_axis_angle((0, 0, 1), math.pi/2) = }\n")
    print(f"{Quaternion(1, 2, 3, 4).normalize() = }\n")
    print(f"{Quaternion(1, 2, 3, 4).conjugate() = }\n")
    print(f"{Quaternion(1, 2, 3, 4).inverse() = }\n")
    print(f"{Quaternion(1, 2, 3, 4).rotate_vector((1, 0, 0)) = }\n")
    print(f"{Quaternion(1, 2, 3, 4).to_rotation_matrix() = }")
