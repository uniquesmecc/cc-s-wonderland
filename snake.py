import curses
import random

# Constants for game dimensions
HEIGHT = 20
WIDTH = 40

# Directions represented as coordinate offsets
DIRECTIONS = {
    curses.KEY_UP: (-1, 0),
    curses.KEY_DOWN: (1, 0),
    curses.KEY_LEFT: (0, -1),
    curses.KEY_RIGHT: (0, 1),
}


def main(stdscr):
    # Setup
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    # Initial snake and food
    snake = [(HEIGHT // 2, WIDTH // 2 + i) for i in range(3)]
    direction = curses.KEY_LEFT
    food = place_food(snake)
    score = 0

    while True:
        # Input
        key = stdscr.getch()
        if key in DIRECTIONS:
            # Prevent reversing directly
            new_direction = DIRECTIONS[key]
            curr_direction = DIRECTIONS.get(direction, (0, 0))
            if (curr_direction[0] + new_direction[0] != 0 or
                    curr_direction[1] + new_direction[1] != 0):
                direction = key

        head_y, head_x = snake[0]
        dy, dx = DIRECTIONS.get(direction, (0, 0))
        new_head = ((head_y + dy) % HEIGHT, (head_x + dx) % WIDTH)

        # Check collisions
        if new_head in snake:
            break  # Game over

        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = place_food(snake)
        else:
            snake.pop()

        # Draw
        stdscr.clear()
        for y, x in snake:
            stdscr.addstr(y, x, '#')
        fy, fx = food
        stdscr.addstr(fy, fx, '*')
        stdscr.addstr(0, 0, f'Score: {score}')
        stdscr.refresh()

    stdscr.nodelay(False)
    stdscr.addstr(HEIGHT // 2, WIDTH // 2 - 5, 'GAME OVER')
    stdscr.addstr(HEIGHT // 2 + 1, WIDTH // 2 - 8, f'Final Score: {score}')
    stdscr.getch()


def place_food(snake):
    while True:
        position = (random.randint(1, HEIGHT - 2), random.randint(1, WIDTH - 2))
        if position not in snake:
            return position


if __name__ == '__main__':
    curses.wrapper(main)
