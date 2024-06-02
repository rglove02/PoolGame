# import Physics

# def create_svg_file(table, index):
#     # Format the filename with the current index
#     filename = f"table-{index}.svg"
#     # Use the svg method of the table to get the SVG string
#     svg_content = table.svg()
#     # Write the SVG string to the file
#     with open(filename, 'w') as file:
#         file.write(svg_content)
#     print(f"SVG file created: {filename}")

# def main():
#     # Create a table instance
#     table = Physics.Table()

#     # Initialize the objects and add them to the table
#     # This part is specific to your simulation setup and needs to be adjusted accordingly
#     # For example:
#     ball_pos = Physics.Coordinate(1000, 100)  # Example ball position
#     ball_vel = Physics.Coordinate(10, 0)     # Example ball velocity
#     ball_acc = Physics.Coordinate(0, 0)      # Example ball acceleration
#     ball = Physics.RollingBall(1, ball_pos, ball_vel, ball_acc)
#     table += ball

#     # Example of adding other objects like holes or cushions
#     # hole_pos = Physics.Coordinate(500, 250)
#     # hole = Physics.Hole(hole_pos)
#     # table += hole

#     # Initially create an SVG for the starting state of the table
#     create_svg_file(table, 0)
    
#     # Perform simulation steps and create SVG files for each state
#     index = 1
#     while True:
#         table = table.segment()
#         if table is None:
#             break
#         create_svg_file(table, index)
#         index += 1

# if __name__ == "__main__":
#     main()

#!/usr/bin/env python3

import math
import sys
sys.path.append('/root/cis2750/A4')
import Physics

table = Physics.Table()

pos = Physics.Coordinate(0, 0)

pos.x = Physics.TABLE_WIDTH / 2.0 - math.sqrt(Physics.BALL_DIAMETER * Physics.BALL_DIAMETER / 2.0)
pos.y = Physics.TABLE_WIDTH / 2.0 - math.sqrt(Physics.BALL_DIAMETER * Physics.BALL_DIAMETER / 2.0)

sb = Physics.StillBall(1, pos)

pos.x = Physics.TABLE_WIDTH / 2.0
pos.y = Physics.TABLE_LENGTH - Physics.TABLE_WIDTH / 2.0
vel = Physics.Coordinate(0.0, -1000.0)
acc = Physics.Coordinate(0.0, 180.0)

rb = Physics.RollingBall(0, pos, vel, acc)

table += sb

table += rb

i = 0

while table:

    with open("table-%d.svg" %(i), "w") as file:
        file.write(table.svg())
    i+=1
    table = table.segment()