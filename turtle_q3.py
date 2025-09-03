# Recursive function to draw one fractal edge with inward dents
def fractal_edge(length, depth):
    if depth == 0:
        turtle.forward(length)   # straight line
    else:
        part = length / 3

        # first part
        fractal_edge(part, depth - 1)

        # inward dent
        turtle.right(60)
        fractal_edge(part, depth - 1)
        turtle.left(120)
        fractal_edge(part, depth - 1)
        turtle.right(60)

        # last part
        fractal_edge(part, depth - 1)

# Main program
def main():
    # Fixed shape = pentagon
    sides = 5

    print("This program draws a fractal pentagon with inward dents.\n")
    side_length = int(input("Enter the side length (pixels): "))
    depth = int(input("Enter recursion depth (0 = straight line): "))

    # Print confirmation of user choices
    print("\n--- Drawing Settings ---")
    print(f"Shape: Pentagon (5 sides)")
    print(f"Side length: {side_length} pixels")
    print(f"Recursion depth: {depth}\n")

    # Setup turtle
    turtle.speed(0)
    for _ in range(sides):
        fractal_edge(side_length, depth)
        turtle.right(360 / sides)

    turtle.done()

if __name__ == "__main__":
    main()
