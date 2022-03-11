def find_horizontal_oriented_ship_border_coordinates(coordinates):
    border_coordinates = []
    for line_index, cell_index in coordinates:
        if line_index > 0:
            border_coordinates.append((line_index - 1, cell_index))
            if line_index < 9:
                border_coordinates.append((line_index + 1, cell_index))
        if coordinates[0][1] > 0:
            border_coordinates.append((coordinates[0][0], coordinates[0][1] - 1))
            if coordinates[0][0] > 0:
                border_coordinates.append((coordinates[0][0] - 1, coordinates[0][1] - 1))
            if coordinates[0][0] < 9:
                border_coordinates.append((coordinates[0][0] + 1, coordinates[0][1] - 1))
        if coordinates[-1][1] < 9:
            border_coordinates.append((coordinates[-1][0], coordinates[-1][1] + 1))
            if coordinates[-1][0] > 0:
                border_coordinates.append((coordinates[-1][0] - 1, coordinates[-1][1] + 1))
            if coordinates[-1][0] < 9:
                border_coordinates.append((coordinates[-1][0] + 1, coordinates[-1][1] + 1))
    return border_coordinates


def find_vertical_oriented_ship_border_coordinates(coordinates):
    border_coordinates = []
    if coordinates[0][0] > 0:
        border_coordinates.append((coordinates[0][0] - 1, coordinates[0][1]))
        if coordinates[0][1] > 0:
            border_coordinates.append((coordinates[0][0] - 1, coordinates[0][1] - 1))
        if coordinates[0][1] < 9:
            border_coordinates.append((coordinates[0][0] - 1, coordinates[0][1] + 1))
    if coordinates[-1][0] < 9:
        border_coordinates.append((coordinates[-1][0] + 1, coordinates[-1][1]))
        if coordinates[-1][1] > 0:
            border_coordinates.append((coordinates[-1][0] + 1, coordinates[-1][1] - 1))
        if coordinates[-1][1] < 9:
            border_coordinates.append((coordinates[-1][0] + 1, coordinates[-1][1] + 1))
    if coordinates[0][1] > 0:
        for line_index, cell_index in coordinates:
            border_coordinates.append((line_index, cell_index - 1))
    if coordinates[0][1] < 9:
        for line_index, cell_index in coordinates:
            border_coordinates.append((line_index, cell_index + 1))
    return border_coordinates


def find_one_deck_ship_border_coordinates(coordinates):
    border_coordinates = []
    if coordinates[0] > 0:
        border_coordinates.append((coordinates[0] - 1, coordinates[1]))
        if coordinates[1] > 0:
            border_coordinates.append((coordinates[0] - 1, coordinates[1] - 1))
        if coordinates[1] < 9:
            border_coordinates.append((coordinates[0] - 1, coordinates[1] + 1))
    if coordinates[0] < 9:
        border_coordinates.append((coordinates[0] + 1, coordinates[1]))
        if coordinates[1] > 0:
            border_coordinates.append((coordinates[0] + 1, coordinates[1] - 1))
        if coordinates[1] < 9:
            border_coordinates.append((coordinates[0] + 1, coordinates[1] + 1))
    if coordinates[1] > 0:
        border_coordinates.append((coordinates[0], coordinates[1] - 1))
    if coordinates[1] < 9:
        border_coordinates.append((coordinates[0], coordinates[1] + 1))
    return border_coordinates
