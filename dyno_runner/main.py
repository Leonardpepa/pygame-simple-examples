from importlib.resources import path
import pygame
from sys import exit

pygame.init()
WIDTH, HEIGHT = 600, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dyno Runner")
clock = pygame.time.Clock()

dyno_images = {"idle": [], "jump": [], "run": []}
bg = pygame.transform.scale(pygame.image.load(f"png/bg.jpg").convert_alpha(), size = (600, 400))
for i in range(1, 11):
    dyno_images["idle"].append(pygame.transform.scale(pygame.image.load(f"png/Idle ({i}).png").convert_alpha(), size = (120, 100)))
    # dyno_images["dead"].append(pygame.image.load(f"png/Dead ({i}).png").convert_alpha())
    dyno_images["jump"].append(pygame.transform.scale(pygame.image.load(f"png/Jump ({i}).png").convert_alpha(), size = (120, 100)))
    if i <=8 :
        dyno_images["run"].append(pygame.transform.scale(pygame.image.load(f"png/Run ({i}).png").convert_alpha(), size = (120, 100)))



class Dyno(pygame.sprite.Sprite):
    animation_frame = 0
    GRAVITY = 0.5
    JUMP = 11
    y_vel = 0
    def __init__(self):
        super().__init__()
        self.images = dyno_images
        self.image = dyno_images["run"][0]
        self.rect = self.image.get_rect(bottomleft = (20, 350))
        self.state = "run"

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.jump()

    def gravity(self):
        self.y_vel += self.GRAVITY
        self.rect.y += self.y_vel
        if self.rect.bottom >= 350:
            self.rect.bottom = 350
            self.y_vel = 0
            self.state = "run"
    
    def jump(self):
        if self.rect.bottom >= 350:
            self.y_vel = -1 * self.JUMP
            self.state = "jump"
            self.animation_frame = 0
    
    def animate(self):
        if self.state == "jump":
            self.animation_frame += 0.25
        else:
            self.animation_frame += 0.15

        if int(self.animation_frame) > len(self.images[self.state]) - 1:
            self.animation_frame = 0

        self.image = self.images[self.state][int(self.animation_frame)]

    def update(self):
        self.input()
        self.gravity()
        super().update()
        self.animate()


dyno_group = pygame.sprite.GroupSingle()
dyno_group.add(Dyno())

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        

        SCREEN.blit(bg, (0, 0))
        dyno_group.update()
        dyno_group.draw(SCREEN)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()