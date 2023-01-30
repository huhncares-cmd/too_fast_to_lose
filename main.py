import pygame, random

pygame.init()

SCREEN_WIDTH    = 400
SCREEN_HEIGHT   = 700 

SCREEN_COLOR = (0, 0, 0)

WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Too fast to lose')

FPS = 30

def check_for_collision(meteorites, player):
    for meteorite_collision in meteorites:
        if player.get_collider().colliderect(meteorite_collision.get_collider()):
            return True
    return False

def redraw_screen(player, stars, meteorites, score, score_font):
    WINDOW.fill(SCREEN_COLOR)

    for star in stars:
        star.y += star.velocity
        if star.y > SCREEN_HEIGHT:
            star.y = 0
        star.draw()
    for meteorite in meteorites:
        meteorite.y += meteorite.velocity
        if meteorite.y - meteorite.radius > SCREEN_HEIGHT:
            meteorites.remove(meteorite)
        meteorite.draw()
    score_text = score_font.render(str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//6))
    WINDOW.blit(score_text, score_rect)
    player.draw()
    pygame.display.update()

    return stars, meteorites

class Meteorite:
    def __init__(self, radius, x, y, velocity, color):
        self.radius = radius
        self.x = x
        self.y = y

        self.color = color
        self.velocity = velocity
    
    def draw(self):
        pygame.draw.circle(WINDOW, self.color, (self.x, self.y), self.radius)

    def get_collider(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

class Star:
    def __init__(self, radius, x, y, velocity, color):
        self.radius = radius
        self.x = x
        self.y = y

        self.color = color
        self.velocity = velocity
    
    def draw(self):
        pygame.draw.circle(WINDOW, self.color, (self.x, self.y), self.radius)

class Player:
    def __init__(self, width, height, velocity):
        self.width = width
        self.height = height

        self.x = SCREEN_WIDTH // 2 - width // 2
        self.y = SCREEN_HEIGHT - SCREEN_HEIGHT // 4

        self.velocity = velocity
    
    def draw(self):
        pygame.draw.rect(WINDOW, (255, 0, 0), (self.x, self.y, self.width, self.height))
    
    def get_collider(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

if __name__ == "__main__":
    player = Player(50, 50, 10)
    clock = pygame.time.Clock()

    score_font = pygame.font.Font("assets/font/font.ttf", 64)

    meteorite_spawn_interval_max = FPS * 5
    meteorite_spawn_interval = meteorite_spawn_interval_max
    meteorite_velocity = 10
    max_meteorite_velocity = 25

    meteorites = []

    score = 0

    WINDOW.fill(SCREEN_COLOR)
    stars = []
    for i in range(100):
        stars.append(Star(1, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), 4, (255, 255, 255)))
        stars[i].draw() 
    player.draw()
    pygame.display.update()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x > player.velocity:
            player.x -= player.velocity
        if keys[pygame.K_RIGHT] and player.x < SCREEN_WIDTH - player.width - player.velocity:
            player.x += player.velocity
        
        if meteorite_spawn_interval <= 0:
            meteorite_spawn_interval = meteorite_spawn_interval_max
            meteorites.append(Meteorite(random.randint(20, 100), random.randint(0, SCREEN_WIDTH), 0, meteorite_velocity, (0, 0, 255)))
            score += 1
            if meteorite_spawn_interval_max >= FPS * 1.2:
                meteorite_spawn_interval_max -= FPS // 3
            if meteorite_velocity <= max_meteorite_velocity:
                meteorite_velocity += 0.1
        else:
            meteorite_spawn_interval -= 1

        print(meteorite_velocity, meteorite_spawn_interval, meteorite_spawn_interval_max)

        if check_for_collision(meteorites, player):
            running = False

        stars, meteorites = redraw_screen(player, stars, meteorites, score, score_font)
    pygame.quit()