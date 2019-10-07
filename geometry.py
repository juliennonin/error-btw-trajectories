import numpy as np
import doctest
from matplotlib.patches import Polygon

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def __str__(self):
        return f"⟨{self.x}, {self.y}⟩"
    
    def __eq__(self, point):
        return self.x == point.x and self.y == point.y
    
    def coordinates(self):
        return [self.x, self.y]
    
    def distance(self, point):
        """
        >>> np.round(Point(-8, 9 ).distance(Point( 0, 0)), 2)
        12.04
        >>> np.round(Point(10, 20).distance(Point(-4, 5)), 2)
        20.52
        >>> np.round(Point(-3, 5 ).distance(Point(-3, 5)), 2)
        0.0
        """
        return np.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)
    
class Vector:
    def __init__(self, anchor, endpoint):
        self.x = endpoint.x - anchor.x
        self.y = endpoint.y - anchor.y
            
    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)
    
    def __neg__(self):
        return Point(-self.x, -self.y)
    
    def __sub__(self, point):
        return self + (-point)
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __str__(self):
        return f"{{{self.x}, {self.y}}}"
    
    def scalar(self, vector):
        return self.x * vector.x + self.y * vector.y
    
    def is_colinear(self, vector):
        return self.x * vector.y - vector.x * self.y == 0
    
    def toArray(self):
        return np.array([self.x, self.y])
    
class LineSegment:
    def __init__(self, anchor, endpoint):
        self.anchor = anchor
        self.endpoint = endpoint
        
    def __repr__(self):
        return f"Ray({repr(self.anchor)}, {repr(self.endpoint)})"
    
    def __str__(self):
        return f"[{str(self.anchor)}⋯{str(self.endpoint)}]"
    
    def contains(self, point):
        """
        >>> LineSegment(Point(1, -2), Point(2, 0)).contains(Point(5, 6)) # working test
        False
        >>> LineSegment(Point(1, 0), Point(2, -1)).contains(Point(3, 1)) # working test
        False
        >>> LineSegment(Point(5, -1), Point(5, 4)).contains(Point(5, 0)) # vertical
        True
        """
        vec_a = Vector(self.anchor, self.endpoint)
        vec_b = Vector(self.anchor, point)
        return vec_a.is_colinear(vec_b) and 0 <= vec_a.scalar(vec_b) <= vec_a.scalar(vec_a)
    
    def line_equation_coeffs(self):
        """ax + by = c
    
        N.B. if (a, b, c) is a solution then λ(a, b, c) is also a solution
        >>> LineSegment(Point(3, 3), Point(2, 0)).line_equation_coeffs() # working test
        (-3, 1, -6)
        >>> LineSegment(Point(1, 2), Point(3, 2)).line_equation_coeffs() # a = 0
        (0, -2, -4)
        >>> LineSegment(Point(0, 0), Point(1, 3)).line_equation_coeffs() # c = 0
        (3, -1, 0)
        >>> LineSegment(Point(2, 2), Point(2, -1)).line_equation_coeffs()# b = 0
        (-3, 0, -6)
        """
        a = self.endpoint.y - self.anchor.y
        b = self.anchor.x - self.endpoint.x
        c = b * self.anchor.y + a * self.anchor.x
        return a, b, c
    
    def distance(self, point):
        """
        >>> np.round(LineSegment(Point(-1, 2), Point(2, 3)).distance(Point(1, 1)), 2) # working test
        1.58
        >>> np.round(LineSegment(Point(0, 1), Point(0, 3)).distance(Point(-1, 0)), 2) # vertical line
        1.0
        """
        a, b, c = self.line_equation_coeffs()
        return abs(b * point.y + a * point.x - c) / np.hypot(a, b)
    
    def intersects(self, seg):
        """
        Find intersection point between two segment lines : self & segment

        Parameters :
            - p1, p2, q1, q2 : np.ndarrays of shape (2,)
        Returns : the coordinates of the intersection points,  
            if the line segments intersect

        [TODO] Manage the case where the matrix is singular

        >>> LineSegment(Point(-2, 2), Point(3, 4)).intersects(LineSegment(Point(1, 5), Point(1, 2))) # [p1, p2] and ]q1, q2[ intersect
        Point(1.0, 3.2)
        >>> LineSegment(Point(1, 2), Point(4, 2)).intersects(LineSegment(Point(-2, 3), Point(-2, 1))) # (p1, p2) and ]q1, q2[ intersect but not [p1, p2] and ]q1, q2[
        >>> LineSegment(Point(2, 3), Point(2, 0)).intersects(LineSegment(Point(2, 2), Point(2, 1))) # colinear
        >>> LineSegment(Point(2, 3), Point(2, 0)).intersects(LineSegment(Point(1, 2), Point(1, -1))) # parallel
        """
        p1x, p1y = self.anchor.x, self.anchor.y
        p2x, p2y = self.endpoint.x, self.endpoint.y
        q1x, q1y = seg.anchor.x, seg.anchor.y
        q2x, q2y = seg.endpoint.x, seg.endpoint.y
        a = np.array([[q2x - q1x, p1x - p2x],
                      [q2y - q1y, p1y - p2y]])
        if np.linalg.det(a): # if a is invertible (if lines intersect)
            b = np.array([p1x - q1x, p1y - q1y])
            t = np.linalg.solve(a,b)
            if np.all(0 < t) and np.all(t < 1): # segments intersect
                intersection = Point(p1x + t[1] * (p2x - p1x), p1y + t[1] * (p2y - p1y))
                return intersection
        return None
    
    def toVector(self):
        return Vector(self.anchor, self.endpoint)