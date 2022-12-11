import random
import pygame
from detect_object import CameraFeed
import calib_data

class Game:
    def __init__(self, width, height):
        # initializing pygame
        pygame.init()

        # default parameters
        self.width = width
        self.height = height

        # monitor size
        self.monitor_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

        # initializing display
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        # window title
        pygame.display.set_caption('WooooooooooW game')
        # icon
        icon = pygame.image.load('game/icon.png')
        pygame.display.set_icon(icon)

        # running loop
        self.running = True

        # fps clock set
        self.clock = pygame.time.Clock()

        # fullscreen bool
        self.fullscreen = False

    def draw_aruco_markers(self):
        markers = []
        for i in range(4):
            img = pygame.image.load(f"./ArucoMarkers/marker_{i}.png")
            markers.append(img)

        # known that image marker size is 200x200
        imageSize = 200
        padding = 20

        scrWidth, srcHeight = self.screen.get_width(), self.screen.get_height()

        points = [
            (padding, padding),
            (scrWidth - imageSize - padding, padding),
            (scrWidth - imageSize - padding, srcHeight - imageSize - padding),
            (padding, srcHeight - imageSize - padding)
        ]

        for marker, point in zip(markers, points):
            self.screen.blit(marker, point)

    def run(self):
        while self.running:

            # setting fps to 60
            self.clock.tick(60)


            # handing events
            for event in pygame.event.get():

                # quit event handler
                if event.type == pygame.QUIT:
                    self.running = False

                # keyboard event handler
                if event.type == pygame.KEYDOWN:

                    # resize handler
                    if event.type == pygame.VIDEORESIZE:
                        if not self.fullscreen:
                            self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                    # fullscreen handler
                    if event.key == pygame.K_F11:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
                        else:
                            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

                    # esc handler
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            # Update the screen
            self.screen.fill((255, 255, 255))
            
            self.draw_aruco_markers()

            
            pygame.display.flip()

game = Game(800, 600)
game.run()

