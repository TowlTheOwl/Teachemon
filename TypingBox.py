import pygame

class TypingBox:
    def __init__(self, pos:tuple, length, width, id) -> None:
        self.text = ""
        self.x = pos[0]
        self.y = pos[1]
        self.length = length
        self.width = width
        self.rect = pygame.Rect(self.x, self.y, length, width)
        self.rect.center = pos
        self.id = id
        self.valid_keys = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def update(self, events, arrow):
        if arrow == self.id:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    for key in self.valid_keys:
                        if len(self.text)<20 and event.key == pygame.key.key_code(key):
                            self.text += key.upper()
    def return_rect(self):
        return self.rect
    def return_text(self):
        return self.text
    def draw(self, screen, font:pygame.font.Font):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        text_render = font.render(self.text, True, (255, 255, 255))
        text_rect = text_render.get_rect(centery=self.y, left=self.x-self.length/2+10)
        screen.blit(text_render, text_rect)
    def reset(self):
        self.text = ""