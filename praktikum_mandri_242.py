import pygame
import sys

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tugas PBO: Space Battle - Victory System")

font = pygame.font.SysFont("Arial", 50, bold=True)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

class GameObject(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Bullet(GameObject):
    def __init__(self, x, y):
        super().__init__((255, 255, 0), 5, 10, x, y)
        self.speed = -7

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Player(GameObject):
    def __init__(self):
        super().__init__((0, 128, 255), 40, 40, SCREEN_WIDTH//2, SCREEN_HEIGHT-50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        return Bullet(self.rect.centerx - 2, self.rect.top)

class Enemy(GameObject):
    def __init__(self, x_pos, speed):
        super().__init__((255, 0, 0), 30, 30, x_pos, -30)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = -30
            self.rect.x = (self.rect.x + 100) % (SCREEN_WIDTH - 30)


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(5):
    enemy = Enemy(x_pos=i * 110 + 30, speed=2)
    all_sprites.add(enemy)
    enemies.add(enemy)

def main():
    running = True
    game_over = False
    victory = False
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not game_over and not victory:
                if event.key == pygame.K_SPACE:
                    b = player.shoot()
                    all_sprites.add(b)
                    bullets.add(b)

        if not game_over and not victory:
            all_sprites.update()
            pygame.sprite.groupcollide(enemies, bullets, True, True)
            if len(enemies) == 0:
                victory = True
            if pygame.sprite.spritecollide(player, enemies, False):
                game_over = True
        screen.fill((20, 20, 20))
        all_sprites.draw(screen)
        if victory:
            draw_text("YOU WIN!", font, (0, 255, 0), SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 25)
        elif game_over:
            draw_text("GAME OVER", font, (255, 0, 0), SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 25)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()