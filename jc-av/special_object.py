class Mushroom:
    def __init__(self, x: int, y: int):
        """ This method creates the Mushroom object
        @param x the starting x of the Ground
        @param y the starting y of the Ground"""
        self.x = x
        self.y = y
        self.sprite = [0, 0, 0, 16, 16, x, y]  # img bank, x and y of the image bank, width, height, x, y and colkey

class Coin:
    def __init__(self, x: int, y: int):
        """ This method creates the Coin object
        @param x the starting x of the Coin
        @param y the starting y of the Coin"""
        self.x = x
        self.y = y
        self.sprite = [2, 0, 48, 16, 16, x, y]  # img bank, x and y of the image bank, width, height, x, y




