import random
import pygame
from pygame.locals import *
from detect_object import CameraFeed
import calib_data
from pygame_platform import Platform


class Game(Platform):
    def __init__(self, width: int, height: int, musicFileName: str, volume=1, caption="Pygame Game", icon=None):
        super().__init__(width, height, musicFileName, volume, caption, icon)

    def draw_aruco_markers(self):
        # size: 200x200 and padding: 10

        points = [
            "lt 10 10 0 0",
            "rt -210 10 0 0",
            "rb -210 -210 0 0",
            "lb 10 -210 0 0",
        ]

        for i, point in enumerate(points):
            self.drawImage(f"./ArucoMarkers/marker_{i}.png", pos=point, scale=1)

    def eventHandler(self):
        # handing events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # keyboard event handler
            if event.type == KEYDOWN:

                # resize handler
                if event.type == VIDEORESIZE:
                    if not self.fullscreen:
                        self.screen = pygame.display.set_mode(
                            (event.w, event.h), pygame.RESIZABLE
                        )

                # fullscreen handler
                if event.key == K_F11:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.screen = pygame.display.set_mode(
                            self.monitor_size, pygame.FULLSCREEN
                        )
                    else:
                        self.screen = pygame.display.set_mode(
                            (self.width, self.height), pygame.RESIZABLE
                        )
                        self.screen = pygame.display.set_mode(
                            (self.width, self.height), pygame.RESIZABLE
                        )

                # esc handler
                if event.key == K_ESCAPE:
                    self.running = False

    def run(self):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)

        while self.running:
            # setting fps to 60
            self.clock.tick(60)

            self.scrWidth, self.scrHeight = (
                self.screen.get_width(),
                self.screen.get_height(),
            )

            # event handler
            self.eventHandler()

            self.screen.fill((255, 255, 255))
            self.draw_aruco_markers()

            mx, my = pygame.mouse.get_pos()
            # self.setText("Calibration...", 20, pos="mt 0 0 1 0", foregroundColor=GREEN)

            # updates everything in screen
            pygame.display.flip()


game = Game(
    width=800,
    height=600,
    musicFileName="./game/test.mp3",
    volume=0.7,
    caption="Base template",
    icon="./game/icon.png",
)
game.run()
