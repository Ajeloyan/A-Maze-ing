from mazegen.generator import Grid
from mazegen.validator import parsing
import sys
from time import time

def main() -> None:
	output: str = "output_maze.txt"
	try:
		config = parsing(sys.argv[1])
	except Exception as e:
		print(e)
		sys.exit(1)
	grid = Grid(config)
	print()
	# grid.draw_grid()
	# grid.dig_maze()
	print()
	start = time()
	# grid.maze_solver()
	grid.dig_maze()
	path = grid.maze_solver()
	grid.draw_grid()
	end = time()
	progtime = end - start
	print(progtime)
	grid.generate_txt()
if __name__ == "__main__":
	main()
