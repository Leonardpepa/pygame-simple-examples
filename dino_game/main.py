import pygame

pygame.init()

WIDTH, HEIGHT = 800, 300
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")


class Dino(pygame.rect.Rect):
    VEL = 5
    JUMP = 10
    GRAVITY = 0.7
    
    def __init__(self, x, y, w, h, color):
        super().__init__((x, y, w, h))
        self.color = color
        self.y_vel = 0
        self.vertical_direction = "D"
        self.can_jump = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)
    
    def collide_with_grounds(self, grounds):
        collided = False
        for g in grounds:
            if self.colliderect(g):
                if self.vertical_direction == "D":
                    self.y_vel = 0
                    self.y = g.top - self.h
                    collided = True

        self.can_jump = collided

    def collide_with_enemys(self, enemys):
        for e in enemys:
            if self.colliderect(e):
                return True
        
        return False
                

    def gravity(self):
        self.y_vel += self.GRAVITY
        self.y += self.y_vel
        if self.y_vel >= 0: self.vertical_direction = "D"


    def jump(self):
        if self.can_jump:
            self.y_vel = -1 * self.JUMP
            self.vertical_direction = "U"

    def move_right(self):
        self.x += self.VEL
    
    def move_left(self):
        self.x -= self.VEL
    

def update(clock: pygame.time.Clock):
    clock.tick(FPS)
    pygame.display.flip()

def main():
    run = True
    clock = pygame.time.Clock()
    dino = Dino(30, HEIGHT - 300, 30, 40, "black")
    grounds = [pygame.Rect(0, HEIGHT - 60, WIDTH, 60)]
    enemys = [pygame.Rect(WIDTH - 20, HEIGHT - 90, 15, 30)]
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        
        # if keys[pygame.K_LEFT]:
        #     dino.move_left()
        
        # if keys[pygame.K_RIGHT]:
        #     dino.move_right()
        
        if keys[pygame.K_SPACE]:
            dino.jump()
        


        screen.fill("white")
        dino.gravity()
        for e in enemys:
            e.left -= 7
            if e.left <= 0:
                e.left = WIDTH - 30

        dino.collide_with_grounds(grounds)
        if dino.collide_with_enemys(enemys):
            dino = Dino(30, HEIGHT - 300, 30, 40, "black")
            grounds = [pygame.Rect(0, HEIGHT - 60, WIDTH, 60)]
            enemys = [pygame.Rect(WIDTH - 20, HEIGHT - 90, 15, 30)]
            continue

        dino.draw(screen)
        for g in grounds:
            pygame.draw.rect(screen, "magenta", g)
        for e in enemys:
            pygame.draw.rect(screen, "red", e)
        update(clock)
    pygame.quit()


if __name__ == "__main__":
    main()