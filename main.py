import pygame
import sys
import random

pygame.init()



pygame.mixer.init()


mainTheme = 'main-theme.mp3'
anotherTheme = 'secondary-theme.mp3'


songList = [mainTheme, anotherTheme]


def selectRandomSong():
    return random.choice(songList)


def playSelectedSong(song):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(0, 0.0)


selectedSong = selectRandomSong()

MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)


playSelectedSong(selectedSong)


bite_sound = pygame.mixer.Sound('bite.mp3')



info = pygame.display.Info()
SW, SH = info.current_w, info.current_h  




BLOCK_SIZE = 50  
FONT = pygame.font.Font("font.ttf", BLOCK_SIZE * 2)
FONT_SMALL = pygame.font.Font("font.ttf", 30)  



screen = pygame.display.set_mode((SW, SH), pygame.FULLSCREEN)
pygame.display.set_caption("SnakeX")
clock = pygame.time.Clock()



icon = pygame.image.load('taskbar-icon.ico')  
pygame.display.set_icon(icon) 
icon = pygame.transform.scale(icon, (32, 32))




apple_image = pygame.image.load('apple.png')  
apple_image = pygame.transform.scale(apple_image, (BLOCK_SIZE, BLOCK_SIZE))  




death_sound = pygame.mixer.Sound('death.wav')



class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE  
        self.xdir = 1  
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)  
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]  
        self.dead = False



    def update(self):
        global apple


        for i in range(len(self.body) - 1, 0, -1): 
            self.body[i].x, self.body[i].y = self.body[i - 1].x, self.body[i - 1].y  

        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE

        self.body.insert(0, pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE))

        for square in self.body[1:]:  
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True  
        if self.head.x < 0 or self.head.x >= SW or self.head.y < 0 or self.head.y >= SH:
            self.dead = True

        if self.dead:
            death_sound.play()  
            self.reset()

        if self.head.x == apple.x and self.head.y == apple.y:
            apple = Apple()  
            bite_sound.play()  

        else:
            self.body.pop()

    def reset(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]  
        self.xdir = 1
        self.ydir = 0
        self.dead = False





class Apple:
    def __init__(self):
        self.x = int(random.randint(0, SW - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
    
    def update(self):

        screen.blit(apple_image, self.rect)




def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)




score = FONT.render("0", True, "white")
score_rect = score.get_rect(center=(SW / 2, SH / 20))




esc_message = FONT_SMALL.render("Press ESC to exit SnakeX!", True, "white")
esc_message_rect = esc_message.get_rect(center=(SW / 2, SH - 30))  




snake = Snake()
apple = Apple()




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MUSIC_END:
            selectedSong = selectRandomSong()
            playSelectedSong(selectedSong)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                snake.ydir = 1
                snake.xdir = 0

            elif event.key == pygame.K_UP:
                snake.ydir = -1
                snake.xdir = 0

            elif event.key == pygame.K_RIGHT:
                snake.ydir = 0
                snake.xdir = 1

            elif event.key == pygame.K_LEFT:
                snake.ydir = 0
                snake.xdir = -1

            elif event.key == pygame.K_s:
                snake.ydir = 1
                snake.xdir = 0

            elif event.key == pygame.K_w:
                snake.ydir = -1
                snake.xdir = 0

            elif event.key == pygame.K_d:
                snake.ydir = 0
                snake.xdir = 1

            elif event.key == pygame.K_a:
                snake.ydir = 0
                snake.xdir = -1
                
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    snake.update()

    screen.fill('black') 
    drawGrid()  
    apple.update() 

    score = FONT.render(f"{len(snake.body) + 1}", True, "white")
    screen.blit(score, score_rect)



    pygame.draw.circle(screen, "green", (snake.head.x + BLOCK_SIZE // 2, snake.head.y + BLOCK_SIZE // 2), BLOCK_SIZE // 2)



    for square in snake.body:
        pygame.draw.rect(screen, "green", square)

    screen.blit(esc_message, esc_message_rect)

    pygame.display.update() 

    clock.tick(12)