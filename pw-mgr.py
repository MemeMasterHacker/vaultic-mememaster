#!/usr/bin/env python3
import curses, random, string, pyperclip

CHARSETS = {
    "Uppercase": string.ascii_uppercase,
    "Lowercase": string.ascii_lowercase,
    "Digits":    string.digits,
    "Symbols":   string.punctuation,
}

def generate(length, enabled):
    pool = "".join(v for k, v in CHARSETS.items() if enabled[k])
    return "".join(random.choices(pool, k=length)) if pool else ""

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    enabled = {k: True for k in CHARSETS}
    length, cursor, password = 16, 0, ""
    options = list(CHARSETS.keys())

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(1, 2, "=== Password Generator ===", curses.A_BOLD)
        stdscr.addstr(3, 2, f"Length: {length}  (← → to adjust)")

        for i, name in enumerate(options):
            mark = "[x]" if enabled[name] else "[ ]"
            attr = curses.color_pair(1) if cursor == i else curses.A_NORMAL
            stdscr.addstr(5 + i, 2, f"{mark} {name}", attr)

        stdscr.addstr(5 + len(options), 2, "[ ] Generate", curses.color_pair(1) if cursor == len(options) else curses.A_NORMAL)
        stdscr.addstr(5 + len(options) + 1, 2, "[ ] Copy to clipboard", curses.color_pair(1) if cursor == len(options) + 1 else curses.A_NORMAL)

        if password:
            stdscr.addstr(h - 3, 2, f"Password: {password}", curses.color_pair(2))

        stdscr.addstr(h - 1, 2, "↑↓ Navigate  ENTER Select  Q Quit")
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            cursor = (cursor - 1) % (len(options) + 2)
        elif key == curses.KEY_DOWN:
            cursor = (cursor + 1) % (len(options) + 2)
        elif key == curses.KEY_LEFT and cursor == len(options):
            pass
        elif key == curses.KEY_LEFT:
            length = max(1, length - 1)
        elif key == curses.KEY_RIGHT:
            length = min(128, length + 1)
        elif key in (curses.KEY_ENTER, 10):
            if cursor < len(options):
                enabled[options[cursor]] = not enabled[options[cursor]]
            elif cursor == len(options):
                password = generate(length, enabled)
            elif cursor == len(options) + 1 and password:
                pyperclip.copy(password)

curses.wrapper(main)

