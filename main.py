import argparse
import random
import sys
import time

import pygame

SIZE = 25

CELL_SIZE = 25
GRID_WIDTH = SIZE
GRID_HEIGHT = SIZE
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Grid Display")


def parse_args():
    parser = argparse.ArgumentParser()

    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument(
        "-r", "--rows", type=int, default=10, help="Number of rows in the board"
    )
    parser.add_argument(
        "-c", "--cols", type=int, default=10, help="Number of columns in the board"
    )
    parser.add_argument(
        "-g",
        "--generations",
        type=int,
        default=10,
        help="Number of generations to simulate",
    )

    args = parser.parse_args()
    return args


def generate_map(size):
    map = []

    for i in range(size):
        map.append([])

        for _ in range(size):
            cell_status = random.randint(0, 1)
            map[i].append(cell_status)

    return map


def is_position_out_of_range(cell_pos, map):
    size = len(map[0]) - 1

    pos_x = cell_pos[0]
    pos_y = cell_pos[1]

    is_x_out = pos_x < 0 or pos_x > size
    is_y_out = pos_y < 0 or pos_y > size

    if is_x_out or is_y_out:
        return True

    return False


def get_live_neighbors(cell_pos, map):
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

        coord_out = is_position_out_of_range([x, y], map)
        if coord_out:
            continue

        neighbor_cell = map[x][y]
        is_neighbor_alive = neighbor_cell == 1

        if is_neighbor_alive:
            amount_of_live_neighbors += 1

    return amount_of_live_neighbors


def apply_rules(map, size):
    for i in range(size):
        for j in range(size):
            cell_pos = [i, j]
            live_neighbors = get_live_neighbors(cell_pos, map)

            overpopulation_death = live_neighbors > 3
            loneliness_death = live_neighbors < 2

            if overpopulation_death or loneliness_death:
                map[i][j] = 0

            should_reproduce = live_neighbors == 3

            if should_reproduce:
                map[i][j] = 1

    return map


def draw_grid(map):
    for row in range(SIZE):
        for col in range(SIZE):

            if map[row][col] == 1:
                color = (255, 255, 255)
            else:
                color = (0, 0, 0)

            pygame.draw.rect(
                screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )


def main():
    args = parse_args()

    print(args.rows)

    map = generate_map(SIZE)
    screen.fill((255, 255, 255))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        map = apply_rules(map, SIZE)

        draw_grid(map)

        # Update display
        pygame.display.flip()

        time.sleep(0.1)


if __name__ == "__main__":
    main()


pygame.quit()
sys.exit()
