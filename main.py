import pygame
import random

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu d'Évitage")

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Chargement de l'image de fond
background_image_path = "floresta-mais-velha-do-mundo-1.png"
try:
    background_image = pygame.image.load(background_image_path).convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except FileNotFoundError:
    print(f"Image introuvable : {background_image_path}")
    background_image = None  # Aucun fond si l'image est introuvable

# Horloge pour réguler le FPS
clock = pygame.time.Clock()

# Variables du joueur
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 10

# Variables des obstacles
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 10
obstacle_frequency = 15  # Fréquence des obstacles (plus c'est bas, plus ils arrivent souvent)

# Score
score = 0

# Police
font = pygame.font.SysFont("Arial", 30)

# Fonction pour afficher le score
def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Fonction pour dessiner le joueur
def draw_player(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, player_width, player_height))

# Fonction pour dessiner un obstacle
def draw_obstacle(x, y):
    pygame.draw.rect(screen, RED, (x, y, obstacle_width, obstacle_height))

# Fonction pour vérifier les collisions
def check_collision(player_x, player_y, obstacle_x, obstacle_y):
    return (
        player_x < obstacle_x + obstacle_width and
        player_x + player_width > obstacle_x and
        player_y < obstacle_y + obstacle_height and
        player_y + player_height > obstacle_y
    )

# Fonction principale du jeu
def game():
    global player_x, score
    running = True
    obstacles = []

    while running:
        # Affichage du fond
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BLACK)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Détection des touches
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Créer des obstacles
        if random.randint(1, obstacle_frequency) == 1:
            obstacle_x = random.randint(0, WIDTH - obstacle_width)
            obstacles.append([obstacle_x, -obstacle_height])

        # Déplacer et dessiner les obstacles
        for obstacle in obstacles[:]:
            obstacle[1] += obstacle_speed
            if obstacle[1] > HEIGHT:
                obstacles.remove(obstacle)
                score += 1  # Augmenter le score quand un obstacle est évité

            if check_collision(player_x, player_y, obstacle[0], obstacle[1]):
                running = False  # Le joueur a touché un obstacle, fin du jeu

            draw_obstacle(obstacle[0], obstacle[1])

        # Dessiner le joueur
        draw_player(player_x, player_y)

        # Afficher le score
        display_score()

        # Actualiser l'écran
        pygame.display.update()

        # Limiter le nombre d'images par seconde
        clock.tick(60)

    # Fin du jeu
    pygame.quit()
    print(f"Game Over! Your final score is: {score}")

# Lancer le jeu
game()
