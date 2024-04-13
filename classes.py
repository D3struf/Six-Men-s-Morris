import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def transform_scale(self, sizes):
        self.image = pygame.transform.scale(self.image, sizes)
        
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Pieces(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.clicked = False
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_clicked(pygame.mouse.get_pos()):
            self.clicked = True
        else:
            self.clicked = False

class BoardPosition:
    def __init__(self, position):
        self.position = position
        self.occupied = False  # Initially, the position is not occupied
        self.piece = None

    def draw_circle(self, surface):
        self.circle = pygame.draw.circle(surface, "GREEN", self.position, 15, 4)
    
    def is_clicked(self, mouse_pos):
        x, y = self.position
        return (x - 40) <= mouse_pos[0] <= (x + 40) and (y - 40) <= mouse_pos[1] <= (y + 40)
    
    def set_piece(self, piece):
        self.piece = piece
        self.occupied = True

    def remove_piece(self):
        self.piece = None
        self.occupied = False
        
class Overlay(pygame.sprite.Sprite):
    def __init__(self, image_page, position):
        super().__init__()
        self.image = pygame.image.load(image_page).convert_alpha()
        self.rect = self.image.get_rect(center=position)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)