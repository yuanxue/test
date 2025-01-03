from dataclasses import dataclass, field
from typing import Set
from enum import Enum
import math


class TaskCategory(Enum):
    GEOMETRY = "Geometry"
    DATA_ANALYSIS = "DataAnalysis"
    SPATIAL_UNDERSTANDING = "SpatialUnderstanding"


raw_examples = [
    {
        'image_description': 'a triangle with sides labeled 5 cm, 12 cm, and 13 cm.',
        'query': 'Find the area of the triangle.'
        'ground_truth': 'triangle_area_by_sides(5, 12, 13)'
        'image': '9qY99XhidnZ9U7U.png'
    },
    {
        'task': 'An isosceles triangle is drawn with a base of 10 cm and equal sides of 7 cm.',
        'query': 'Find the perimeter of the triangle.'
        'ground_truth': 'isosceles_triangle_perimeter(10, 8)'
        'image': '3Wv9zBDP8J5rgRu'
    },
    {
        'task': 'A rectangle with dimensions 8 cm by 6 cm',
        'query': 'Calculate the perimeter of the rectangle'
        'ground_truth': 'rectangle_perimeter(8, 6)'
        'image': 'AQWqXKvyP87Bq5c'
    },
]


name_to_func = {
    "triangle_area_by_sides": '''
def triangle_area_by_sides(a: float, b: float, c: float) -> float:
    """Calculates the area of a triangle using Heron's formula.

    Args:
        a: Length of the first side.
        b: Length of the second side.
        c: Length of the third side.

    Returns:
        The area of the triangle.
    """
    s = (a + b + c) / 2  # Semi-perimeter
    return math.sqrt(s * (s - a) * (s - b) * (s - c))
''',
    "hypotenuse_length": '''
def hypotenuse_length(short_leg: float) -> float:
    """Calculates the hypotenuse of a right triangle.

    Args:
        short_leg: Length of the shorter leg of the triangle.

    Returns:
        The length of the hypotenuse.
    """
    return short_leg * math.sqrt(2)
''',
    "isosceles_triangle_perimeter": '''
def isosceles_triangle_perimeter(base: float, side: float) -> float:
    """Calculates the perimeter of an isosceles triangle.

    Args:
        base: Length of the base of the triangle.
        side: Length of the equal sides of the triangle.

    Returns:
        The perimeter of the triangle.
    """
    return 2 * side + base
''',
    "rectangle_perimeter": '''
def rectangle_perimeter(length: float, width: float) -> float:
    """Calculates the perimeter of a rectangle.

    Args:
        length: Length of the rectangle.
        width: Width of the rectangle.

    Returns:
        The perimeter of the rectangle.
    """
    return 2 * (length + width)
''',
    "parallelogram_area": '''
def parallelogram_area(base: float, height: float) -> float:
    """Calculates the area of a parallelogram.

    Args:
        base: Base length of the parallelogram.
        height: Height of the parallelogram.

    Returns:
        The area of the parallelogram.
    """
    return base * height
''',
    "trapezoid_area": '''
def trapezoid_area(base1: float, base2: float, height: float) -> float:
    """Calculates the area of a trapezoid.

    Args:
        base1: Length of the first base.
        base2: Length of the second base.
        height: Height of the trapezoid.

    Returns:
        The area of the trapezoid.
    """
    return (base1 + base2) * height / 2
''',
    "third_angle_of_triangle": '''
def third_angle_of_triangle(angle1: float, angle2: float) -> float:
    """Calculates the third angle of a triangle.

    Args:
        angle1: The first angle in degrees.
        angle2: The second angle in degrees.

    Returns:
        The third angle in degrees.
    """
    return 180 - (angle1 + angle2)
''',
    "vertical_angle": '''
def vertical_angle(angle: float) -> float:
    """Finds the measure of the vertical angle.

    Args:
        angle: Measure of one angle in degrees.

    Returns:
        Measure of the vertical angle in degrees.
    """
    return angle
''',
    "sum_of_interior_angles": '''
def sum_of_interior_angles(sides: int) -> float:
    """Calculates the sum of interior angles of a polygon.

    Args:
        sides: Number of sides of the polygon.

    Returns:
        The sum of the interior angles in degrees.
    """
    return (sides - 2) * 180
''',
    "circle_circumference": '''
def circle_circumference(radius: float) -> float:
    """Calculates the circumference of a circle.

    Args:
        radius: Radius of the circle.

    Returns:
        The circumference of the circle.
    """
    return 2 * math.pi * radius
''',
    "sector_area": '''
def sector_area(radius: float, angle: float) -> float:
    """Calculates the area of a sector of a circle.

    Args:
        radius: Radius of the circle.
        angle: Central angle of the sector in degrees.

    Returns:
        The area of the sector.
    """
    return (angle / 360) * math.pi * radius**2
''',
    "cylinder_volume": '''
def cylinder_volume(radius: float, height: float) -> float:
    """Calculates the volume of a cylinder.

    Args:
        radius: Radius of the cylinder's base.
        height: Height of the cylinder.

    Returns:
        The volume of the cylinder.
    """
    return math.pi * radius**2 * height
''',
    "cube_surface_area": '''
def cube_surface_area(side: float) -> float:
    """Calculates the total surface area of a cube.

    Args:
        side: Length of one side of the cube.

    Returns:
        The total surface area of the cube.
    """
    return 6 * side**2
''',
    "cone_slant_height": '''
def cone_slant_height(radius: float, height: float) -> float:
    """Calculates the slant height of a cone.

    Args:
        radius: Radius of the base of the cone.
        height: Height of the cone.

    Returns:
        The slant height of the cone.
    """
    return math.sqrt(radius**2 + height**2)
''',
    "triangle_area_coordinates": '''
def triangle_area_coordinates(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> float:
    """Calculates the area of a triangle using its vertices in a coordinate plane.

    Args:
        x1: x-coordinate of the first vertex.
        y1: y-coordinate of the first vertex.
        x2: x-coordinate of the second vertex.
        y2: y-coordinate of the second vertex.
        x3: x-coordinate of the third vertex.
        y3: y-coordinate of the third vertex.

    Returns:
        The area of the triangle.
    """
    return abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2
''',
    "distance_between_points": '''
def distance_between_points(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculates the distance between two points.

    Args:
        x1: x-coordinate of the first point.
        y1: y-coordinate of the first point.
        x2: x-coordinate of the second point.
        y2: y-coordinate of the second point.

    Returns:
        The distance between the points.
    """
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
''',
    "line_slope": '''
def line_slope(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculates the slope of a line passing through two points.

    Args:
        x1: x-coordinate of the first point.
        y1: y-coordinate of the first point.
        x2: x-coordinate of the second point.
        y2: y-coordinate of the second point.

    Returns:
        The slope of the line.
    """
    return (y2 - y1) / (x2 - x1) if x1 != x2 else float('inf')
'''
}
