import pygame

class Button:
    def __init__(self, image_path, position):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.resize = (self.rect.x + 75, self.rect.y + 75)
        self.clicked = False
        self.selected = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def transform_scale(self, sizes):
        self.rect.width = sizes[0]
        self.rect.height = sizes[1]
        self.image = pygame.transform.scale(self.image, sizes)
        
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def update(self, mouse_pos):
        if self.is_clicked(mouse_pos):
            self.clicked = True
        else:
            self.clicked = False