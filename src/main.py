#!/usr/bin/env python3

import curses
from curses.textpad import Textbox, rectangle
from atm import Atm

class Menu:
	def __init__(self, stdscr, title="Menu"):
		self.__title  = title

		# Initialize the ATM application Colors
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
		self.__terminal_color = curses.color_pair(1) # Set the terminal color
		
		curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
		self.__input_color = curses.color_pair(2) # Set the input color
	# END __init__

	def start(self):
		
		pass
	# END start 	

	def end(self):
		# Clean up the curses window
		curses.endwin()
	# END end

	def login(self):
		pass
	# END login

	def __del__(self):
		# Clean up the curses window
		curses.endwin()
	# END __del__
# END Menu

def main(stdscr):
	menu = Menu(stdscr, "ATM Application")
	menu.start()
# END main

if __name__ == "__main__":
	curses.wrapper(main)