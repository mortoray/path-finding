import mortoray_path_finding as mpf

maze = mpf.maze.create_wall_maze( 20, 12 )

finder = mpf.draw.Finder()
finder.set_board(maze.board)
finder.run()


