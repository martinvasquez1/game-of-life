import argparse
import os
import random
import sys
import time

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame


def parse_args():
    parser = argparse.ArgumentParser()

    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument(
        "-r", "--rows", type=int, default=25, help="Number of rows in the board"
    )
    parser.add_argument(
        "-c", "--cols", type=int, default=25, help="Number of columns in the board"
    )
    parser.add_argument(
        "-g",
        "--generations",
        type=int,
        default=600,
        help="Number of generations to simulate",
    )
    parser.add_argument(
        "-b",
        "--birth-probability",
        type=float,
        default="0.25",
        help="Initial probability of a cell being alive",
    )
    parser.add_argument(
        "-s", "--cell-size", type=int, default=20, help="Size of each cell in pixels"
    )
    parser.add_argument(
        "-w",
        "--wait-time",
        type=float,
        default=0.1,
        help="Wait time between generations in seconds",
    )

    args = parser.parse_args()
    return args


def init_pygame(dimensions, cell_size):
    rows = dimensions["rows"]
    columns = dimensions["columns"]
    screen_width = cell_size * columns
    screen_height = cell_size * rows

    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))

    return screen


def check_quit_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def generate_map(dimensions, birth_probability):
    map = []

    for i in range(dimensions["rows"]):
        map.append([])

        for _ in range(dimensions["columns"]):
            cell_state = 1 if random.random() < birth_probability else 0
            map[i].append(cell_state)

    return map


def is_position_out_of_range(cell_pos, dimensions):
    rows_size = dimensions["rows"] - 1
    cols_size = dimensions["columns"] - 1

    pos_x = cell_pos[0]
    pos_y = cell_pos[1]

    is_x_out = pos_x < 0 or pos_x > rows_size
    is_y_out = pos_y < 0 or pos_y > cols_size

    if is_x_out or is_y_out:
        return True

    return False


def get_live_neighbors(cell_pos, map, dimensions):
    amount_of_live_neighbors = 0

    neighbors_position = [
        [-1, 1],
        [0, 1],
        [1, 1],
        [-1, 0],
        [1, 0],
        [-1, -1],
        [0, -1],
        [1, -1],
    ]

    for neighbor_pos in neighbors_position:
        x = cell_pos[0] + (neighbor_pos[0] * -1)
        y = cell_pos[1] + (neighbor_pos[1] * -1)

        is_coord_out = is_position_out_of_range([x, y], dimensions)
        if is_coord_out:
            continue

        neighbor_cell = map[x][y]
        is_neighbor_alive = neighbor_cell == 1

        if is_neighbor_alive:
            amount_of_live_neighbors += 1

    return amount_of_live_neighbors


def apply_rules(map, dimensions):
    for i in range(dimensions["rows"]):
        for j in range(dimensions["columns"]):
            cell_pos = [i, j]
            live_neighbors = get_live_neighbors(cell_pos, map, dimensions)

            overpopulation_death = live_neighbors > 3
            loneliness_death = live_neighbors < 2

            if overpopulation_death or loneliness_death:
                map[i][j] = 0

            should_reproduce = live_neighbors == 3

            if should_reproduce:
                map[i][j] = 1

    return map


def draw_grid(screen, map, dimensions, cell_size):
    for row in range(dimensions["rows"]):
        for col in range(dimensions["columns"]):

            if map[row][col] == 1:
                color = (255, 255, 255)
            else:
                color = (0, 0, 0)

            pygame.draw.rect(
                screen, color, (col * cell_size, row * cell_size, cell_size, cell_size)
            )

    pygame.display.flip()


def main():
    args = parse_args()

    generations = args.generations
    wait_time = args.wait_time
    birth_probability = args.birth_probability
    cell_size = args.cell_size
    dimensions = {"rows": args.rows, "columns": args.cols}

    map = generate_map(dimensions, birth_probability)

    screen = init_pygame(dimensions, cell_size)
    screen.fill((255, 255, 255))

    running = True

    for generation in range(generations):
        check_quit_event()

        map = apply_rules(map, dimensions)
        draw_grid(screen, map, dimensions, cell_size)

        time.sleep(wait_time)


if __name__ == "__main__":
    main()
