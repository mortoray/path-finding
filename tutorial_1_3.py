import mortoray_path_finding as mpf
	
maze = mpf.maze.create_wall_maze( 20, 12 )
filled = mpf.tutorial_1.fill_shortest_path(maze.board, maze.start, maze.end)
path = mpf.tutorial_1.backtrack_to_start(filled, maze.end)

finder = mpf.draw.Finder()
finder.set_board(filled)
finder.set_path(path)
finder.run()

