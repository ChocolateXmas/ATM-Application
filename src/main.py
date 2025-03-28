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

		self.stdscr = stdscr
		self.__atm = Atm()
	# END __init__

	def start(self):
		curses.start_color()

		# Set the background color
		self.stdscr.bkgd(' ', self.__terminal_color)
		self.stdscr.clear()

		# Get terminal dimensions
		height, width = self.stdscr.getmaxyx()

		# Display the title at the top center
		title_y = 1
		title_x = (width - len(self.__title)) // 2
		self.stdscr.addstr(title_y, title_x, self.__title, curses.color_pair(1) | curses.A_BOLD)

		self.__login(height, width)

		# Display the collected data (for debugging purposes)
		self.stdscr.clear()
		self.stdscr.addstr(height // 2, width // 2 - 10, f"Username: {username}", curses.color_pair(1))
		self.stdscr.addstr(height // 2 + 1, width // 2 - 10, f"PIN: {'*' * len(pin)}", curses.color_pair(1))
		self.stdscr.refresh()
		self.stdscr.getch()
	# END start 	

	def end(self):
		# Clean up the curses window
		curses.endwin()
	# END end

	def __login(self, height, width):
		# Center the input fields
		username_prompt = "Enter Username: "
		pin_prompt = "Enter PIN (4 digits): "
		username_y = height // 2 - 2
		username_x = (width - len(username_prompt) - 20) // 2
		pin_y = height // 2
		pin_x = username_x

		# Input for username
		self.stdscr.addstr(username_y, username_x, username_prompt, curses.color_pair(2))
		username_win = curses.newwin(1, 20, username_y, username_x + len(username_prompt))
		curses.textpad.rectangle(self.stdscr, username_y - 1, username_x + len(username_prompt) - 1,
									username_y + 1, username_x + len(username_prompt) + 20)
		self.stdscr.refresh()
		username_box = curses.textpad.Textbox(username_win)
		username = username_box.edit().strip()

		# Input for PIN (hidden with *)
		self.stdscr.addstr(pin_y, pin_x, pin_prompt, curses.color_pair(2))
		pin_win = curses.newwin(1, 20, pin_y, pin_x + len(pin_prompt))
		curses.textpad.rectangle(self.stdscr, pin_y - 1, pin_x + len(pin_prompt) - 1,
									pin_y + 1, pin_x + len(pin_prompt) + 20)
		self.stdscr.refresh()

		pin = ""
		while len(pin) < 4:
			key = pin_win.getch()
			if key in range(48, 58):  # Check if the key is a digit (ASCII 48-57)
				pin += chr(key)
				pin_win.addch('*')
			elif key == curses.KEY_BACKSPACE or key == 127:  # Handle backspace
				if len(pin) > 0:
					pin = pin[:-1]
					y, x = pin_win.getyx()
					pin_win.delch(y, x - 1)
		self.stdscr.refresh()
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