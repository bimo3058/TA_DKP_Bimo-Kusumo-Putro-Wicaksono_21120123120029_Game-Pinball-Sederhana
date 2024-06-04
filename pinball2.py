import pygame
import random
import sys
import math

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 768
BG_COLOR = (0, 0, 0)

# Setup layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pinball Coba-Coba")

# Wallpaper
wallpaper = pygame.image.load("wallpaperbetter.com_1280x768.jpg")

# Warna
WHITE = (255, 255, 255)
DARKRED = (139, 0, 0)
DARKBLUE = (0, 0, 128)
GRAY = (150, 150, 150)
LIGHTGRAY= (160,160,160)
DARKGRAY = (102, 102, 102)

# Frame rate
clock = pygame.time.Clock()
FPS = 60

class Ball:
    def __init__(self):
        self.radius = 10
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.dx = random.choice([-9, 9])  # Kecepatan horizontal awal
        self.dy = random.choice([-9, -8, -7, -6])  # Kecepatan vertikal awal
        self.color = GRAY
        self.collision_color_change_delay = 0
    
    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Pantulan dari dinding
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.dx *= -1
        if self.y <= self.radius:
            self.dy *= -1
        elif self.y >= SCREEN_HEIGHT - self.radius:
            game_over_screen()

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class Paddle:
    def __init__(self):
        self.width = 170
        self.height = 10
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 30
        self.dx = 0
        self.color = LIGHTGRAY
    
    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.dx = -7
        elif keys[pygame.K_RIGHT]:
            self.dx = 7
        else:
            self.dx = 0
        self.x += self.dx

        # Batas layar
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Block:
    def __init__(self, x, y, radius=15, color=DARKRED, outline_color=WHITE, outline_width=2):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.destroyed = False

    def draw(self):
        if not self.destroyed:
            # Gambar outline
            pygame.draw.circle(screen, self.outline_color, (self.x, self.y), self.radius, self.outline_width)
            # Gambar blok
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius - self.outline_width)

    def check_collision(self, ball):
        if not self.destroyed:
            distance = math.sqrt((self.x - ball.x)**2 + (self.y - ball.y)**2)
            if distance <= self.radius + ball.radius:
                self.destroyed = True
                ball.dy *= -1
                ball.color = DARKRED  # Ganti warna bola saat mengenai blok
                ball.collision_color_change_delay = 5 
                return True
        return False

def create_blocks(rows, cols):
    blocks = []
    block_radius = 15
    for row in range(rows):
        for col in range(cols):
            x = (col * 2 + 1) * ((SCREEN_WIDTH - 2*block_radius) // (cols * 2)) + block_radius
            y = (row * 2 + 1) * ((SCREEN_HEIGHT // 4 - 2*block_radius) // (rows * 2)) + block_radius
            blocks.append(Block(x, y, block_radius))
    return blocks     

def main_menu_screen():
    wallpaper = pygame.image.load("wallpaperbetter.com_1280x768.jpg")
    font = pygame.font.Font("bahnschrift.ttf", 50)
    text = font.render("PINBALL COBA COBA", True, WHITE)

    button_font = pygame.font.Font("bahnschrift.ttf", 22)
    restart_text = button_font.render("Mulai", True, WHITE)
    quit_text = button_font.render("Keluar", True, WHITE)

    start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50)
    screen.blit(wallpaper, (0, 0))
    
    # Menggambar kotak UI
    ui_box = pygame.Rect(SCREEN_WIDTH // 2 - 280, SCREEN_HEIGHT // 2 - 180, 570, 330)
    pygame.draw.rect(screen, DARKGRAY, ui_box)
    pygame.draw.rect(screen, DARKBLUE, start_button)
    pygame.draw.rect(screen, DARKRED, quit_button)

    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 100))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 70))

    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    main()
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
    
def game_over_screen():
    font = pygame.font.Font("bahnschrift.ttf", 74)
    text = font.render("GAME OVER", True, WHITE)

    button_font = pygame.font.Font("bahnschrift.ttf", 22)
    restart_text = button_font.render("Lanjut", True, WHITE)
    quit_text = button_font.render("Keluar", True, WHITE)

    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50)

    # Menggambar kotak UI
    ui_box = pygame.Rect(SCREEN_WIDTH // 2 - 280, SCREEN_HEIGHT // 2 - 180, 570, 330)
    pygame.draw.rect(screen, DARKGRAY, ui_box)
    pygame.draw.rect(screen, DARKBLUE, restart_button)
    pygame.draw.rect(screen, DARKRED, quit_button)

    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 100))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 70))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    main()
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def main():
    running = True
    ball = Ball()
    paddle = Paddle()
    blocks = create_blocks(5, 25)  # 5 baris, 25 kolom
    score = 0
    destroyed_blocks = 0  # Jumlah blok yang dihancurkan

    # Font untuk teks skor
    font = pygame.font.Font("bahnschrift.ttf", 22)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Mendapatkan input tombol saat ini
        keys = pygame.key.get_pressed()
        ball.move()
        paddle.move(keys)

        # Deteksi benturan antara bola dan paddle
        if ball.y + ball.radius >= paddle.y and paddle.x - ball.radius <= ball.x <= paddle.x + paddle.width + ball.radius:
            ball.dy *= -1
            ball.dx = 10 * ((ball.x - (paddle.x + paddle.width // 2)) / paddle.width)

        # Deteksi tabrakan antara bola dan blok
        for block in blocks:
            if block.check_collision(ball):
                score += 10  
                destroyed_blocks += 1 
                if destroyed_blocks % 5 == 0:  
                    # Batasi peningkatan kecepatan bola
                    if math.sqrt(ball.dx ** 2 + ball.dy ** 2) < 4:
                        ball.dx *= 1.1  
                        ball.dy *= 1.1
                        # Batas kecepatan maksimum bola
                        speed_limit = 4
                        if math.sqrt(ball.dx ** 2 + ball.dy ** 2) > speed_limit:
                            ball.dx *= speed_limit / math.sqrt(ball.dx ** 2 + ball.dy ** 2)
                            ball.dy *= speed_limit / math.sqrt(ball.dy ** 2 + ball.dy ** 2)
                break

        # Menggambar objek
        screen.blit(wallpaper, (0, 0))
        ball.draw()
        paddle.draw()
        for block in blocks:
            block.draw()

        # Tampilkan skor
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, SCREEN_HEIGHT - 40))

        if ball.collision_color_change_delay > 0:
            ball.collision_color_change_delay -= 1
            if ball.collision_color_change_delay == 0:
                ball.color = GRAY
        pygame.display.flip()

        # Periksa apakah semua blok hancur
        if all(block.destroyed for block in blocks):
            print("Congratulations! You destroyed all the blocks.")
            running = False
        
        clock.tick(FPS)

    main_menu_screen()
    game_over_screen()

if __name__ == "__main__":
    main_menu_screen()
    main()
