import random
import pygame
import sys
from pygame.locals import *

class Particle:
    def __init__(self, x, y, radius, color, dx, dy):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dx = dx
        self.dy = dy

    def draw(self, win):
        pygame.draw.circle(win, self.color, (round(self.x), round(self.y)), self.radius)
    
    def distanceTo(self, other_particle):
        return (((self.x - other_particle.x) ** 2 + (self.y - other_particle.y) ** 2) ** 0.5)
    
    def detectCollision(self, particles):
        for particle in particles:
            if particle != self:
                distance = self.distanceTo(particle)
                if distance <= self.radius + particle.radius:
                    # Separate particles slightly after collision to prevent sticking
                    overlap = 0.5 * (distance - self.radius - particle.radius)
                    
                    self.x -= overlap * (self.x - particle.x) / distance
                    self.y -= overlap * (self.y - particle.y) / distance
                    
                    particle.x += overlap * (self.x - particle.x) / distance
                    particle.y += overlap * (self.y - particle.y) / distance

                    # Calculate new velocities after collision
                    new_dx1 = (self.dx * (self.radius - particle.radius) + 2 * particle.radius * particle.dx) / (self.radius + particle.radius)
                    new_dy1 = (self.dy * (self.radius - particle.radius) + 2 * particle.radius * particle.dy) / (self.radius + particle.radius)
                    new_dx2 = (particle.dx * (particle.radius - self.radius) + 2 * self.radius * self.dx) / (self.radius + particle.radius)
                    new_dy2 = (particle.dy * (particle.radius - self.radius) + 2 * self.radius * self.dy) / (self.radius + particle.radius)

                    self.dx, self.dy = new_dx1, new_dy1
                    particle.dx, particle.dy = new_dx2, new_dy2

        # Detect collision with walls
        if self.x - self.radius <= 0:
            self.x = self.radius  # adjust x position to keep particle within screen
            self.dx *= -1  # reverse x direction
        elif self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius  # adjust x position to keep particle within screen
            self.dx *= -1  # reverse x direction

        if self.y - self.radius <= 0:
            self.y = self.radius  # adjust y position to keep particle within screen
            self.dy *= -1  # reverse y direction
        elif self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius  # adjust y position to keep particle within screen
            self.dy *= -1  # reverse y direction

    def updatePos(self):
        self.x += self.dx
        self.y += self.dy

def initParticles(num_particles, width, height):
    particles = []
    while len(particles) < num_particles:
        x = random.randint(50, width - 50)
        y = random.randint(50, height - 50)
        radius = random.uniform(2, 20)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        dx = random.randint(-10, 10)
        dy = random.randint(-10, 10)
        
        new_particle = Particle(x, y, radius, color, dx, dy)
        
        if all(new_particle.distanceTo(p) > new_particle.radius + p.radius for p in particles):
            particles.append(new_particle)
    
    return particles

pygame.init()

WIDTH, HEIGHT = 800, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Collision simulation")

particles = initParticles(50, WIDTH, HEIGHT)

done = False
clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
    win.fill("white")

    for particle in particles:
        particle.draw(win)
        particle.detectCollision(particles)
        particle.updatePos()
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()
