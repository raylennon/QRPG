import pygame

class TestScreen:
    def __init__(self, size):
        pygame.init()
        self.size = size
        self.matrix = pygame.display.set_mode(size)
        
        pygame.display.set_caption("QRPG Testing Window")

    def SetImage(self, img):

        mode = img.mode
        size = img.size
        data = img.tobytes()
        
        py_image = pygame.image.fromstring(data, size, mode)

        rect = py_image.get_rect()
        rect.center = (self.size[0]/2, self.size[1]/2)
        self.matrix.blit(py_image, rect)
        pygame.display.update()
        return
    def Clear(self):
        #self.matrix.fill((0,0,0))
        pygame.display.flip()
        return