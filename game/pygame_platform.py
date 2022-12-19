import pygame
import os

class Platform:
    loaded_imgs = {}
    loaded_fonts = {}
    loaded_texts = {}

    def __init__(self, width: int, height: int, resizable: bool, fullscreen: bool, musicFileName: str, volume: float, caption: str, icon: str, custom_cursor: str):
        # initializing pygame
        pygame.init()
        pygame.font.init()

        # setting the absolute path
        self.abs_path = os.path.dirname(__file__)

        # cursor customization
        if custom_cursor:
            pygame.mouse.set_visible(False)
            self.cursor = pygame.image.load(os.path.join(self.abs_path, 'cursor.png'))
            self.cursor = pygame.transform.scale(self.cursor, (20, 20))
            self.cursor_rect = self.cursor.get_rect()

        if musicFileName:
            pygame.mixer.music.load(os.path.join(self.abs_path, musicFileName))
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(volume)

        # default parameters
        self.width = width
        self.height = height

        if resizable:
            self.scrWidth = self.width
            self.scrHeight = self.height

            # monitor size
            self.monitor_size = (
                pygame.display.Info().current_w,
                pygame.display.Info().current_h,
            )

            # initializing display
            self.screen = pygame.display.set_mode(
                (self.width, self.height), pygame.RESIZABLE
            )
        else:
            self.screen = pygame.display.set_mode(
                (self.width, self.height)
            )

        # window title
        if caption:
            pygame.display.set_caption(caption)
        pygame.display.set_caption('Platform')

        # icon
        if icon:
            icon = pygame.image.load(icon)
            pygame.display.set_icon(icon)

        # running loop
        self.running = True

        # fps clock set
        self.clock = pygame.time.Clock()

        # fullscreen bool
        if fullscreen:
            self.fullscreen = False

    def drawImage(self, filename: str, pos=(0, 0), scale=1, angle=0):
        if filename in self.loaded_imgs:
            img = self.loaded_imgs[os.path.join(self.abs_path, filename)]
            pos = self.getPos(pos, (img.get_width(), img.get_height()))
            self.screen.blit(img, pos)
        else:
            img = pygame.image.load(filename).convert_alpha()
            # img.set_colorkey((1, 0, 0))
            size = img.get_size()
            scaled_size = (int(size[0] * scale), int(size[1] * scale))

            img = pygame.transform.scale(img, scaled_size)
            img = pygame.transform.rotate(img, angle)
            pos = self.getPos(pos, (img.get_width(), img.get_height()))

            self.loaded_imgs[os.path.join(self.abs_path, filename)] = img
            self.screen.blit(img, pos)

    def setText(
        self,
        text="",
        size=32,
        pos=(0, 0),
        foregroundColor=(0, 0, 0),
        backgroundColor=None,
    ):
    
        if size not in self.loaded_fonts:
            font = pygame.font.SysFont("Comic Sans MS", size)
            self.loaded_fonts[size] = font

        if f"{text}{size}" not in self.loaded_texts:
            textSurface = font.render(text, True, foregroundColor, backgroundColor)
            self.loaded_texts[f"{text}{size}"] = textSurface
        else:
            textSurface = self.loaded_texts[f"{text}{size}"]
            pos = self.getPos(pos, (textSurface.get_width(), textSurface.get_height()))
            self.screen.blit(textSurface, pos)

    def getPos(self, position: str, size: tuple) -> tuple:
        '''
            getPos function working principle:
                l - left -> x = 0
                m - middle -> x = half-screen-width
                r - right -> x = screen-width
                t - top -> y = 0
                c - center -> y = half-screen-height
                b - bottom -> y = screen-height

                position: str format:
                    '[x_side][y_side] offsetX offsetY centerX centerY'

                    example:
                        'mc 0 0 1 0' -> middle in X-axis 
                                        center at Y-axis
                                        offsetX -> 0
                                        offsetY -> 0
                                        centerX -> True
                                        centerY -> False
        '''
        if type(position) == tuple:
            return position
        position_dict = {
            "l": 0,
            "m": self.scrWidth // 2,
            "r": self.scrWidth,
            "t": 0,
            "c": self.scrHeight // 2,
            "b": self.scrHeight,
        }

        combination, offsetX, offsetY, centerX, centerY = position.split(" ")
        if centerX == "1":
            offsetX = -size[0] // 2 + int(offsetX)
        if centerY == "1":
            offsetY = -size[1] // 2 + int(offsetY)
        pos = (
            position_dict[combination[0]] + int(offsetX),
            position_dict[combination[1]] + int(offsetY),
        )
        return pos