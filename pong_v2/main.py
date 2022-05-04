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

    def draw(self, *args):
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
        self.ball = Ball(20, 20, width/2, height/2)
        self.player1 = Racket(width=10, height=80, x=0, y=height/2)
        self.player2 = Racket(width=10, height=80, x=width - 20, y= height/2, max_speed=10)
        self.ai = Ai(self.player2, self.ball)
        self.judge = Judge(self.board, self.ball, self.player2)

    def run(self):
        """
        The main program loop.
        """
        print(not self.handle_events())
        while not self.handle_events():
            self.ball.move(self.board, self.player1, self.player2)
            self.board.draw(
                self.ball,
                self.player1,
                self.player2,
                self.judge,
            )
            self.ai.move()
            self.player1.move_smooth()
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.player1.max_speed += 7
                if event.key == pygame.K_UP:
                    self.player1.max_speed -= 7

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.player1.max_speed -= 7
                if event.key == pygame.K_UP:
                    self.player1.max_speed += 7
                
            # Mouse control
            # if event.type == pygame.locals.MOUSEMOTION:
            #     x, y = event.pos
            #     self.player1.move(y) 
            
            


class Drawable(object):
    """
    Base class for drawn objects.
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
    def __init__(self, width, height, x, y, color=(255, 0, 0), x_speed=5, y_speed=5):
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
        self.rect.x, self.rect.y = self.start_x, self.start_y
        self.bounce_y()

    def move(self, board, *args):
        """
        Moves the ball by the velocity vector.
        """
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.rect.x <= 0 or self.rect.x >= board.surface.get_width()-self.width:
            self.bounce_x()
        
        if self.rect.y <= 0 or self.rect.y >= board.surface.get_height()-self.height:
            self.bounce_y()

        for racket in args:
            if self.rect.colliderect(racket.rect):
                self.bounce_x()


class Racket(Drawable):
    """
    Racket, it moves on the Y axis with a speed limit.
    """

    def __init__(self, width, height, x, y, color=(0,255, 0), max_speed=0):
        super(Racket, self).__init__(width, height, x, y, color)
        self.max_speed = max_speed
        self.surface.fill(color)

    def move(self, y):
        """
        Moves the racket to the designated place.
        """
        delta = y - self.rect.y
        if abs(delta) > self.max_speed:
            delta = self.max_speed if delta > 0 else -self.max_speed
        self.rect.y += delta

    def move_smooth(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= pygame.display.get_window_size()[1]:
            self.rect.bottom = pygame.display.get_window_size()[1]

        self.rect.y += self.max_speed


class Ai(object):
    """
    The opponent controls his racket on the basis of observing the bll.
    """
    def __init__(self, racket, ball):
        self.ball = ball
        self.racket = racket

    def move(self):
        y = self.ball.rect.centery

        self.racket.move(y)

        if self.racket.rect.top <= 0:
            self.racket.rect.top = 0
        if self.racket.rect.bottom >= pygame.display.get_window_size()[1]:
            self.racket.rect.bottom = pygame.display.get_window_size()[1]
        


class Judge(object):
    """
    Game referee.
    """

    def __init__(self, board, ball, *args):
        self.ball = ball
        self.board = board
        self.rackets = args
        self.score = [0, 0]

        pygame.font.init()
        font_path = pygame.font.match_font('arial')
        self.font = pygame.font.Font(font_path, 64)

    def update_score(self, board_width):
        """
        If necessary, he assigns points and brings the ball to its original position.
        """
        if self.ball.rect.x <= 0:
            self.score[0] += 1
            self.ball.reset()
        elif self.ball.rect.x >= board_width-self.ball.width:
            self.score[1] += 1
            self.ball.reset()

    def draw_text(self, surface, text, x, y):
        """
        Draws the indicated text in the correct place.
        """
        text = self.font.render(text, True, (150, 150, 150))
        rect = text.get_rect()
        rect.center = x, y
        surface.blit(text, rect)

    def draw_on(self, surface):
        """
        Updates and draws the results.
        """
        width = self.board.surface.get_width()
        self.update_score(width)

        height = self.board.surface.get_height()
        self.draw_text(surface, "Player: {}".format(self.score[0]), width/2, height * 0.3)
        self.draw_text(surface, "Computer: {}".format(self.score[1]), width/2, height * 0.7)

if __name__ == "__main__":
    game = PongGame(800, 500)
    game.run()