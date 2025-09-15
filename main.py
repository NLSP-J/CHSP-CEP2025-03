import pygame as pg
import random, time
pg.init()
clock = pg.time.Clock()
import asyncio

red = (255, 0, 0)

lives = 3

win_width = 1100
win_height = 700
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('MINECRAFT 1.25')

font = pg.font.Font(None, 30)
speed = 10
score = 1
running = True

life_size = 70
life_data = []
life = pg.image.load('./assets/images/life_apple.jfif')
life = pg.transform.scale(life, (life_size, life_size))

player_size = 70
player_pos = [win_width / 2, win_height - player_size]  # 400, 600-40
player_image = pg.image.load('./assets/images/Camman18.png')
player_image = pg.transform.scale(player_image, (player_size, player_size))  # 40,40

obj_size = 70
obj_data = []     # List to store object positions and their images
obj = pg.image.load('./assets/images/NetSwordNoBack.png')
obj = pg.transform.scale(obj, (obj_size, obj_size))



bg_image = pg.image.load('./assets/images/MCBG.jpg')
bg_image = pg.transform.scale(bg_image, (win_width, win_height))


def create_object(obj_data):
    if len(obj_data) < 10 and random.random() < 0.1:            
        x = random.randint(0, win_width - obj_size)
        y = 0                                        
        obj_data.append([x, y, obj])

def create_life(life_data):
    if len(life_data) < 2 and random.random() < 0.01:
        x = random.randint (0, win_width - life_size)
        y = 0
        life_data.append([x,y,life])


def update_objects(obj_data):
    global score, obj_size

    for object in obj_data:
        x, y, image_data = object
        if y < win_height:
             y += speed
             object[1] = y
             screen.blit(image_data, (x, y))
        else:
            obj_data.remove(object)
            score += 1
            obj_size += 1
            
def update_life(life_data):

    global score
    global lives
   
    for life in life_data:
        x, y, image_data = life
        if y < win_height:
            y += speed
            life[1] = y
            screen.blit(image_data, (x, y))
        else:
            life_data.remove(life)
       


def collision_check(obj_data, player_pos, life_data):
    global running, lives
    for object in obj_data:
        x, y, image_data = object
        player_x, player_y = player_pos[0], player_pos[1]
        obj_rect = pg.Rect(x, y, obj_size, obj_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(obj_rect):
            lives -= 1
            obj_data.remove(object)
            if lives == 0:
                running = False
                break
    for life in life_data:
        x, y, image_data = life
        player_x, player_y = player_pos[0], player_pos[1]
        life_rect = pg.Rect(x, y, obj_size, obj_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(life_rect):
            life_data.remove(life)
            lives += 1
            life_rect = pg.Rect(x, y, life_size, life_size)
           
async def main():
    global running, player_pos, bg_image
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys_pressed=pg.key.get_pressed()
        if keys_pressed[pg.K_LEFT]and player_pos[0] > 0:
            player_pos[0] -=10
        if keys_pressed[pg.K_RIGHT] and player_pos[0] < win_width - player_size:
            player_pos[0] += 10

        screen.blit(bg_image, (0, 0))
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        text = f'Score: {score}'
        text = font.render(text, 10, red)
        screen.blit(text, (win_width - 200, win_height - 40))

        text = f'Lives: {lives}'
        text = font.render(text, 10, red)
        screen.blit(text, (win_width - 200, win_height - 60))


        create_object(obj_data)
        update_objects(obj_data)
        collision_check(obj_data, player_pos, life_data)
        create_life(life_data)
        update_life(life_data)
        
        if lives == 0:
            bg_image = pg.image.load('C:/MyFiles/pyproj/pygame_env/CHSP/Weihan Zhai/gameover.jpg')
            bg_image = pg.transform.scale(bg_image, (win_width, win_height))
            text = f'Score: {score}'
            text = font.render(text, 10, red)
            screen.blit(bg_image, (0, 0))
            screen.blit(text, (win_width // 2, win_height // 2 + 200))
            pg.display.flip()
            time.sleep(2)
            running = False

        clock.tick(30)
        pg.display.flip()
        await asyncio.sleep(0)

    pg.quit()
    


asyncio.run(main())