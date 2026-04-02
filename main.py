import pygame
import sys

from logger import log_state, log_event
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
                    ast.split()
                    shot.kill()
            if is_colided:
                log_event("player_hit")
                print("Game Over")
                sys.exit()
        pygame.display.flip()

if __name__ == "__main__":
    main()
