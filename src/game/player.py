import math
import pygame
from src.game.content import SOLID, WATER


class Player:
    def __init__(self, data):
        self.pos = [data.get('x', 40.5), data.get('y', 45.0), data.get('z', 40.5)]
        self.yaw = data.get('yaw', 0.0)
        self.pitch = data.get('pitch', 0.0)
        self.vel = [0.0, 0.0, 0.0]
        self.on_ground = False
        self.eye_height = 1.62
        self.width = 0.6
        self.height = 1.8
        self.walk_time = 0.0
        self.is_walking = False

    @property
    def eye_y(self):
        return self.pos[1] + self.eye_height

    def forward(self):
        cp = math.cos(self.pitch)
        return (math.sin(self.yaw) * cp, math.sin(self.pitch), math.cos(self.yaw) * cp)

    def handle_input(self, keys, dt):
        speed = 4.5
        fx, fz = math.sin(self.yaw), math.cos(self.yaw)
        rx, rz = math.cos(self.yaw), -math.sin(self.yaw)
        mx = mz = 0.0
        if keys[pygame.K_w]: mx += fx; mz += fz
        if keys[pygame.K_s]: mx -= fx; mz -= fz
        if keys[pygame.K_a]: mx -= rx; mz -= rz
        if keys[pygame.K_d]: mx += rx; mz += rz
        L = math.hypot(mx, mz)
        if L > 0.001:
            self.vel[0] = mx / L * speed
            self.vel[2] = mz / L * speed
            self.is_walking = True
            self.walk_time += dt * 8
        else:
            self.vel[0] = 0.0
            self.vel[2] = 0.0
            self.is_walking = False

    def update_physics(self, dt, world):
        bx = int(math.floor(self.pos[0]))
        bz = int(math.floor(self.pos[2]))
        by = int(math.floor(self.pos[1] + 0.5))
        in_water = world.get_block(bx, by, bz) == WATER
        keys = pygame.key.get_pressed()

        if in_water:
            self.vel[1] -= 8.0 * dt
            self.vel[1] = max(self.vel[1], -3.0)
            if keys[pygame.K_SPACE]:
                self.vel[1] = 3.0
        else:
            self.vel[1] -= 28.0 * dt
            self.vel[1] = max(self.vel[1], -50.0)
            if keys[pygame.K_SPACE] and self.on_ground:
                self.vel[1] = 8.0
                self.on_ground = False

        self.on_ground = False
        self._move_axis(0, self.vel[0] * dt, world)
        self._move_axis(1, self.vel[1] * dt, world)
        self._move_axis(2, self.vel[2] * dt, world)

        # Respawn if fallen through world
        if self.pos[1] < -10:
            self.pos[1] = 60
            self.vel = [0.0, 0.0, 0.0]

    def _move_axis(self, axis, delta, world):
        if abs(delta) < 1e-6:
            return
        old = self.pos[axis]
        self.pos[axis] += delta
        if self._collides(world):
            self.pos[axis] = old
            if axis == 1 and delta < 0:
                self.on_ground = True
            self.vel[axis] = 0.0

    def _collides(self, world):
        hw = self.width / 2
        x0, x1 = self.pos[0] - hw, self.pos[0] + hw
        y0, y1 = self.pos[1], self.pos[1] + self.height
        z0, z1 = self.pos[2] - hw, self.pos[2] + hw
        for bx in range(int(math.floor(x0)), int(math.floor(x1)) + 1):
            for by in range(int(math.floor(y0)), int(math.floor(y1)) + 1):
                for bz in range(int(math.floor(z0)), int(math.floor(z1)) + 1):
                    if world.get_block(bx, by, bz) in SOLID:
                        if (x1 > bx and x0 < bx + 1 and y1 > by
                                and y0 < by + 1 and z1 > bz and z0 < bz + 1):
                            return True
        return False

    def to_dict(self):
        return {'x': self.pos[0], 'y': self.pos[1], 'z': self.pos[2],
                'yaw': self.yaw, 'pitch': self.pitch}
