import sys
import pygame
import track as track

SCREEN_SIZE  = 980,720

SCREEN_SIZE

# Object dimensions
BRICK_WIDTH   = 60
BRICK_HEIGHT  = 15
#PADDLE_WIDTH  = 100
PADDLE_WIDTH = SCREEN_SIZE[0] / 3
PADDLE_HEIGHT = 12
BALL_DIAMETER = 16
BALL_RADIUS   = int (BALL_DIAMETER / 2)

MAX_PADDLE_X = SCREEN_SIZE[0] - PADDLE_WIDTH
MAX_BALL_X   = SCREEN_SIZE[0] - BALL_DIAMETER
MAX_BALL_Y   = SCREEN_SIZE[1] - BALL_DIAMETER

# Paddle Y coordinate
PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 10

# Color constants
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0,0,255)
BRICK_COLOR = (200,200,0)

# State constants
STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3

class Bricka:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Bricks-O-Bricks")

        self.clock = pygame.time.Clock()

        if pygame.font:
            self.font = pygame.font.Font(None,30)
        else:
            self.font = None

        self.init_game()


    def init_game(self):
        self.lives = 3
        self.score = 0
        self.state = STATE_BALL_IN_PADDLE

        self.paddle   = pygame.Rect(300,PADDLE_Y,PADDLE_WIDTH,PADDLE_HEIGHT)
        self.ball     = pygame.Rect(300,PADDLE_Y - BALL_DIAMETER,BALL_DIAMETER,BALL_DIAMETER)

        self.ball_vel = [5,-5]

        self.create_bricks()


    def create_bricks(self):
        y_ofs = 35
        self.bricks = []
        for i in range(10):
            x_ofs = 35
            for j in range(13):
                self.bricks.append(pygame.Rect(x_ofs,y_ofs,BRICK_WIDTH,BRICK_HEIGHT))
                x_ofs += BRICK_WIDTH + 10
            y_ofs += BRICK_HEIGHT + 5

    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, BRICK_COLOR, brick)

    def left_click(self):
        print('lckick')
        self.paddle.left -= 30
        if self.paddle.left < 0:
            self.paddle.left = 0
    
    def right_click(self):
        print('rckick')
        self.paddle.left += 30
        maxPaddleLeft = SCREEN_SIZE[0] - self.paddle.width
        if self.paddle.left > maxPaddleLeft:
            self.paddle.left = maxPaddleLeft

    def check_input(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1:
                    self.lives = 5
                if ev.key == pygame.K_q:
                    exit(1)
                # if ev.key == pygame.K_LEFT:
                #     left_click()
                # if ev.key == pygame.K_RIGHT:
                #     right_click()
                if ev.key == pygame.K_SPACE and self.state == STATE_BALL_IN_PADDLE:
                    self.ball_vel = [5,-5]
                    self.state = STATE_PLAYING
                elif ev.key == pygame.K_RETURN and (self.state == STATE_GAME_OVER or self.state == STATE_WON):
                    self.init_game()

    def move_ball(self):
        self.ball.left += self.ball_vel[0]
        self.ball.top  += self.ball_vel[1]

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MAX_BALL_X:
            self.ball.left = MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]

        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top >= MAX_BALL_Y:
            self.ball.top = MAX_BALL_Y
            self.ball_vel[1] = -self.ball_vel[1]

    def handle_collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += 3
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                break

        if len(self.bricks) == 0:
            self.state = STATE_WON

        if self.ball.colliderect(self.paddle):
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            else:
                self.state = STATE_GAME_OVER

    def show_stats(self):
        if self.font:
            font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives), False, WHITE)
            self.screen.blit(font_surface, (205,5))

    def show_message(self,message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message,False, WHITE)
            x = (SCREEN_SIZE[0] - size[0]) / 2
            y = (SCREEN_SIZE[1] - size[1]) / 2
            self.screen.blit(font_surface, (x,y))


    def frame(self):
        self.clock.tick(50)
        self.screen.fill(BLACK)
        self.check_input()

        if self.state == STATE_PLAYING:
            self.move_ball()
            self.handle_collisions()
        elif self.state == STATE_BALL_IN_PADDLE:
            self.ball.left = self.paddle.left + self.paddle.width / 2
            self.ball.top  = self.paddle.top - self.ball.height
            # self.show_message("PRESS SPACE TO LAUNCH THE BALL ")
            self.show_message("PRESS 1. Easy 2.Medium 3.Hard Q.Quit  PRESS SPACE TO LAUNCH THE BALL")
        elif self.state == STATE_GAME_OVER:
            self.show_message("GAME OVER. PRESS ENTER TO PLAY AGAIN")
        elif self.state == STATE_WON:
            self.show_message("YOU WON! PRESS ENTER TO PLAY AGAIN")

        self.draw_bricks()

        # Draw paddle
        pygame.draw.rect(self.screen, BLUE, self.paddle)

        # Draw ball
        pygame.draw.circle(self.screen, WHITE, (self.ball.left + BALL_RADIUS, self.ball.top + BALL_RADIUS), BALL_RADIUS)

        self.show_stats()

        pygame.display.flip()

    def run(self):
        track.leftHandler = lambda : self.left_click()
        track.rightHandler = lambda : self.right_click()
        while 1:
            self.frame()
            track.frame()


if __name__ == "__main__":
    Bricka().run()