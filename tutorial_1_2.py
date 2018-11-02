import mortoray_path_finding as mpf
	
maze = mpf.maze.create_wall_maze( 20, 12 )
filled = mpf.tutorial_1.fill_shortest_path(maze.board, maze.start, maze.end)

finder = mpf.draw.Finder()
finder.set_board(filled)
finder.run()

