class TileColorError(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message


class Tile:
    def __init__(self, color):
        self.width = 30
        self.height = 30
        #int color 0=YELLOW 1=RED 2=GREEN 3=BLUE 4=GREY
        if color > 4 or color < 0:
            raise TileColorError(f"tile color is outside the bounds of the arrray (0-3): {color}")
        else:
            self.color = color
    
    def setRect(self, rect):
        self.rect = rect
