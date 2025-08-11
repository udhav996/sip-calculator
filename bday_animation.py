import curses
import time
from typing import List, Tuple


CAKE_ART_TOP = [
    "                .-''''-.               ",
    "              .'   _    `.             ",
    "             /    (_)     \\            ",
    "            |  .-.___.-.   |            ",
    "            | (  '   `  )  |            ",
    "            |  `-.___.-'   |            ",
    "            |               |           ",
    '            |   .-""""-.   |           ',
    "            |  /  _  _  \\  |           ",
    "            |  | (_)(_) |  |           ",
    "            |  |   /\\   |  |           ",
    "            |  |  /__\\  |  |           ",
    "            |  \\       /  |           ",
    "            |   `-.___-'   |           ",
    "            |               |           ",
    "            '.___..___..__.'           ",
]

# A larger cake that will be revealed top-to-bottom at the end
FINAL_CAKE_ART = [
    "                           .-''''''-.                           ",
    "                        .-'  _      _`-.                        ",
    "                      .'   _(_)    (_)_  `.                      ",
    "                     /    (_)  .-.  (_)   \\                     ",
    "                    ;        .(   ).       ;                    ",
    "                    |         `-.-'        |                    ",
    '                    |    .-"""-. .-"""-.   |                    ',
    "                    |   /  _  _ V _  _  \\  |                    ",
    "                    |   | (_)(_)|(_)(_) |  |                    ",
    "                    |   |   /\\  |  /\\   |  |                    ",
    "                    |   |  /__\\ | /__\\  |  |                    ",
    "                    |   \\       |       /  |                    ",
    "                    |    `-.___.-^-.___-'   |                    ",
    "                    |                       |                    ",
    "                    |   .---------------.   |                    ",
    "                    |   |###############|   |                    ",
    "                    |   |###############|   |                    ",
    "                    |   |###############|   |                    ",
    "                    |   |###############|   |                    ",
    "                    |___'---------------'___|                    ",
    '                 .-"_________________________"-.                 ',
    "               .'______________________________`.               ",
    "              /__________________________________\\              ",
]

WORDS = ["Happy", "Birthday", "to", "Dear", '"Manoj sir"']

TYPE_DELAY = 0.06
MOVE_DELAY = 0.03
REVEAL_DELAY = 0.05


