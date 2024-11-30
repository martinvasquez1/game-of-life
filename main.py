import random
import time

SIZE = 10


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


def death_conditions(map, size):
    for i in range(size):
        for j in range(size):
            cell_pos = [i, j]
            live_neighbors = get_live_neighbors(cell_pos, map)

            overpopulation_death = live_neighbors > 3
            loneliness_death = live_neighbors < 2

            if overpopulation_death or loneliness_death:
                map[i][j] = 0

    return map


def reproduction(map, size):
    pass


def main():
    map = generate_map(SIZE)

    while True:
        map = death_conditions(map, SIZE)
        # map = reproduction(map, SIZE)

        print(map)
        time.sleep(2)


if __name__ == "__main__":
    main()
