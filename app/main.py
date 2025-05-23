#!/usr/bin/env python3

import curses
from curses.textpad import Textbox, rectangle
from scripts.atm.atm import Atm
from scripts.menu.menu import Menu

def main(stdscr):
	menu = Menu(stdscr, "ATM System")
	menu.start()
	menu.end()
# END main

if __name__ == "__main__":
	curses.wrapper(main)