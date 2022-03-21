def convert_coordinates(indexed_coordinates):
    coordinates = []
    for x in indexed_coordinates:
        coordinates.append(f"{'ABCDEFGHIJ'[x[1]]}:{x[0] + 1}")
    return coordinates
