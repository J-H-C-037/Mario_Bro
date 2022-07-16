
class Clouds:
    def __init__(self, x: int, y: int):
        """ This method creates the Cloud object
        @param x the starting x of the Cloud
        @param y the starting y of the Cloud"""
        self.x = x
        self.y = y
        self.sprite = [2, 0, 80, 64, 40, x, y]  # img bank, x and y of the image bank, width, height, x, y and colkey

class Bushes:
    def __init__(self, x: int, y: int):
        """ This method creates the Bushes object
        @param x the starting x of the Bushes
        @param y the starting y of the Bushes"""
        self.x = x
        self.y = y
        self.sprite = [2, 0, 216, 48, 32, x, y]  # img bank, x and y of the image bank, width, height, x, y and colkey

