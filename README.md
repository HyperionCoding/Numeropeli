# Numeropeli

Simple number game where you have to fill the grid with numbers in order following the rules.
The next number has to be either 3 steps away in any cardinal direction or 2 steps in any ordinal direction. For example 3 to the right, or 2 to the left and down.

The numbers can be written to the tiles or right clicked to place the next number. Right clicking a tile with a number in it reverts the game to that point (be careful!).

Green tile means the next number can be placed there. Red tile indicates a dead tile. Dead tiles have two or less possible connections and not moving to that tile means it will become a dead end. Yellow tile is the current highest tile. Blue coloring is purely visual.

Example solutions for 5x5-10x10 grids are included.

### Arguments:
--g	  Grid size

--t	  Tile size

--a  	Enable automatic numbering of tiles when there is only one possibility
