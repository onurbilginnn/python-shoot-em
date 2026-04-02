import pygame
import random

from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from circleshape import CircleShape
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
    def update(self, dt):
        self.position += self.velocity * dt
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        random_angle = random.uniform(20 , 50)
        asteroid_vector1 = self.velocity.rotate(random_angle)
        asteroid_vector2 = self.velocity.rotate(random_angle * -1)
        small_asteroid_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, small_asteroid_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, small_asteroid_radius)
        asteroid1.velocity = asteroid_vector1 * 1.2
        asteroid2.velocity = asteroid_vector2 * 1.2



        
        