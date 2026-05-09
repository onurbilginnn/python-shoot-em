import pygame
import sys
import math

from logger import log_state, log_event
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, EXTRA_LIFE_SCORE

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    score_font = pygame.font.Font(None, 36)
    life_font = pygame.font.Font(None, 36)
    popup_font = pygame.font.Font(None, 30)
    score = 0
    extra_life = 1
    score_popups = []
    extra_life_popups = []
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    astreoidField = AsteroidField()
    dt = 0
    clock =  pygame.time.Clock()
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        dt = clock.tick(60) / 1000
        updatable.update(dt)
        for obj in drawable:
            obj.draw(screen)
        for ast in asteroids:
            is_colided = ast.collides_with(player)
            for shot in shots:
                if ast.collides_with(shot):
                    log_event("asteroid_shot")
                    hit_position = ast.position.copy()
                    earned_score = ast.calculate_asteroid_score()
                    ast.split()
                    shot.kill()
                    print("asteroid radius:", ast.radius)
                    score += earned_score
                    if score / (EXTRA_LIFE_SCORE * extra_life) > 1:
                        print(score / (EXTRA_LIFE_SCORE * extra_life))
                        extra_life += 1
                        player.total_lifes += 1
                        extra_life_popups.append(
                        {
                            "position": hit_position,
                            "value": "+1 Life",
                            "age": 0.0,
                            "duration": 5.0,
                        }
                    )
                    else:
                        score_popups.append(
                            {
                                "position": hit_position,
                                "value": earned_score,
                                "age": 0.0,
                                "duration": 3.0,
                            }
                        )
                    break
            if is_colided:
                if player.is_invulnerable():
                    continue
                if player.total_lifes > 0:
                    player.delete_life()
                    player.start_invulnerability()
                else:
                    log_event("player_hit")
                    print("Game Over")
                    sys.exit()
        rounded_score = math.ceil(score)
        score_surface = score_font.render(f"Score: {rounded_score}", True, "white")
        screen.blit(score_surface, (20, 20))
        player_surface = life_font.render(f"Lifes: {player.total_lifes}", True, "red")
        screen.blit(player_surface, (1150, 20))

        for popup in score_popups[:]:
            popup["age"] += dt
            if popup["age"] >= popup["duration"]:
                score_popups.remove(popup)
                continue

            progress = popup["age"] / popup["duration"]
            rise_offset = popup["age"] * 40
            alpha = max(0, int(255 * (1 - progress)))
            popup_text = f"+{math.ceil(popup['value'])}"
            popup_surface = popup_font.render(popup_text, True, "white")
            popup_surface.set_alpha(alpha)
            popup_rect = popup_surface.get_rect(
                center=(popup["position"].x, popup["position"].y - rise_offset)
            )
            screen.blit(popup_surface, popup_rect)

        for popup in extra_life_popups[:]:
            popup["age"] += dt
            if popup["age"] >= popup["duration"]:
                extra_life_popups.remove(popup)
                continue

            progress = popup["age"] / popup["duration"]
            rise_offset = popup["age"] * 40
            alpha = max(0, int(255 * (1 - progress)))
            popup_surface = popup_font.render(popup["value"], True, "green")
            popup_surface.set_alpha(alpha)
            popup_rect = popup_surface.get_rect(
                center=(popup["position"].x, popup["position"].y - rise_offset)
            )
            screen.blit(popup_surface, popup_rect)

        pygame.display.flip()

if __name__ == "__main__":
    main()
