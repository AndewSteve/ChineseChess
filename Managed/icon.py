import pygame

class icon(pygame.sprite.Sprite):
    def __init__(self,image_path, initial_position=(0, 0)):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
    
    def set_topleft(self,topleft):
        self.rect.topleft = topleft
    
    def set_center(self,center):
        self.center = center