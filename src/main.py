#!/usr/bin/env python3

import curses
from curses.textpad import Textbox, rectangle
from atm import Atm

class Menu:
	def __init__(self, stdscr, title="Menu"):
		self.__atm = Atm()
		# Initialize the ATM application Colors
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
		self.__terminal_color = curses.color_pair(1) # Set the terminal color
		curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
		self.__input_color = curses.color_pair(2) # Set the input color
		self.stdscr = stdscr # Store the standard screen object
		self.__title  = title
		self.height, self.width = self.stdscr.getmaxyx() # Get terminal dimensions
		self.__title_y = 1; self.__title_x = ((self.width - len(self.__title)) // 2) # Center the title
	# END __init__

	def __display_title(self):
		# Display the title at the top center
		self.stdscr.addstr(self.__title_y, self.__title_x, self.__title, self.__terminal_color | curses.A_BOLD)
	# END __display_title	

	def start(self):
		curses.start_color()

		# Set the background color
		self.stdscr.bkgd(' ', self.__terminal_color)
		self.stdscr.clear()

		while True:
			self.__display_title()
			self.__login()
			self.stdscr.clear()
		# END while
	# END start 	

	def end(self):
		# Clean up the curses window
		curses.endwin()
	# END end

	def __login(self):
		# Center the input fields
		username_prompt = "Enter Username: "
		pin_prompt = "Enter PIN (4 digits): "
		username_y = self.height // 2 - 2
		username_x = (self.width - len(username_prompt) - 20) // 2
		pin_y = self.height // 2
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
		# END while
		self.stdscr.refresh()
		
		# Display the collected data (for debugging purposes)
		self.stdscr.clear()
		self.stdscr.addstr(self.height // 2, self.width // 2 - 10, f"Username: {username}", curses.color_pair(1))
		self.stdscr.addstr(self.height // 2 + 1, self.width // 2 - 10, f"PIN: {'*' * len(pin)}", curses.color_pair(1))
		self.stdscr.refresh()
		self.stdscr.getch()
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