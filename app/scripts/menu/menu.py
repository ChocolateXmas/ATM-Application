#!/usr/bin/env python3

import curses
from curses.textpad import Textbox, rectangle
from scripts.atm.atm import Atm

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

		self.__withdraw_amounts = [50, 100, 150, 300]
		"""
			self.__withdraw_options : dict()
			* -> 	(option: amount) ~ (str: int[amount] / str["Other"])
		"""
		# Dict comphrehension for options to withdraw ( 1 - 50, 2 - 100, etc ...)
		self.__withdraw_options = { str(option + 1) : (self.__withdraw_amounts[option] if option < len(self.__withdraw_amounts) else "Other")
									for option in range(0, len(self.__withdraw_amounts) + 1) }

		self.__running = True # Flag to control the main loop
	# END __init__

	def __display_title(self):
		# Display the title at the top center
		self.stdscr.addstr(self.__title_y, self.__title_x, self.__title, self.__terminal_color | curses.A_BOLD)
	# END __display_title	

	def __display_greet_title(self):
		self.stdscr.addstr(self.__greet_title_y, self.__greet_title_x, self.__greet_title, self.__terminal_color | curses.A_BOLD)
	# END __display_greet_title

	def start(self):
		# curses.curs_set(0)  # Hide cursor
		# self.stdscr.nodelay(True)  # Set non-blocking mode
		# self.stdscr.timeout(1)  # Timeout in milliseconds
		curses.start_color()

		# Set the background color
		self.stdscr.bkgd(' ', self.__terminal_color)
		self.stdscr.clear()

		while self.__running:
			# key = self.stdscr.getch()
			# if key == 27: # ESC key
			# 	self.end()
			# 	break
			# # END if
			# elif key == -1:
			# 	continue
			# else:
			self.stdscr.clear()
			self.__login()
			self.stdscr.clear()
			self.__menu_options()
			# END else
		# END while
	# END start 	

	def end(self):
		# Clean up the curses window
		curses.endwin()
	# END end
	
	"""
		Gets the wanted Y-coordinate for Deposit input box location.
		formerElement:bool is True if we have a former element above the Deposit input box - that way the input box will be below it with an empty break line,
							  False otherwise.
		* Deposit amount can be only a multiplier of 20, 50, 100 !

		Returns:
			int: Wanted Deposit amount if casting was successful, otherwise returns 0.
	"""
	def __show_deposit_inputbox(self, desposit_y, formerElement=False) -> int:
		deposit_prompt = "Enter Deposit Amount: "
		max_deposit_length = 10
		desposit_y += 2 if formerElement else 0
		deposit_x = self.__get_middle_x(deposit_prompt + " " * max_deposit_length)
		# Input box for Deposit
		self.stdscr.addstr(desposit_y, deposit_x, deposit_prompt, self.__input_color)
		deposit_win = curses.newwin(1, max_deposit_length, desposit_y, deposit_x + len(deposit_prompt))
		curses.textpad.rectangle(self.stdscr, desposit_y - 1, deposit_x + len(deposit_prompt) - 1,
									desposit_y + 1, deposit_x + len(deposit_prompt) + max_deposit_length)
		self.stdscr.refresh()
		# Deposit amount value input is a string now, but will be converted to int later
		deposit_amount = ""
		while True:
			key = deposit_win.getch()
			if key in range(48, 58): # Check if the key is a digit (ASCII 48-57)
				if len(deposit_amount) < max_deposit_length - 1:
					deposit_amount += chr(key)
					deposit_win.addch(chr(key))
				# END if 
			# END if
			elif key == curses.KEY_BACKSPACE or key == 127: # Handle backspace
				if len(deposit_amount) > 0:
					deposit_amount = deposit_amount[:-1]
					y, x = deposit_win.getyx()
					deposit_win.delch(y, x - 1)
				# END if
			# END elif
			elif key == curses.KEY_ENTER or key == 10 or key == 13: # Enter key
				if len(deposit_amount) == 0:
					empty_deposit_amount_msg = "PIN must be 4 digits. Please try again."
					self.stdscr.addstr(desposit_y + 2, self.__get_middle_x(empty_deposit_amount_msg), empty_deposit_amount_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT | curses.A_UNDERLINE)
					self.stdscr.refresh()
				# END if
				break
			# END elif
		# END while
		self.__clear_line(desposit_y + 2)
		self.stdscr.refresh()
		try:
			return int(deposit_amount)
		except:
			return 0
	# END __show_deposit_inputbox
	
	"""
		Gets the wanted Y-coordinate for Withdraw input box location.
		formerElement:bool is True if we have a former element above the Withdraw input box - that way the input box will be below it with an empty break line,
							  False otherwise.
		* Withdraw amount can be only a multiplier of 20, 50, 100 !

		Returns:
			int: Wanted Withdraw amount if casting was successful, otherwise returns 0.
	"""
	def __show_withdraw_options(self, withdraw_y, formerElement=False) -> int:
		# This function assumes the options were already printed to the user, and now it's destiny it to only get the option to withdraw
		withdraw_prompt = "Choose Option: "
		withdraw_y += 2 if formerElement else 0
		withdraw_x = self.__get_middle_x(withdraw_prompt)
		other_amount_prompt = "Enter amount: "
		max_other_amount_length = 10
		other_y = withdraw_y + 2 # Y Coordinate for "Enter amount: " message
		other_x = self.__get_middle_x(other_amount_prompt + " " * max_other_amount_length)
		other_empty_amount_y = other_y + 2 # Y Coordinate for Empty Amount input message
		self.stdscr.addstr(withdraw_y, withdraw_x, withdraw_prompt, self.__terminal_color | curses.A_BOLD)
		self.stdscr.refresh()
		other_amount = ""
		selection_done = False # If Other amount was entered, end the outer while loop and return a value
		while not selection_done:
			chosen_option = self.stdscr.getch()
			if chr(chosen_option) in self.__withdraw_options.keys():
				if isinstance(self.__withdraw_options[ chr(chosen_option) ], int): # Means it's a number of NIS
					return self.__withdraw_options[ chr(chosen_option) ]
				# END if
				else: # "Other" amount to withdraw
					self.stdscr.addstr(other_y, other_x, other_amount_prompt, self.__terminal_color | curses.A_BOLD)
					other_win = curses.newwin(1, max_other_amount_length, other_y, other_x + len(other_amount_prompt))
					curses.textpad.rectangle(self.stdscr, other_y - 1, other_x + len(other_amount_prompt) - 1,
														  other_y +1 , other_x + len(other_amount_prompt) + max_other_amount_length + 1)
					self.stdscr.refresh()
					while True:
						key = other_win.getch()
						if key in range(48, 58): # Check if the key is a digit (ASCII 48-57)
							if len(other_amount) == 0 and chr(key) == '0': # disallow "0" as a first char of amount
								continue
							# END if
							elif len(other_amount) < max_other_amount_length - 1:
								other_amount += chr(key)
								other_win.addch( chr(key) )
							# END elif 
						# END if
						elif key == curses.KEY_BACKSPACE or key == 127: # Handle backspace
							if len(other_amount) > 0:
								other_amount = other_amount[:-1]
								y, x = other_win.getyx()
								other_win.delch(y, x - 1)
							# END if
						# END elif
						elif key == curses.KEY_ENTER or key == 10 or key == 13: # Enter key
							if len(other_amount) == 0: raise ValueError("Amount can't be empty")
							else: selection_done = True; break;
						# END elif
					# END while
				# END else
			# END if
			else:
				raise ValueError("No Option Selected!")
			# END if
		# END while
		try: 
			return int(other_amount)
		except ValueError: 
			return 0
	# END __show_withdraw_options

	"""
		Gets the Y-coordinate for USERNAME input box location.
		formerElement:bool is True if we have a former element above the USERNAME input box - that way the input box will be below it with an empty break line,
							False otherwise.

		Returns:
			str: The entered username as a string.
	"""
	def __show_username_inputbox(self, username_y, formerElement=False) -> str:
		username_prompt = "Enter Username: "
		max_username_length = 20
		username_y += 2 if formerElement else 0
		username_x = self.__get_middle_x(username_prompt + " " * max_username_length)
		# Username input box
		self.stdscr.addstr(username_y, username_x, username_prompt, self.__input_color)
		username_win = curses.newwin(1, max_username_length, username_y, username_x + len(username_prompt))
		curses.textpad.rectangle(self.stdscr, username_y - 1, username_x + len(username_prompt) - 1, username_y + 1, username_x + len(username_prompt) + max_username_length)
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

		return username
	# END __show_username_inputboxß

	"""
		Gets the Y-coordinate for PINCODE input box location.
		formerElement:bool is True if we have a former element above the PINCODE input box - that way the input box will be below it with an empty break line,
							  False otherwise.

		Returns:
			str: The entered PIN code as a string.
	"""
	def __show_pincode_inputbox(self, pin_y, formerElement=False) -> str:
		pin_prompt = "Enter PIN (4 digits): "
		max_pin_length = 14
		pin_y += 2 if formerElement else 0
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
			elif key == 27:
				self.end() # ESC key
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
	
	def __display_back_title(self):
		get_back_msg = "Press ESC to go BACK"
		self.stdscr.addstr(self.height - 1, self.__get_middle_x(get_back_msg), get_back_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
		self.stdscr.refresh()		
	# END __display_back_title

	def __login(self):
		while True:
			self.__display_title()
			self.__display_back_title()
			screen_y = self.height // 2 - 2 # Center the username input box
			username = self.__show_username_inputbox(screen_y)
			pin = self.__show_pincode_inputbox(screen_y , formerElement=True)

			# Check if the username and PIN are correct, and set the user info
			if not self.__atm.login(username, pin):
				login_failed_msg = "Invalid username/PIN. try again. (Enter to continue)"
				login_x = self.__get_middle_x(login_failed_msg)
				self.stdscr.addstr(screen_y + 4, login_x, login_failed_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT | curses.A_UNDERLINE)
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
		middle_y = (self.height // 2) - 3 # minus 3 because we have 3 lines to show (deposit_msg | error_msg), the input box, and one empty break line between them
		try:
			self.stdscr.clear() 
			deposit_msg = "How much would you like to Deposit?"
			self.stdscr.addstr(middle_y, self.__get_middle_x(deposit_msg), deposit_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
			self.stdscr.refresh()
			deposit_amount = self.__show_deposit_inputbox(middle_y, formerElement=True)
			self.__atm.deposit(deposit_amount)
			"""
				Raises a ValueError if the user is not logged in.
				Raises a ValueError if the amount is not a multiple of 20, 50 or 100.
				otherwise, Adds the amount to the user's balance.
			"""
			middle_y += 2 # 1 line for new pin msg + input box takes 2 lines + 1 empty break line
			self.__clear_line( *range(middle_y-1, middle_y + 1 + 1) )
			deposit_success_msg = f"{deposit_amount} NIS successfuly deposited!"
			self.stdscr.addstr(middle_y, self.__get_middle_x(deposit_success_msg), deposit_success_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
			self.stdscr.refresh()
			middle_y += 2
		# END try
		except ValueError as ve: 
			error_msg = str(ve)
			self.stdscr.clear()
			self.stdscr.addstr(middle_y, self.__get_middle_x(error_msg), error_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
			self.stdscr.refresh()
		# END except
		middle_y += 2 # 1 line for new pin msg + input box takes 2 lines + 1 empty break line
		deposit_exit_msg = "Press any key to get BACK"
		self.stdscr.addstr(middle_y, self.__get_middle_x(deposit_exit_msg), deposit_exit_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
		self.stdscr.refresh()
		self.stdscr.getch()
	# END __deposit_screen

	def __withdraw_screen(self):
		# __atm.withdraw
		withdraw_options_lines_amount = len(self.__withdraw_options)
		middle_y = (self.height // 2) - (withdraw_options_lines_amount + 2) # amount of withdraw options is the amount of rows needed + 1 for the withdraw_msg + 1 empty break line
		try:
			self.stdscr.clear() 
			withdraw_msg = "How much would you like to Withdraw?"
			self.stdscr.addstr(middle_y, self.__get_middle_x(withdraw_msg), withdraw_msg, self.__terminal_color | curses.A_BOLD)
			middle_y += 2
			for option, amount in self.__withdraw_options.items():
				line = f"{option} - {amount}"
				self.stdscr.addstr(middle_y, self.__get_middle_x(line), line, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
				middle_y += 1
			# END for
			self.stdscr.refresh()
			withdraw_amount = self.__show_withdraw_options(middle_y, formerElement=True)
			self.__atm.withdraw(withdraw_amount)
			"""
				Raises a ValueError if the user is not logged in.
				Raises a ValueError if the amount is not a multiple of 20, 50 or 100.
				Raises a ValueError if the amount is greater than the user's balance.
				Otherwise, Withdraws the amount from the user's balance.
			"""
			# middle_y += 2 # 1 line for new pin msg + input box takes 2 lines + 1 empty break line
			# self.__clear_line( *range(middle_y-1, middle_y + 1 + 1) )
			# deposit_success_msg = f"{deposit_amount} NIS successfuly deposited!"
			# self.stdscr.addstr(middle_y, self.__get_middle_x(deposit_success_msg), deposit_success_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
			# self.stdscr.refresh()
			middle_y += 2
			withdraw_success_msg = f"{withdraw_amount} NIS successfuly withdrawed!"
			self.stdscr.addstr(middle_y, self.__get_middle_x(withdraw_success_msg), withdraw_success_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
			self.stdscr.refresh()
		# END try
		except ValueError as ve: 
			error_msg = str(ve)
			self.stdscr.clear()
			self.stdscr.addstr(middle_y, self.__get_middle_x(error_msg), error_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
			self.stdscr.refresh()
		# END except
		middle_y += 2 # 1 line for new pin msg + input box takes 2 lines + 1 empty break line
		deposit_exit_msg = "Press any key to get BACK"
		self.stdscr.addstr(middle_y, self.__get_middle_x(deposit_exit_msg), deposit_exit_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
		self.stdscr.refresh()
		self.stdscr.getch()
		pass
	# END __withdraw_screen

	def __balance_screen(self):
		# __atm.get_balance
		self.stdscr.clear()
		balance_msg = [ 
			"Your current balance: ", 
			f"{self.__atm.get_balance()} NIS"
		]
		middle_y = (self.height // 2) - len(balance_msg)
		for msg in balance_msg:
			self.stdscr.addstr(middle_y, self.__get_middle_x(msg), msg, self.__terminal_color | curses.A_BOLD | curses.A_ITALIC)
			middle_y += 1
		# END for
		balance_exit_msg = "Press any key to get BACK"
		self.stdscr.addstr(middle_y + 1, self.__get_middle_x(balance_exit_msg), balance_exit_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
		self.stdscr.refresh()
		self.stdscr.getch()
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

	def __change_pin_screen(self):
		middle_y = (self.height // 2) - 3 # minus 3 because we have 3 lines to show (new_pin_msg | error_msg), the input box, and one empty break line between them
		try:
			self.stdscr.clear() 
			new_pin_msg = f"Hello {str(self.__atm.get_user_name())}, Enter NEW PINCODE"
			self.stdscr.addstr(middle_y, self.__get_middle_x(new_pin_msg), new_pin_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
			self.stdscr.refresh()
			new_pin = self.__show_pincode_inputbox(middle_y , formerElement=True)
			self.__atm.change_pin(new_pin)
		# END try
		except ValueError as ve: 
			error_msg = str(ve)
			self.stdscr.clear()
			self.stdscr.addstr(middle_y, self.__get_middle_x(error_msg), error_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
			self.stdscr.refresh()
		# END except
		middle_y += 4 # 1 line for new pin msg + input box takes 2 lines + 1 empty break line
		new_pin_exit_msg = "PINCODE changed succesfuly! Press any key to get BACK"
		self.stdscr.addstr(middle_y + 2, self.__get_middle_x(new_pin_exit_msg), new_pin_exit_msg, self.__terminal_color | curses.A_BOLD | curses.A_STANDOUT)
		self.stdscr.refresh()
		self.stdscr.getch()
	# END __change_pin_screen

	def __recipe_screen(self):
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
