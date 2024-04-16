import pygame

class Pieces:
    def __init__(self, image_path, position):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.clicked = False
        self.current_position = position
    
    def move(self, new_position):
        self.rect.center = new_position
        self.current_position = new_position
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_clicked(pygame.mouse.get_pos()):
            self.clicked = True
        else:
            self.clicked = False