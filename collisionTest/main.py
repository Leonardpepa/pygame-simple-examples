from typing import List
import pygame

pygame.init()

WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Test")
FPS = 60
COLLITION_TOLL = 25

class Entity(pygame.Rect):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)


class Ground(Entity):
    pass

class Bullet(Entity):

    def __init__(self, x, y, w, h, color, movement):
        super().__init__(x, y, w, h, color)
        self.movement = movement


    def move(self):
        self.x += self.movement.get("x")
        self.y += self.movement.get("y")


class Player(Entity):
    VEL = 8
    GRAVITY = 0.50
    JUMP = 14
    def __init__(self, x, y, w, h, color):
            super().__init__(x, y, w, h, color)
            self.x_vel = self.VEL
            self.y_vel = 0
            self.floor_collision = False
            self.right_wall_collition = False
            self.left_wall_collition = False
            self.ceiling_collition = False
            self.direction = "D"
            self.horizontal_direction = "R"
            self.bullets = []

    def shoot(self):
        movement = {"y": 0}
        x_pos = 0
        if self.horizontal_direction == "R":
            movement["x"] = 10
            x_pos = self.x + self.w
        else:
            movement["x"] = -1 * 10
            x_pos = self.x - self.w // 2
        self.bullets.append(Bullet(x_pos, self.y + self.h // 2, 5, 5, "black", movement))

    def draw(self, screen):
        super().draw(screen)
        if self.horizontal_direction == "R":
            pygame.draw.rect(screen, "black", (self.x + self.w // 2, self.y + self.h // 2, 30, 5))
        elif self.horizontal_direction == "L":
            pygame.draw.rect(screen, "black", (self.x - 10, self.y + self.h // 2, 30, 5))
        for b in self.bullets:
            pygame.draw.rect(screen, b.color, b)

    def move_right(self):
        if self.right >= WIDTH:
            return
        if self.right_wall_collition:
            return
        self.x += self.x_vel
        self.horizontal_direction = "R"

    def move_left(self):
        if self.left <= 0:
            return
        if self.left_wall_collition:
            return
        self.x -= self.x_vel
        self.horizontal_direction = "L"
        
    def gravity(self):
        if self.floor_collision and self.direction == "D":
            self.y_vel = 0 
            return
        if self.ceiling_collition and self.direction == "U":
            self.y_vel = 0

        if self.y_vel <= 15:
            self.y_vel += self.GRAVITY

        if self.y_vel >= 0:
            self.direction = "D"
    
        self.y += self.y_vel
    
    def jump(self):
        if self.floor_collision:
            self.y_vel = -1 * self.JUMP
            self.direction = "U"


def collide_Player_ground(player: Player, grounds: List[Ground]):
    floor_collision = False
    ceiling_collision = False
    left_collision = False
    right_collision = False

    for ground in grounds:
        if player.colliderect(ground):
            if abs(player.bottom - ground.top) <= COLLITION_TOLL and player.direction == "D":
                floor_collision = True
                player.y_vel = 0
                player.y = ground.top - player.h + 1
                continue
            if abs(player.top - ground.bottom) <= COLLITION_TOLL and player.direction == "U":
                ceiling_collision = True
                player.y = ground.bottom
                player.y_vel = 0
                continue

            if abs(player.left - ground.right) <= COLLITION_TOLL and player.horizontal_direction == "L":
                left_collision = True
                player.x = ground.right - 1
                continue

            if abs(player.right - ground.left) <= COLLITION_TOLL and player.horizontal_direction == "R":
                right_collision = True
                player.x = ground.left - player.w + 1
                continue


    player.floor_collision = floor_collision
    player.ceiling_collition = ceiling_collision
    player.left_wall_collition = left_collision
    player.right_wall_collition = right_collision
    

def bullets_collision(bullet, grounds: List[Ground]):
    for ground in grounds:
        if bullet.colliderect(ground):
                return True
    return False

def update(clock):
    clock.tick(FPS)
    pygame.display.flip()

def main():
    run = True
    clock = pygame.time.Clock()
    player = Player(250, 250, 40, 40, "red")
    grounds = [Ground(0, HEIGHT - 100, WIDTH, 100, "magenta"), Ground(WIDTH // 2, HEIGHT - 400, 30, 300, "brown"), Ground(0, HEIGHT - 300, 200, 50, "black"), Ground(300, HEIGHT - 500, 200, 50, "green"), Ground(600, HEIGHT - 400, 200, 50, "yellow"), Ground(700, HEIGHT - 200, 50, 20, "magenta")]
    previous_time = pygame.time.get_ticks()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_left()

        if keys[pygame.K_RIGHT]:
            player.move_right()

        if keys[pygame.K_UP]:
            player.jump()
        
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - previous_time > 180:
                previous_time = current_time
                player.shoot()
                
        screen.fill("White")

        player.gravity()
        collide_Player_ground(player, grounds)

        for b in player.bullets[:]:
            b.move()
            if b.x <= 0 or b.x + b.w >= WIDTH:
                player.bullets.remove(b)
            
            if b.y - b.h <= 0 or b.y >= HEIGHT:
                player.bullets.remove(b)
            
            if bullets_collision(b, grounds):
                player.bullets.remove(b)                
            
            print(len(player.bullets))
        
        player.draw(screen)
        for ground in grounds:
            ground.draw(screen)
        update(clock)

    pygame.quit()
    

if __name__ == "__main__":
    main()

