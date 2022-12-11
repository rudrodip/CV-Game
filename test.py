import cv2
import pygame

class FaceDetector:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Create a Pygame window
        self.window = pygame.display.set_mode((960, 540))
        self.clock = pygame.time.Clock()
        # Create a VideoCapture object
        self.video_capture = cv2.VideoCapture('test_example.mp4')

    def run(self):
        while True:
            # Read a frame from the camera
            ret, frame = self.video_capture.read()
            self.clock.tick(24)
            # Convert the frame to a Pygame image
            frame = cv2.resize(frame, (960, 540))
            image = pygame.image.frombuffer(frame, (960, 540), 'BGR')

            # Update the Pygame window with the new frame
            self.window.blit(image, (0, 0))
            pygame.display.update()

            # Check for quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.video_capture.release()
                    pygame.quit()
                    return

if __name__ == '__main__':
    face_detector = FaceDetector()
    face_detector.run()
