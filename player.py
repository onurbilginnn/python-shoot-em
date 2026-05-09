import pygame
from circleshape import CircleShape
from shot import Shot

from constants import (
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_INVULNERABILITY_SECONDS,
    LINE_WIDTH,
    PLAYER_SHOOT_SPEED,
    SHOT_RADIUS,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    STARTING_LIFE_COUNT
)


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0
        self.total_lifes = STARTING_LIFE_COUNT
        self.invulnerability_timer = 0.0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        if self.is_invulnerable():
            # Blink at ~10Hz while invulnerable.
            if int(self.invulnerability_timer * 10) % 2 == 0:
                return
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shoot_cooldown -= dt
        self.invulnerability_timer = max(0.0, self.invulnerability_timer - dt)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(dt * -1)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(dt * -1)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.shoot_cooldown > 0:
            return
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

    def add_life(self):
        self.total_lifes += 1
    
    def delete_life(self):
        self.total_lifes -= 1

    def is_invulnerable(self):
        return self.invulnerability_timer > 0

    def start_invulnerability(self):
        self.invulnerability_timer = PLAYER_INVULNERABILITY_SECONDS