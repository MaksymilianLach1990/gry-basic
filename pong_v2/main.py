import pygame
import pygame.locals

class Board(object):
    """
    Board for play. Odpowiada za draw game window
    """

    def __init__(self, width, height):
        """
        Konstruktor planszy do gry. Przygotowuje okienko gry.

        :param width:
        :param height:
        """
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption("Ping Pong")

    def draw(self, args):
        """
        Rysuje okno gry
        
        :param args: lista obiektów do narysowania
        """
        background = (0, 0, 0)
        self.surface.fill(background)
        for drawable in args:
            drawable.draw_on(self.surface)

        pygame.display.update()


class PongGame(object):
    """
    Łączy wszystkie elementy gry w całość.
    """

    def __init__(self, width, height):
        pygame.init()
        self.board = Board(width, height)

        self.fps_clock = pygame.time.Clock()

    def run(self):
        """
        Główna pętla programu
        """
        while not self.handle_events():
            self.board.draw()
            self.fps_clock.tick(30)

    def handle_events(self):
        """
        Obsługa zdarzeń systemowych
        
        :return True jeżeli pygame przekazał zdarzenie wyjścia z gry
        """
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                return True    


class Drawable(object):
    """
    Klasa bazowa dla rysowanych obiektów
    """
    def __init__(self, width, height, x, y, color=(0, 255, 0)):
        self.width = width
        self.height = height
        self.color = color
        self.surface = pygame.Surface([width, height], pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.surface.get_rect(x=x, y=y)

    def draw_on(self, surface):
        surface.blit(self.surface, self.rect)
        

if __name__ == "__main__":
    game = PongGame(800, 500)
    game.run()