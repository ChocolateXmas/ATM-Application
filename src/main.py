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
		self.height, self.width = self.stdscr.getmaxyx() # Get terminal dimensions
		
		self.__title  = title
		self.__title_y = 1; self.__title_x = self.__get_middle_x(self.__title) # Center the title

		self.__greet_title = "ATM Menu"
		self.__greet_title_y = 1; self.__greet_title_x = self.__get_middle_x(self.__greet_title) # Center the greet title

		# Initialize the menu options
		self.__menu_actions = {
			"d": {"msg": "Press button d to Deposit Money", "function" : self.__deposit_screen},
			"w": {"msg": "Press button w to Withdraw Money", "function" : self.__withdraw_screen},
			"c": {"msg": "Press button c to Check your Balance", "function" : self.__balance_screen},
			"q": {"msg": "Press to q to Quit", "function" : self.__logout},
			"p": {"msg" : "Press button p to Change PIN_CODE", "function" : self.__change_pin_screen},
			"r": {"msg" : "Press button r to Get a RECIPE", "function" : self.__recipe_screen}
		}
	# END __init__

	def __display_title(self):
		# Display the title at the top center
		self.stdscr.addstr(self.__title_y, self.__title_x, self.__title, self.__terminal_color | curses.A_BOLD)
	# END __display_title	

	def __display_greet_title(self):
		self.stdscr.addstr(self.__greet_title_y, self.__greet_title_x, self.__greet_title, self.__terminal_color | curses.A_BOLD)
	# END __display_greet_title

	def start(self):
		curses.start_color()

		# Set the background color
		self.stdscr.bkgd(' ', self.__terminal_color)
		self.stdscr.clear()

		while True:
			self.stdscr.clear()
			self.__login()
			self.stdscr.clear()
			self.__menu_options()
		# END while
	# END start 	

	def end(self):
		# Clean up the curses window
		curses.endwin()
	# END end

	"""
		Gets the Y-coordinate of a former element for displaying the PINCODE input box below it accordingly.
		former:bool is True if we have a former element above the PINCODE input box, False otherwise

		Returns:
			str: The entered PIN code as a string.
	"""
	def __show_pincode_inputbox(self, pin_y, former=False) -> str:
		pin_prompt = "Enter PIN (4 digits): "
		max_pin_length = 14
		pin_y += 2 if former else 0
		pin_x = self.__get_middle_x(pin_prompt + " " * max_pin_length)
		# Input for PIN (hidden with *)
		self.stdscr.addstr(pin_y, pin_x, pin_prompt, self.__input_color)
		pin_win = curses.newwin(1, max_pin_length, pin_y, pin_x + len(pin_prompt))
		curses.textpad.rectangle(self.stdscr, pin_y - 1, pin_x + len(pin_prompt) - 1,
									pin_y + 1, pin_x + len(pin_prompt) + max_pin_length)
		self.stdscr.refresh()
		# PIN input
		pin = ""
		while True:
			key = pin_win.getch()
			if key in range(48, 58): # Check if the key is a digit (ASCII 48-57)
				if len(pin) < max_pin_length - 1:
					pin += chr(key)
					pin_win.addch('*')
				# END if 
			# END if
			elif key == curses.KEY_BACKSPACE or key == 127: # Handle backspace
				if len(pin) > 0:
					pin = pin[:-1]
					y, x = pin_win.getyx()
					pin_win.delch(y, x - 1)
				# END if
			# END elif
			elif key == curses.KEY_ENTER or key == 10 or key == 13: # Enter key
				if len(pin) == 4:
					break
				empty_pin_msg = "PIN must be 4 digits. Please try again."
				self.stdscr.addstr(pin_y + 2, self.__get_middle_x(empty_pin_msg), empty_pin_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT | curses.A_UNDERLINE)
				self.stdscr.refresh()
			# END elif
		# END while
		self.__clear_line(pin_y + 2)
		self.stdscr.refresh()
		return pin
	# END __show_pincode_inputbox

	def __login(self):
		while True:
			self.__display_title()
			# Center the input fields
			username_prompt = "Enter Username: "
			max_username_length = 20
			username_y = self.height // 2 - 2
			username_x = self.__get_middle_x(username_prompt + " " * max_username_length)
			# Username input box
			self.stdscr.addstr(username_y, username_x, username_prompt, self.__input_color)
			username_win = curses.newwin(1, 20, username_y, username_x + len(username_prompt))
			curses.textpad.rectangle(self.stdscr, username_y - 1, username_x + len(username_prompt) - 1, username_y + 1, username_x + len(username_prompt) + 20)
			username = ""
			# Input for username
			while len(username) == 0:
				self.stdscr.refresh()
				username_box = curses.textpad.Textbox(username_win)
				username = username_box.edit().strip()
				if len(username) == 0:
					empty_username_msg = "Username cannot be empty. Please try again."
					self.stdscr.addstr(username_y + 2, self.__get_middle_x(empty_username_msg), empty_username_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT | curses.A_UNDERLINE)
					self.stdscr.refresh()
				# END if
			# END while
			self.__clear_line( *range(username_y -1, username_y + 2 + 1) ) # Clear textbox & username input line
			welcome_msg = f"Welcome, {username}!"
			welcome_x = self.__get_middle_x(welcome_msg)
			self.stdscr.addstr(username_y, welcome_x, welcome_msg, self.__terminal_color | curses.A_BOLD)
			self.stdscr.refresh()

			pin = self.__show_pincode_inputbox(username_y , True)

			# Check if the username and PIN are correct, and set the user info
			if not self.__atm.login(username, pin):
				login_failed_msg = "Invalid username/PIN. try again. (Enter to continue)"
				login_x = self.__get_middle_x(login_failed_msg)
				self.stdscr.addstr(username_y + 4, login_x, login_failed_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT | curses.A_UNDERLINE)
				self.stdscr.refresh()
				self.stdscr.getch()
				self.stdscr.clear()
				continue
			# END if
			break
		# END while
	# END login

	"""
		Displays the greeting message after succesful login and waits for a key press to choose action.
	"""
	def __menu_options(self):
		while self.__atm.is_logged_in():
			self.stdscr.clear()
			self.stdscr.refresh()
			self.__display_greet_title()
			middle_y = (self.height // 2) - len(self.__menu_actions)
			for action, options in self.__menu_actions.items():
				msg = options["msg"]
				self.stdscr.addstr(middle_y, self.__get_middle_x(msg), msg, self.__terminal_color | curses.A_BOLD)
				middle_y += 1
			# END for
			self.stdscr.refresh()
			action = self.stdscr.getch()
			# check if the input char is in out menu actions keys (d, w, c, q, p, r)
			if chr(action) in self.__menu_actions:
				self.__menu_actions[ chr(action) ]["function"]()
			# END if
		# END while
	# END __greet

	def __deposit_screen(self):
		# self.__atm.deposit
		pass
	# END __deposit_screen

	def __withdraw_screen(self):
		# __atm.withdraw
		pass
	# END __withdraw_screen

	def __balance_screen(self):
		# __atm.get_balance
		pass
	# END __balance_screen

	def __logout(self):
		middle_y = (self.height // 2) - 2 # minus 2 because we have 2 lines to show (logout_msg | error_msg), and one empty break line between them
		try: 
			logout_msg = f"GOODBYE {str(self.__atm.get_user_name())}, HAVE A NICE DAY"
			self.__atm.logOut()
			# middle_y = (self.height // 2) - len(logout_msg)
			self.stdscr.clear()
			self.stdscr.addstr(middle_y, self.__get_middle_x(logout_msg), logout_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
			self.stdscr.refresh()
		# END try
		except ValueError as ve: 
			error_msg = str(ve)
			self.stdscr.clear()
			self.stdscr.addstr(middle_y, self.__get_middle_x(error_msg), error_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
			self.stdscr.refresh()
		# END except
		logout_exit_msg = "Press any key to EXIT"
		self.stdscr.addstr(middle_y + 2, self.__get_middle_x(logout_exit_msg), logout_exit_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
		self.stdscr.refresh()
		self.stdscr.getch()
	# END __logout

	"""
		def change_pin(self, newPin: str) -> None:
			if not self.is_logged_in():
				raise ValueError("User is not logged in")
			# END if
			users[self.__userName]["pin"].set_pin(newPin)
		# END change_pin
	"""
	def __change_pin_screen(self):
		# __atm.change_pin
		middle_y = (self.height // 2) - 3 # minus 3 because we have 3 lines to show (logout_msg | error_msg), and one empty break line between them
		try:
			self.stdscr.clear() 
			new_pin_msg = f"Hello {str(self.__atm.get_user_name())}, Enter NEW PINCODE"
			self.stdscr.addstr(middle_y, self.__get_middle_x(new_pin_msg), new_pin_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
			self.stdscr.refresh()
			new_pin = self.__show_pincode_inputbox(middle_y , True)
			self.__atm.change_pin(new_pin)
		# END try
		except ValueError as ve: 
			error_msg = str(ve)
			self.stdscr.clear()
			self.stdscr.addstr(middle_y, self.__get_middle_x(error_msg), error_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
			self.stdscr.refresh()
		# END except
		middle_y += 4
		new_pin_exit_msg = "PINCODE changed succesfuly! Press any key to get BACK"
		self.stdscr.addstr(middle_y + 2, self.__get_middle_x(new_pin_exit_msg), new_pin_exit_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
		self.stdscr.refresh()
		self.stdscr.getch()
	# END __change_pin_screen

	def __recipe_screen(self):
		# __atm.get_recipe
		self.stdscr.clear()
		recipe_msg = self.__atm.get_recipe() # List of lines of messages
		middle_y = (self.height // 2) - len(recipe_msg)
		for msg in recipe_msg:
			self.stdscr.addstr(middle_y, self.__get_middle_x(msg), msg, self.__terminal_color | curses.A_BOLD | curses.A_ITALIC)
			middle_y += 1
		# END for
		recipe_exit_msg = "Press any key to get BACK"
		self.stdscr.addstr(middle_y + 1, self.__get_middle_x(recipe_exit_msg), recipe_exit_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
		self.stdscr.refresh()
		self.stdscr.getch()
		# pass
	# END __recipe_screen

	"""
		gets a string and returns the x coordinate to center it
	"""
	def __get_middle_x(self, text: str) -> int:
		return (self.width - len(text)) // 2
	# END __get_middle_x

	"""
		gets uknown amount of line numbers (int), and clears each line 
	"""
	def __clear_line(self, *lines: int):
		for line in lines:
			self.stdscr.move(line, 0)
			self.stdscr.clrtoeol()
		# END for
	# END __clear_line

	def __del__(self):
		# Clean up the curses window
		curses.endwin()
	# END __del__
# END Menu

def main(stdscr):
	menu = Menu(stdscr, "ATM System")
	menu.start()
# END main

if __name__ == "__main__":
	curses.wrapper(main)