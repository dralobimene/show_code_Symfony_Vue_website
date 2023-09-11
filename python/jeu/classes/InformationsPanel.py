# classes/InformationsPanel.py

import pygame
import pygame_gui


class InformationsPanel(pygame.Surface):
    def __init__(self, rect):
        super().__init__(rect.size)
        self.rect = rect
        self.scroll_y = 0
        self.messages = []

    def update(self):
        self.fill((0, 0, 0))
        intermediate = pygame.Surface((self.rect.width, self.rect.height * 2))

        x1, x2 = self.rect.left, self.rect.right
        a, b = (255, 0, 0), (60, 255, 120)
        y1, y2 = self.rect.top, self.rect.bottom
        h = y2 - y1
        rate = (
            float((b[0] - a[0]) / h),
            float((b[1] - a[1]) / h),
            float((b[2] - a[2]) / h)
        )
        for line in range(y1, y2):
            color = (
                min(max(a[0] + (rate[0] * line), 0), 255),
                min(max(a[1] + (rate[1] * line), 0), 255),
                min(max(a[2] + (rate[2] * line), 0), 255)
            )
            pygame.draw.line(intermediate, color, (x1, line), (x2, line))

        y = 20
        font = pygame.font.SysFont('', 22)

        for i, message in enumerate(self.messages):
            text_color = (255, 255, 255)
            if message.startswith("sys: "):
                text_color = (255, 0, 0)
            text_surface = font.render(message, True, text_color)
            intermediate.blit(text_surface, (10, y + 20 * (i + 1)))

        self.blit(intermediate, (0, self.scroll_y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.scroll_y = min(self.scroll_y + 15, 0)
            if event.button == 5:
                self.scroll_y = max(self.scroll_y - 15, -self.rect.height)

    def add_message(self, message):
        self.messages.append(message)
        self.scroll_y = min(0, -(len(self.messages) * 20 - self.rect.height))
