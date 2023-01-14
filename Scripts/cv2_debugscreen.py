
import pygame
import numpy as np
import cv2
import sys


class TestScreen:
    def __init__(self, size):
        self.size = size

        pygame.init()
        self.scrn = pygame.display.set_mode(size)
        
        pygame.display.set_caption('preview')

    def SetImage(self, img):
        rawframe = np.flipud(np.array(img))#[:, :, ::-1]
        surface = pygame.surfarray.make_surface(cv2.resize(rawframe, self.size, interpolation=0))
        self.scrn.blit(pygame.transform.rotate(surface, 90), (0,0))
        pygame.display.update()
        return

    def Clear(self):
        #self.matrix.fill((0,0,0))
        return

    def check(self):
        pygame.init()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
        return