import matplotlib.pyplot as plt
import math


class Point:
    def __init__(self, x: float | int = 0., y: float | int = 0., accuracy: int = 2,
                 silence_mode: bool = False) -> None:
        """
        Initialization

        :param x: The coordinate of the point on the 'x' axis, default = 0.0
        :param y: The coordinate of the point on the 'y' axis, default = 0.0
        :param accuracy: The number of decimal in calculations, default = 2
        :param silence_mode: Output message or not, default = False
        """

        if not (isinstance(x, float | int) and isinstance(y, float | int)):
            raise TypeError("x and y must be floats/integers")
        elif not isinstance(accuracy, int):
            raise TypeError("accuracy must be an integer")
        elif not isinstance(silence_mode, bool):
            raise TypeError("silence_mode must be a bool")

        self.__decimal = accuracy
        self.__silence_mode = silence_mode
        self.x = x
        self.y = y
        self.vector = (x, y)

        if not self.__silence_mode:
            print(f"{Point.__name__}: {self.x, self.y}")

    def get_coordinates(self) -> tuple:
        """
        Get current cartesian coordinates
        """

        if not self.__silence_mode:
            print(f"{Point.__name__}: {self.x, self.y}")

        return self.x, self.y

    def get_polar_coordinates(self, degrees: bool = True) -> tuple:
        """
        Convert cartesian coordinates to polar

        :param degrees: return coordinates in [deg] or [rad], default in [deg]
        """

        x_polar = self.x
        y_polar = self.y
        message = f"{Point.__name__}: {self.x, self.y} -> polar -> "

        if self.x == 0 or self.y == 0:

            if self.x == self.y == 0:
                message += "[possible any angle] -> "
            elif self.x == 0:
                x_polar = self.y
                y_polar = math.pi / 2

        else:

            r = (self.x ** 2 + self.y ** 2) ** 0.5
            phi = math.atan(self.y / self.x)
            x_polar = r
            y_polar = phi

        if degrees:
            x_polar, y_polar = self.radians_to_degrees()

        x_polar = round(x_polar, self.__decimal)
        y_polar = round(y_polar, self.__decimal)

        message += f"{x_polar, y_polar}"
        if degrees:
            message += " [deg]"
        else:
            message += " [rad]"

        if not self.__silence_mode:
            print(message)

        return x_polar, y_polar

    def set_coordinates(self, x: float, y: float) -> None:
        """
        Set new coordinates
        """

        old_x = self.x
        old_y = self.y
        self.x = x
        self.y = y
        self.vector = (x, y)

        message = f"{Point.__name__}: {old_x, old_y} -> update -> {self.x, self.y}"
        if not self.__silence_mode:
            print(message)

    def radians_to_degrees(self) -> tuple:
        """
        Convert radians to degrees
        """

        x_rad = self.x * 180 / math.pi
        y_rad = self.y * 180 / math.pi

        return x_rad, y_rad

    def distance(self, point: "Point") -> float:
        """
        Point-to-point distance
        """

        distance = ((self.x - point.x) ** 2 + (self.y - point.y) ** 2) ** 0.5
        distance = round(distance, self.__decimal)

        message = f"Distance between {self.x, self.y} and {point.x, point.y} -> {distance}"
        if not self.__silence_mode:
            print(message)

        return distance

    def equality(self, compared: "Point") -> bool:
        """
        Check points equality

        :param compared: (x, y) object, class 'Point'
        """

        if not self.__silence_mode:
            print(self.vector == compared.vector)

        return self.vector == compared.vector

    def plot(self) -> None:
        """
        Plotting points
        """

        plt.plot([0, self.x], [self.y, self.y], color="black", linestyle="dashed")
        plt.plot([self.x, self.x], [0, self.y], color="black", linestyle="dashed")
        plt.plot(self.x, self.y, "ro", markersize=15)
        plt.show()


