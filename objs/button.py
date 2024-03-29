import helper.config as config
import pygame

class Button():
    button_width = 300
    button_height = 100

    def __init__ (self, x, y, color, text):
        self.color = color
        self.x = x
        self.y = y
        self.text = text
    
    def draw(self, screen):
        rect = pygame.Rect((self.x, self.y), (Button.button_width, Button.button_height))
        pygame.draw.rect(config.screen, self.color, rect, 0, 15)

        font = pygame.font.SysFont('Calibri', 60)
        text= font.render(self.text, False, (config.WHITE))
        config.screen.blit(text, (self.x + Button.button_width // 2 - text.get_width() // 2, self.y + Button.button_height // 2 - text.get_height() // 2))
    
    def is_over(self, screen):
        return