#!/usr/bin/python3
import mortoray_path_finding as mpf

finder = mpf.Finder()

board = mpf.create_wall_board(20,10)
finder.set_board(board)
finder.run()