class Line:
    def __init__(self, start_point: Point, end_point: Point) -> None:
        """
        Initialization

        :param start_point: Start point, default (0, 0)
        :param end_point: End point, default (0, 0)
        """

        if not (isinstance(start_point, Point) and isinstance(end_point, Point)):
            raise TypeError("points must be a class 'Point'")

        self.__p1 = start_point.vector
        self.x1, self.y1 = self.__p1
        self.__p2 = end_point.vector
        self.x2, self.y2 = self.__p2

    def __iter__(self):
        return self.__p1, self.__p2

    def set_points(self, start_point: Point, end_point: Point) -> None:
        """
        Set new points

        :param start_point: Start point
        :param end_point: End point
        """

        self.__p1 = start_point.vector
        self.x1, self.y1 = self.__p1
        self.__p2 = end_point.vector
        self.x2, self.y2 = self.__p2

    def plot(self) -> None:
        """
        Plotting line
        """

        plt.plot([self.x1, self.x2],
                 [self.y1, self.y2],
                 color="black")
        plt.show()

    @staticmethod
    def det_2x2(x: tuple[float, float], y: tuple[float, float]) -> float:
        """
        Calculating determinant (2x2 matrix)

        :param x: first column
        :param y: second column
        """

        return x[0] * y[1] - x[1] * y[0]

    def length(self, line: "Line") -> tuple[tuple[float, float], tuple[float, float]]:
        """
        Lines width and high
        """

        width = (abs(self.x1 - self.x2), abs(line.x1 - line.x2))
        high = (abs(self.y1 - self.y2), abs(line.y1 - line.y2))

        return width, high

    def linear_equation(self, line: "Line") -> tuple[tuple[float, float], tuple[float, float]]:
        """
        Solving linear equations
        """

        x_diff, y_diff = self.length(line)
        slope = (y_diff[0] / x_diff[0], y_diff[1] / x_diff[1])
        intercept = (self.y1 - slope[0] * self.x1, line.y1 - slope[1] * line.x1)

        return slope, intercept

    def check_parallel_touch(self, line: "Line") -> bool:
        """
        Checking whether parallel lines touch at the ends
        """

        k, b = self.linear_equation(line)
        if k[0] == k[1] and b[0] == b[1]:
            x1_touch = ((line.x1 == self.x1) and (line.x2 < self.x1)) or ((line.x1 == self.x2) and (line.x2 > self.x2))
            x2_touch = ((line.x2 == self.x1) and (line.x1 < self.x1)) or ((line.x2 == self.x2) and (line.x1 > self.x2))

            if x1_touch ^ x2_touch:
                return True

        return False

    def check_parallel_intersection(self, line: "Line") -> bool:
        """
        Checking whether parallel lines intersect
        """

        k, b = self.linear_equation(line)
        if k[0] == k[1] and b[0] == b[1]:
            x1_inside = (line.x1 >= self.x1) and (line.x1 <= self.x2)
            x2_inside = (line.x2 >= self.x1) and (line.x2 <= self.x2)
            x1x2_over = ((line.x1 <= self.x1) and (line.x2 >= self.x2)) or \
                        ((line.x1 >= self.x1) and (line.x2 <= self.x2))

            if x1_inside or x2_inside or x1x2_over:
                return True

        return False

    def intersection(self, line: "Line") -> bool:
        """
        Checking whether lines intersect
        """

        x_diff, y_diff = self.length(line)

        if not (self.det_2x2(x_diff, y_diff) or self.check_parallel_intersection(line)):
            print(False)
            return False

        print(True)
        return True

    def intersection_point(self, line: "Line") -> Point:
        """
        Finding intersection point
        """

        if not self.intersection(line):
            raise Exception("lines don't intersect")

        x_diff, y_diff = self.length(line)
        div = self.det_2x2(x_diff, y_diff)
        if div == 0:
            if self.check_parallel_touch(line):
                x, y = (self.x1, self.y1) if self.x1 == line.x1 else (self.x2, self.y2)
            else:
                raise Exception("infinity number of points")
        else:
            det = (self.det_2x2(*self), self.det_2x2(*line))
            x = self.det_2x2(det, x_diff) / div
            y = self.det_2x2(det, y_diff) / div

        p = Point(x, y, silence_mode=True)
        print(p.get_coordinates())

        return p


if __name__ == "__main__":
    a = Point(0, 0)
    b = Point(5, 5)
    c = Point(4, 4)
    d = Point(16, 16)
    a.distance(b)
    a.get_coordinates()
    b.get_polar_coordinates()
    c.set_coordinates(5, 5)
    b.equality(c)
    d.plot()

    l1 = Line(a, b)
    l2 = Line(c, d)
    l1.plot()
    if l1.intersection(l2):
        l1.intersection_point(l2)
