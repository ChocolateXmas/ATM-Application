#!/usr/bin/env python3

import curses
from atm import Atm



def main(stdscr):
	i = 0
	while True:
		curses.start_color()
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
		stdscr.bkgd(' ', curses.color_pair(1))
		stdscr.clear()
		height, width = stdscr.getmaxyx()
		title = f"Atm Application {i}"
		i += 1
		title_y = height // 2
		title_x = (width - len(title)) // 2
		stdscr.addstr(title_y, title_x, title, curses.color_pair(1) | curses.A_BOLD)
		win = curses.newwin(12, 40, 20, 20)
		win.box()
		win.addstr(5, 10, "Inside a box!", curses.color_pair(1))
		win.refresh()
		stdscr.refresh()
		stdscr.getch()
	# END while
# END main

if __name__ == "__main__":
	curses.wrapper(main)