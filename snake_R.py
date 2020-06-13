import pygame
import random
import os

pygame.mixer.init()
pygame.init()

#colors
white = (255, 255, 255)
red = (255, 0, 0)
blue =(0, 0, 255)
green =(0,255,0)
black = (0, 0, 0)

# Creating Window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width,screen_height))
#Background Image
bgimg = pygame.image.load("s.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
#Welcome Image
bgimg2 = pygame.image.load("snakew.jpg")
bgimg2 = pygame.transform.scale(bgimg2, (screen_width, screen_height)).convert_alpha()
#Game over Image
bgimg3 = pygame.image.load("g_over.jpg")
bgimg3 = pygame.transform.scale(bgimg3, (screen_width, screen_height)).convert_alpha()


# Game Title
pygame.display.set_caption("Snake R")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(green)
        gameWindow.blit(bgimg2, (0, 0))
        text_screen("Welcome to Snake(R)", blue, 260,250)
        text_screen("Press Space Bar To Play ", red, 230, 300)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back2.mp3')
                    pygame.mixer.music.play()

                    gameloop()

        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    #check if highscore file exist
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        highscore = f.read()

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_veloci = 2
    snake_size = 30
    fps = 60
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            gameWindow.fill(black)
            gameWindow.blit(bgimg3, (0, 0))
            text_screen("Game Over! Press Enter To Continue", red, 100, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_veloci
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_veloci
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_veloci
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_veloci
                        velocity_x = 0

                    if event.key == pygame.K_x:
                       score += 10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<15 and abs(snake_y - food_y)<15:
                score += 10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 3
                init_veloci += float(0.1)



                pygame.mixer.music.load('beep.mp3')
                pygame.mixer.music.play()


                if score > int(highscore):
                    highscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg,(0,0))
            text_screen("Score: " + str(score) + "  Max: " + str(highscore), black, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()

            plot_snake(gameWindow, blue, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