def draw_centered_text(stdscr: "curses._CursesWindow", y: int, text: str, color: int = 0) -> None:
    height, width = stdscr.getmaxyx()
    x = max(0, (width - len(text)) // 2)
    if 0 <= y < height:
        stdscr.addstr(y, x, text[: max(0, width - x)], curses.color_pair(color))


def draw_art_centered(stdscr: "curses._CursesWindow", top_y: int, art: List[str], color: int = 0) -> Tuple[int, int]:
    height, width = stdscr.getmaxyx()
    art_width = max(len(line) for line in art)
    left_x = max(0, (width - art_width) // 2)
    for idx, line in enumerate(art):
        y = top_y + idx
        if 0 <= y < height:
            stdscr.addstr(y, left_x, line[: max(0, width - left_x)], curses.color_pair(color))
    return top_y, left_x


def ensure_size(stdscr: "curses._CursesWindow") -> None:
    height, width = stdscr.getmaxyx()
    min_h = 35
    min_w = 90
    if height < min_h or width < min_w:
        stdscr.clear()
        msg1 = "Please enlarge the terminal window."
        msg2 = f"Required at least {min_w}x{min_h}, current is {width}x{height}."
        draw_centered_text(stdscr, height // 2 - 1, msg1, 2)
        draw_centered_text(stdscr, height // 2 + 1, msg2, 2)
        stdscr.refresh()
        while True:
            time.sleep(0.25)
            h2, w2 = stdscr.getmaxyx()
            if h2 >= min_h and w2 >= min_w:
                break


def animate_typewriter(stdscr: "curses._CursesWindow", y: int, word: str, color: int = 0) -> None:
    for i in range(1, len(word) + 1):
        stdscr.timeout(0)
        draw_centered_text(stdscr, y, word[:i], color)
        stdscr.refresh()
        time.sleep(TYPE_DELAY)


def redraw_frame(
    stdscr: "curses._CursesWindow",
    cake_top_y: int,
    typed_words: List[Tuple[str, int, int]],
    typing_line_y: int,
    current_typing_text: str,
) -> None:
    stdscr.erase()
    draw_art_centered(stdscr, cake_top_y, CAKE_ART_TOP, 3)
    for text, y, color in typed_words:
        draw_centered_text(stdscr, y, text, color)
    if current_typing_text:
        draw_centered_text(stdscr, typing_line_y, current_typing_text, 6)
    stdscr.refresh()


def animate_move_up(
    stdscr: "curses._CursesWindow",
    cake_top_y: int,
    typed_words: List[Tuple[str, int, int]],
    word_index: int,
    target_y: int,
    typing_line_y: int,
) -> None:
    while typed_words[word_index][1] > target_y:
        text, y, color = typed_words[word_index]
        typed_words[word_index] = (text, y - 1, color)
        redraw_frame(stdscr, cake_top_y, typed_words, typing_line_y, "")
        time.sleep(MOVE_DELAY)


def reveal_art_top_to_bottom(
    stdscr: "curses._CursesWindow",
    top_y: int,
    art: List[str],
    color: int = 5,
) -> None:
    height, width = stdscr.getmaxyx()
    art_width = max(len(line) for line in art)
    left_x = max(0, (width - art_width) // 2)
    for idx, line in enumerate(art):
        y = top_y + idx
        if 0 <= y < height:
            stdscr.addstr(y, left_x, line[: max(0, width - left_x)], curses.color_pair(color))
            stdscr.refresh()
            time.sleep(REVEAL_DELAY)


def run(stdscr: "curses._CursesWindow") -> None:
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)
    curses.init_pair(3, curses.COLOR_MAGENTA, -1)
    curses.init_pair(4, curses.COLOR_CYAN, -1)
    curses.init_pair(5, curses.COLOR_GREEN, -1)
    curses.init_pair(6, curses.COLOR_RED, -1)

    ensure_size(stdscr)
    stdscr.erase()

    height, width = stdscr.getmaxyx()

    cake_top_y = 2
    draw_art_centered(stdscr, cake_top_y, CAKE_ART_TOP, 3)

    area_top_after_cake = cake_top_y + len(CAKE_ART_TOP) + 1
    typing_line_y = area_top_after_cake + 8

    typed_words: List[Tuple[str, int, int]] = []

    stdscr.refresh()
    time.sleep(0.6)

    target_start_y = area_top_after_cake + 1

    for idx, word in enumerate(WORDS):
        redraw_frame(stdscr, cake_top_y, typed_words, typing_line_y, "")
        time.sleep(0.2)

        current_text = ""
        for i in range(1, len(word) + 1):
            current_text = word[:i]
            redraw_frame(stdscr, cake_top_y, typed_words, typing_line_y, current_text)
            time.sleep(TYPE_DELAY)

        typed_words.append((word, typing_line_y, 4 if idx % 2 == 0 else 2))
        redraw_frame(stdscr, cake_top_y, typed_words, typing_line_y, "")

        target_y = target_start_y + idx
        animate_move_up(stdscr, cake_top_y, typed_words, len(typed_words) - 1, target_y, typing_line_y)
        time.sleep(0.2)

    stdscr.erase()
    draw_art_centered(stdscr, cake_top_y, CAKE_ART_TOP, 3)
    for i, (text, y, color) in enumerate(typed_words):
        draw_centered_text(stdscr, y, text, color)
    stdscr.refresh()
    time.sleep(0.8)

    overlay_top = area_top_after_cake - 1
    reveal_art_top_to_bottom(stdscr, overlay_top, FINAL_CAKE_ART, 5)

    draw_centered_text(stdscr, height - 2, "Press q to quit", 1)
    stdscr.refresh()

    stdscr.nodelay(True)
    start_time = time.time()
    while True:
        ch = stdscr.getch()
        if ch in (ord('q'), ord('Q')):
            break
        if time.time() - start_time > 20:
            break
        time.sleep(0.05)


if __name__ == "__main__":
    curses.wrapper(run)