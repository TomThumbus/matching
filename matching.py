import pygame
from gobjects import Tile
from random import randint

#initalize pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((500,500))

# title and icon
pygame.display.set_caption("matching game")

#colors
YELLOW = (255,255,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (25,25,25)

COLORS = [YELLOW, RED, GREEN, BLUE, GREY]

def randl(lyst):
    return randint(0,len(lyst) - 2)

def placeTile(tile, col, row_count):
    i = (col * (tile.width + 5)) + 100
    j = (row_count * (tile.height + 5)) + 100
    tile.setRect(pygame.Rect(i, j, tile.width, tile.height))
    if tile.color == 7:
        pygame.draw.rect(screen, (0,0,0), tile.rect)
    else:
        pygame.draw.rect(screen, COLORS[tile.color], tile.rect)

def placeSelected(selected, mousecoords):
    if selected == "nyet":
        pass
    else:
        pygame.draw.rect(screen, COLORS[selected.color], (mousecoords[0], mousecoords[1], selected.width, selected.height), 2)

def drawTiles(tiles):
    row_count = 0
    col_max = 7
    col = 0
    for tile in tiles:
        if col > col_max:
            row_count += 1
            col = 0
        #print(tiles.index(tile), col, row_count)
        placeTile(tile, col, row_count)
        col += 1

def checkTiles(selected, tiles):
    checked = []
    #tile to right = tiles[indexof_tile + 1] unless indexof_tile == 7,15,23,31,39,47,55,63
    #tile to left = tiles[indexof_tile - 1] unless indexof_tile == 0,8,16,24,32,40,48,56
    #tile above = tiles[indexof_tile - 8] unless indexof_tile == 0,1,2,3,4,5,6,7
    #tile below = tiles[indexof_tile + 8] unless indexof_tile == 56,57,58,59,60,61,62,63
    #only black out longest contiguous string of matching tiles
    length = 0
    indexof_right_tile, indexof_left_tile, indexof_up_tile, indexof_down_tile = None,None,None,None
    indexof_tile = tiles.index(selected)
    if indexof_tile not in (7,15,23,31,39,47,55,63):
        indexof_right_tile = indexof_tile + 1
    if indexof_tile not in (0,8,16,24,32,40,48,56):
        indexof_left_tile = indexof_tile - 1
    if indexof_tile not in (0,1,2,3,4,5,6,7):
        indexof_up_tile = indexof_tile - 8
    if indexof_tile not in (56,57,58,59,60,61,62,63):
        indexof_down_tile = indexof_tile + 8
    print(f"{indexof_tile},r {indexof_right_tile},l {indexof_left_tile},u {indexof_up_tile},d {indexof_down_tile}")

def checkRight(selected, tiles, length):
    right_ends = (7,15,23,31,39,47,55,63)
    tile_origin = tiles.index(selected)
    leg = length
    if tile_origin in right_ends:
        return leg
    elif selected.color != tiles[tile_origin + 1].color:
        return leg
    else:
        result = checkRight(tiles[tile_origin + 1], tiles, leg + 1)
        return result


def gl():
    tiles = []
    new_tiles = []
    max_tiles = 64
    for i in range(0, max_tiles):
        tiles.append(Tile(randl(COLORS)))
    tiles[0].color = 4

    #game loop
    running = True
    counter = 0
    selectedTile = "nyet"
    coords = pygame.mouse.get_pos()
    while running:

        #fills the background
        screen.fill((14,14,14))
        #draw box around tiles
        pygame.draw.rect(screen, (255,255,255), (91, 91, 291, 291), 4)
        #draw tiles on screen
        drawTiles(tiles)
        #place selected tile
        placeSelected(selectedTile, coords)
        #update mouse position
        coords = pygame.mouse.get_pos()
        #check tiles
        #checkTiles(tiles)
        #catch and handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("mouse button down")
                #select a tile
                coords = pygame.mouse.get_pos()
                print("coords: ", coords)
                if coords[0] < 99 or coords[0] > 377 or coords[1] < 99 or coords[1] > 377:
                    print("mouse out of bounds")
                else:
                    for tile in tiles:
                        if selectedTile == "nyet":
                            if tile.color != 4:
                                if tile.rect.collidepoint(coords):
                                    print(tiles.index(tile), " collided")
                                    print("length below")
                                    print(checkRight(tile, tiles, 1))
                                    selectedTile = Tile(tile.color)
                                    selectedTile.setRect(tile.rect)
                                    tile.color = 4
            elif event.type == pygame.MOUSEBUTTONUP:
                #place selected tile
                print("mouse button up")
                coords = pygame.mouse.get_pos()
                if coords[0] < 99 or coords[0] > 377 or coords[1] < 99 or coords[1] > 377:
                    print("mouse out of bounds")
                else:
                    for tile in tiles:
                        if selectedTile != "nyet":
                            if tile.color == 4:
                                if tile.rect.collidepoint(coords):
                                    print(tiles.index(tile), " collided")
                                    tile.color = selectedTile.color
                                    tile.setRect(selectedTile.rect)
                                    print(f"tile {tiles.index(tile)} replaced with {selectedTile.color}")
                                    selectedTile = "nyet"
            #debug dump key
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    # debug message
                    print('### Debug dump ###')
                    
                    if selectedTile != "nyet":
                        z = selectedTile.color
                    else:
                        z = "tile not selected"
                    debug_tiles = ""    
                    for tile in tiles:
                        if tile.rect.collidepoint(coords):
                           debug_tiles += f"{str(tiles.index(tile))}, {str(tile.color)} "
                    pos = pygame.mouse.get_pos()
                    s = f"""
                        selectedTile: {selectedTile}
                        mousepos: {pos}
                        selectedColor: {z}
                        selected:
                        {debug_tiles}
                    """
                    print(s)
                    print('### End Debug  ###')

        #pygame.time.delay(200)
        pygame.display.flip()

    
gl()