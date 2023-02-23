from itertools import count
import pygame
import sys
import random
import os
import math
pygame.init()

WIDTH, HEIGHT = 800, 600

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Python")
radius = 15
wallW = 90
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (WIDTH, HEIGHT))
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
base_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha(), (WIDTH, 50))
pygame.mixer.init()
pygame.mixer.music.load(os.path.join("sounds", "flap.mp3"))
pygame.mixer.music.set_volume(0.6)

class Wall:
    color = "green"
    GAP = 190
    VEL = 4
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.opositY = self.y + self.h + self.GAP
        self.opositH = HEIGHT - (self.y + self.h + self.GAP)
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha(), (wallW, self.h)), 180)
        self.op_image = pygame.transform.scale(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha(), (wallW, self.opositH))
        self.top = self.h - self.image.get_height()
        self.bottom = self.h + self.GAP
    
    def __gt__(self, o):
        return self.x > o.x

    def draw(self, win):
        win.blit(self.op_image, (self.x, self.opositY))
        win.blit(self.image, (self.x, self.y))

        # pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))
        # pygame.draw.rect(win, self.color, (self.x, self.opositY, self.w, self.opositH))

    def move(self, lastWall):
        self.x -= self.VEL
        if self.x + self.w + self.GAP <= 0:
            self.__init__(lastWall.x + random.randint(250, 400), 0, wallW,  random.randint(60, HEIGHT - 65 - Wall.GAP))

class Ball:
    VEL = 10
    y_vel = 0
    GRAVITY = 0.8
    anim = 0
    count = 0
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        # self.image = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bird1.png")).convert_alpha(), (self.radius * 2, self.radius * 2 )) 
        self.image = bird_images[0]
    def move(self):
        if self.y_vel <= 8:
            self.y_vel += self.GRAVITY
        self.y += self.y_vel 
 
    
    def animate(self):
        if self.anim >= 19:
            self.anim = 0
            if self.count < len(bird_images) - 1:
                self.count += 1
            else:
                self.count = 0
            self.image = bird_images[self.count]
        else:
            self.anim += 1
        
    
    def jump(self):
        self.y_vel = -self.VEL 
        
    def collide(self, walls):
        base = pygame.mask.from_surface(base_img)
        bird_mask = pygame.mask.from_surface(self.image)
        if bird_mask.overlap(base, (-self.x, HEIGHT - 30  - round(self.y))):
            # if self.y + self.radius >= HEIGHT:
            sys.exit(0)
        
        # for wall in walls:
        #     if self.y - self.radius <= wall.y + wall.h and self.x  + self.radius >= wall.x and self.x <= wall.x + wall.w:
        #         sys.exit(0) 
        #     elif self.y + self.radius >= wall.opositY  and  self.x  + self.radius >= wall.x and self.x <= wall.x + wall.w:
        #         sys.exit(0)

        for wall in walls:
            bird_mask = pygame.mask.from_surface(self.image)
            top_mask = pygame.mask.from_surface(wall.image)
            bottom_mask = pygame.mask.from_surface(wall.op_image)
            top_offset = (wall.x - self.x, wall.top - round(self.y))
            bottom_offset = (wall.x - self.x, wall.bottom - round(self.y))
            b_point = bird_mask.overlap(bottom_mask, bottom_offset)
            t_point = bird_mask.overlap(top_mask,  top_offset)

            if t_point or b_point:
                print("true")
                sys .exit()



    def draw(self, win):
        self.animate()
        # pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        rotated_image = pygame.transform.rotate(self.image, math.radians(-self.y_vel * 180 ))
        new_rect = rotated_image.get_rect(center = self.image.get_rect(topleft = (self.x, self.y)).center)
        # win.blit(self.image, (self.x, self.y))
        win.blit(rotated_image, new_rect.topleft)
        

def generateWalls():
    walls = []
    for i in range(5):
        walls.append(Wall(WIDTH + i * 400 - wallW, 0, wallW, random.randint(60, HEIGHT - 65 - Wall.GAP)))
    return walls

def gameLogic(ball, walls):
    ball.move()
    for wall in walls:
        wall.move(max(walls))
    ball.collide(walls)

def draw(win, ball, walls):
    ball.draw(win)
    for wall in walls:
        wall.draw(win)

def update(clock): 
    clock.tick(60)
    pygame.display.flip()

def main():
    gameStarted = False
    running  = True
    clock = pygame.time.Clock()
    ball = Ball(100, HEIGHT // 2, radius, "red")
    walls = generateWalls()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        # win.fill("black")
        win.blit(bg_img, (0, 0))
        win.blit(base_img, (0, HEIGHT - 30))


        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            gameStarted = True
            pygame.mixer.music.play()
            ball.jump()
        
        if not gameStarted:
            draw(win, ball, walls) 
            update(clock)
            continue
            
        
        gameLogic(ball, walls)
        draw(win, ball, walls) 
        update(clock)

    pygame.quit()

if __name__ == "__main__":
    main()