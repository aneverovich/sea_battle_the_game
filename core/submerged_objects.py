from core.functions.conversion import convert_coordinates


class UndefinedSubmergedObject():
    """Any object that can be interacted with within the game board.

    Undefined submerged object - is the same as UFO but for objects in water.
    https://en.wikipedia.org/wiki/Unidentified_submerged_object
    """

    def __init__(self, code):
        self.level = None
        self.coordinates = []
        self.code = code


class Bomb(UndefinedSubmergedObject):

    def __init__(self, code):
        super().__init__(code)
        self.type = 'Bomb'

    def __str__(self):
        coordinates = convert_coordinates(self.coordinates)
        return f"Bomb: {self.code} | Level: {self.level} | Coordinate: {coordinates}"
