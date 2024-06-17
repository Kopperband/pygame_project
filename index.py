import pygame
import sys

pygame.init()

# sets framerate
clock = pygame.time.Clock()
fps = 60

# sets screen dimensions and creates screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# load the sprite sheet
sprite_sheet = pygame.image.load("sprites.png").convert_alpha()
# removes the background from the sprite
sprite_sheet.set_colorkey((255, 255, 255))

# other images
bg_img = pygame.image.load("background.png")

# list to store extracted sprites and sprite dimensions
sprites = []
sprite_width = 16
sprite_height = 16


# method for extracting sprite from spritesheet
def extract_sprite(sheet, rect):
    # create a new surface with the size of the sprite
    sprite = pygame.Surface(
        (rect.width, rect.height), pygame.SRCALPHA, 32
    ).convert_alpha()
    # blit the sprite onto the new surface
    sprite.blit(sheet, (0, 0), rect)
    return sprite


# used for iterating through the spritesheet and appending the first row to a list
# margin is used to account for the gap between pictures in the spritesheet
margin = 9
for col in range(10):

    rect = pygame.Rect(
        margin + col * sprite_width,
        sprite_height + 18,
        sprite_width,
        sprite_height,
    )
    # extracts sprite and doubles its size
    sprite = pygame.transform.scale2x(
        extract_sprite(sprite_sheet, rect)
    ).convert_alpha()
    sprites.append(sprite)
    margin += 1


# define rectangle for the sprite (x, y, width, height)
sprite_rect = pygame.Rect(9, 9, 16, 16)


class Player:

    def __init__(self, x, y):
        self.sprite_counter = 0
        self.image = sprites[self.sprite_counter]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # counter for framerate
        self.counter = 0

    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 6

        # get keypresses
        key = pygame.key.get_pressed()

        # when each key is pressed it moves the sprite and goes through the proper animation sequence
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            dx -= 5
            self.counter += 1
            if self.counter >= walk_cooldown:
                if self.sprite_counter < 5 or self.sprite_counter >= 7:
                    self.sprite_counter = 5
                self.sprite_counter += 1
                self.counter = 0

        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            dx += 5
            self.counter += 1
            if self.counter >= walk_cooldown:
                if self.sprite_counter < 7 or self.sprite_counter >= 9:
                    self.sprite_counter = 7
                self.sprite_counter += 1
                self.counter = 0

        if key[pygame.K_DOWN] or key[pygame.K_s]:
            dy += 5
            self.counter += 1
            if self.counter >= walk_cooldown:
                if self.sprite_counter > 1:
                    self.sprite_counter = 0
                self.sprite_counter += 1
                self.counter = 0

        if key[pygame.K_UP] or key[pygame.K_w]:
            dy -= 5
            self.counter += 1
            if self.counter >= walk_cooldown:
                if self.sprite_counter <= 2 or self.sprite_counter >= 4:
                    self.sprite_counter = 2
                self.sprite_counter += 1
                self.counter = 0
        # if no keys pressed sprites faces down
        if not any(key):
            self.sprite_counter = 1

        # check for collision

        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        # passes the proper index to the sprites list and the blits it onto the screen
        self.image = sprites[self.sprite_counter]
        screen.blit(self.image, self.rect)


# def tile size
tile_size = 32


def draw_grid():
    for line in range(0, 26):
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (0, line * tile_size),
            (screen_width, line * tile_size),
        )
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (line * tile_size, 0),
            (line * tile_size, screen_height),
        )


class World:
    def __init__(self, data):
        self.tile_list = []

        # load in images
        tree_img = pygame.image.load("bush.png")
        water_img = pygame.image.load("water.png")
        dirt_img = pygame.image.load("dirt.png")

        # iterates through each item in the list that is the grid on the screen to create a list with the image and its rect where matching number is

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                # dirt tiles
                if tile == 0:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    # tree tiles
                if tile == 1:
                    img = pygame.transform.scale(tree_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                    # water tiles
                if tile == 2:
                    img = pygame.transform.scale(water_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    # goes through the tile_list and draws the tiles from the dictioi
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


world_data = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 2, 2, 2, 2, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 2, 2, 2, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 2, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
world = World(world_data)
player = Player(0, 0)
run = True
while run:
    clock.tick(fps)

    screen.blit(bg_img, (0, 0))
    world.draw()
    draw_grid()
    # updates player
    player.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()
