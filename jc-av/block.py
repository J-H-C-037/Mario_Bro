class Ground:
    def __init__(self, x: int, y: int):
        """ This method creates the Ground object
        @param x the starting x of the Ground
        @param y the starting y of the Ground"""
        self.x = x
        self.y = y
        self.sprite = [2, 32, 0, 16, 16, x, y]  # img bank, x and y of the image bank, width, height, x, y and colkey


class Brick:
    def __init__(self, x: int, y: int):
        """ This method creates the Breakable bricks object
        @param x the starting x of the Breakable bricks
        @param y the starting y of the Breakable bricks"""
        self.x = x
        self.y = y

        self.sprite = [2, 0, 0, 16, 16, x, y]  # img bank, x and y of the image bank, width, height, x, y and colkey


class Question:
    def __init__(self, x: int, y: int):
        """ This method creates the question object
        @param x the starting x of the question
        @param y the starting y of the question"""

        self.x = x
        self.y = y
        self.sprite = [2, 0, 24, 16, 16, x, y, 0,24]  # img bank, x and y of the image bank, width, height, x, y and colkey


class Tunnel:
    def __init__(self, x: int, y: int):
        """ This method creates the tunnel object
        @param x the starting x of the tunnel
        @param y the starting y of the tunnel"""
        self.x = x
        self.y = y
        self.sprite = [2, 32, 24, 24, 32, x, y]  # img bank, x and y of the image bank, width, height, x, y and colkey


class BigTunnel:
    def __init__(self, x: int, y: int):
        """ This method creates the tunnel object
        @param x the starting x of the tunnel
        @param y the starting y of the tunnel"""
        self.x = x
        self.y = y

        self.sprite = [2, 32, 24, 24, 40, x, y]  # img bank, x and y of the image bank, width, height, x, y and colkey


class BiggerTunnel:
    def __init__(self, x: int, y: int):
        """ This method creates the tunnel object
        @param x the starting x of the tunnel
        @param y the starting y of the tunnel"""
        self.x = x
        self.y = y

        self.sprite = [2, 32, 24, 24, 48, x, y]  # img bank, x and y of the image bank, width, height, x, y and colkey


class Stairs4:
    def __init__(self, x: int, y: int):
        """ This method creates the tunnel object
        @param x the starting x of the tunnel
        @param y the starting y of the tunnel"""
        self.x = x
        self.y = y

        self.sprite = [2, 120, 80, 16, 64, x, y]  # img bank, x and y of the image bank, width, height, x, y and colkey


class Stairs3:
    def __init__(self, x: int, y: int):
        """ This method creates the tunnel object
        @param x the starting x of the tunnel
        @param y the starting y of the tunnel"""
        self.x = x
        self.y = y
        self.sprite = [2, 120, 80, 16, 48, x, y]  # img bank, x and y of the image bank, width, height, x, y and colkey


class Stairs2:
    def __init__(self, x: int, y: int):
        """ This method creates the tunnel object
        @param x the starting x of the tunnel
        @param y the starting y of the tunnel"""
        self.x = x
        self.y = y

        self.sprite = [2, 120, 80, 16, 32, x, y]  # img bank, x and y of the image bank, width, height, x, y and colkey


class Stairs1:
    def __init__(self, x: int, y: int):
        """ This method creates the tunnel object
        @param x the starting x of the tunnel
        @param y the starting y of the tunnel"""
        self.x = x
        self.y = y

        self.sprite = [2, 120, 80, 16, 16, x, y]  # img bank, x and y of the image bank, width, height, x, y and colkey


class Stairs5:
    def __init__(self, x: int, y: int):
        """ This method creates the tunnel object
        @param x the starting x of the tunnel
        @param y the starting y of the tunnel"""
        self.x = x
        self.y = y

        self.sprite = [2, 72, 128, 16, 80, x, y]  # img bank, x and y of the image bank, width, height, x, y and colkey


class Stairs6:
    def __init__(self, x: int, y: int):
        """ This method creates the tunnel object
        @param x the starting x of the tunnel
        @param y the starting y of the tunnel"""
        self.x = x
        self.y = y

        self.sprite = [2, 120, 80, 16, 96, x, y]  # img bank, x and y of the image bank, width, height, x, y and colkey


class Stairs7:
    def __init__(self, x: int, y: int):
        """ This method creates the tunnel object
        @param x the starting x of the tunnel
        @param y the starting y of the tunnel"""
        self.x = x
        self.y = y

        self.sprite = [2, 120, 80, 16, 112, x, y]  # img bank, x and y of the image bank, width, height, x, y and colkey


class Stairs8:
    def __init__(self, x: int, y: int):
        """ This method creates the tunnel object
        @param x the starting x of the tunnel
        @param y the starting y of the tunnel"""
        self.x = x
        self.y = y

        self.sprite = [2, 120, 80, 16, 128, x, y]  # img bank, x and y of the image bank, width, height, x, y and colkey