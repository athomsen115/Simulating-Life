This program demonstrates Conway's Game of Life. 
It is built of a grid of 9 squares, every cell has 8 neighbors. 
The grid wraps around, (a torus), so that even the boundaries have neighbors.

There are Four Rules:
1. If a cell is ON and has fewer that two neighbors ON, it turns OFF
2. If a cell is ON and has two or three neighbors ON, it remains ON
3. If a cell is ON and has more than three neighbors ON, it turns OFF
4. If a cell is OFF and has exactly three neighbors ON, it turns ON

It is meant to mirror how organisms fair over time, demonstrating underpopulation and overpopulation
