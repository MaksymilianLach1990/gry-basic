import pygame
import pygame.locals

class Board(object):
    """
    Board for play. Responsible for the draw game window.
    """

    def __init__(self, width, height):
        """
        Game board constructor. Prepare the game window.

        :param width:
        :param height:
        """
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption("Ping Pong")

    def draw(self, args):
        """
        Draws the game window.
        
        :param args: list of objects to be drawn
        """
        background = (0, 0, 0)
        self.surface.fill(background)
        for drawable in args:
            drawable.draw_on(self.surface)

        pygame.display.update()


class PongGame(object):
    """
    It brings all  the elements of the game together.
    """

    def __init__(self, width, height):
        pygame.init()
        self.board = Board(width, height)

        self.fps_clock = pygame.time.Clock()

    def run(self):
        """
        The main program loop.
        """
        while not self.handle_events():
            self.board.draw()
            self.fps_clock.tick(30)

    def handle_events(self):
        """
        System event handling.
        
        :return True if pygame passed a quit event
        """
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                return True    


class Drawable(object):
    """
    Base clss for drawn objects.
    """
    def __init__(self, width, height, x, y, color=(0, 255, 0)):
        self.width = width
        self.height = height
        self.color = color
        self.surface = pygame.Surface([width, height], pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.surface.get_rect(x=x, y=y)

    def draw_on(self, surface):
        surface.blit(self.surface, self.rect)


class Ball(Drawable):
    """
    The ball itself controls its speed and the direction of movement.
    """
    def __init__(self, width, height, x, y, color=(255, 0, 0), x_speed=3, y_speed=3):
        super(Ball, self).__init__(width, height, x, y, color)
        pygame.draw.ellipse(self.surface, self.color, [0, 0, self.width, self.height])
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.start_x = x
        self.start_y = y

    def bounce_y(self):
        """
        Inverts the velocity vector on the Y axis.
        """
        self.y_speed *= -1

    def bounce_x(self):
        """
        Inverts the velocity vector on the X axis.
        """
        self.x_speed *= -1

    def reset(self):
        """
        Brings the ball to its initial position and inverts the velocity vector 
        along the X axis.
        """
        self.rect.move(self.start_x, self.start_y)
        self.bounce_x()

    def move(self):
        """
        Moves the ball by the velocity vector.
        """
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed


if __name__ == "__main__":
    game = PongGame(800, 500)
    game.run()