import pygame

class Board:
    def __init__(self, position):
        self.position = position
        self.occupied = False  # Initially, the position is not occupied
        self.piece = None

    def draw_circle(self, surface, color):
        self.circle = pygame.draw.circle(surface, color, self.position, 15, 4)
    
    def is_clicked(self, mouse_pos):
        x, y = self.position
        return (x - 40) <= mouse_pos[0] <= (x + 40) and (y - 40) <= mouse_pos[1] <= (y + 40)