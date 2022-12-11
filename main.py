import random
import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True
        self.balls = []
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the mouse click intersects with any of the balls
                    for ball in self.balls:
                        if ball.rect.collidepoint(event.pos):
                            self.balls.remove(ball)

            # Generate a new random ball if there are less than 3 balls
            if len(self.balls) < 5:
                ball = Ball()
                self.balls.append(ball)

            # Update the screen
            self.screen.fill((255, 255, 255))
            for ball in self.balls:
                ball.update()
                ball.draw(self.screen)
            pygame.display.flip()

class Ball:
    def __init__(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(0, 600)
        self.radius = random.randint(10, 50)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self):
        # Move the ball upward
        self.y -= 1

        # Update the ball's rectangle
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

game = Game()
game.run()

