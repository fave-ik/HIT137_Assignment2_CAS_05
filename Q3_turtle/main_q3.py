"""
Q3 – Recursive turtle pattern on a polygon
- User inputs: number of sides, side length, recursion depth.
- Applies an inward indentation on each edge , recursively.
"""

import turtle as T
from math import cos, sin, pi

def koch_inward(length, depth):
    """Draw one edge with an inward equilateral indentation."""
    if depth == 0:
        T.forward(length)
        return
    third = length / 3.0
    # First segment
    koch_inward(third, depth - 1)
    # Turn inward to form indentation
    T.left(60)
    koch_inward(third, depth - 1)
    T.right(120)
    koch_inward(third, depth - 1)
    T.left(60)
    koch_inward(third, depth - 1)

def draw_polygon_with_pattern(sides, side_len, depth):
    angle = 360.0 / sides
    for _ in range(sides):
        koch_inward(side_len, depth)
        T.right(angle)

def main():
    try:
        sides = int(input("Enter the number of sides (>=3): ").strip())
        side_len = float(input("Enter the side length (px): ").strip())
        depth = int(input("Enter the recursion depth (>=0): ").strip())
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return

    if sides < 3 or side_len <= 0 or depth < 0:
        print("Invalid parameters. sides>=3, side_len>0, depth>=0 required.")
        return

    T.speed(0)
    T.hideturtle()
    T.up(); T.goto(-side_len, side_len/2); T.down()
    draw_polygon_with_pattern(sides, side_len, depth)
    T.done()

if __name__ == "__main__":
    main()
