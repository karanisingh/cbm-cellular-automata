# src/utils/grid_maker.py

grid = [[0] * 100 for _ in range(100)]

# Modify the middle row
grid[49][25] = 2
grid[49][75] = 2

# Open a file in write mode (you can change 'output.txt' to your desired file name)
with open('output.txt', 'w') as file:
    for row in grid:
        file.write(','.join(map(str, row)) + '\n')
