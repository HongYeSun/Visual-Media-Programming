import pygame
import pymunk
import pymunk.pygame_util
import time
import os
import math

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 690
PANEL = 50
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
ballsize = 35

# assets 경로 설정
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')

# pygame init
pygame.init()
pygame.display.set_caption("20191667 홍예선")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + PANEL))
clock = pygame.time.Clock()

# pymunk space
space = pymunk.Space()
static_body = space.static_body
draw_options = pymunk.pygame_util.DrawOptions(screen)

# image load
table_img = pygame.image.load(os.path.join(assets_path, 'table.jpg'))
table_img = pygame.transform.scale(table_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
cue_img = pygame.image.load(os.path.join(assets_path, 'cue.png'))
ball_imgs = []
for i in range(16):
  ball_img = pygame.image.load(os.path.join(assets_path, f'ball{i}.png'))
  ball_img = pygame.transform.scale(ball_img, (ballsize, ballsize))
  ball_imgs.append(ball_img)

# font
myFont = pygame.font.SysFont("arial", 30, True, False)
bigFont = pygame.font.SysFont("arial", 60, True, False)

def write(txt, font, color, x, y):
  img = font.render(txt, True, color)
  screen.blit(img, (x, y))

# function for creating balls
def create_ball(radius, pos):
  body = pymunk.Body()
  body.position = pos
  shape = pymunk.Circle(body, radius)
  shape.mass = 3
  shape.elasticity = 1.0
  # use pivot joint to add friction
  pivot = pymunk.PivotJoint(static_body, body, (0, 0), (0, 0))
  pivot.max_bias = 0 
  pivot.max_force = 1000 # emulate linear friction

  space.add(body, shape, pivot)
  return shape

# function for creating cushions
def create_cushion(poly_dims):
  body = pymunk.Body(body_type = pymunk.Body.STATIC)
  body.position = ((0, 0))
  shape = pymunk.Poly(body, poly_dims)
  shape.elasticity = 0.8
  
  space.add(body, shape)

# create pockets
pockets = [
  (112, 100),
  (600, 100),
  (1088, 100),
  (112, 588),
  (600, 588),
  (1088, 588)
]

# create cushions
cushions = [
  [(152, 101), (160, 117), (557, 117), (570, 101)], # upper left
  [(630, 101), (642, 117), (1038, 101), (1046, 101)], # upper right
  [(1088, 142), (1068, 150),(1068, 537), (1088, 547)], # right
  [(630, 588), (642, 572), (1038, 572), (1046, 588)], # lower right
  [(152, 588), (160, 572), (557, 572), (570, 588)], # lower left
  [(112, 142), (132, 150), (132, 537), (112, 547)] # left
]

# create pool cue
class Cue():
  def __init__(self, pos):
    self.original_image = cue_img
    self.angle = 0
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = pos

  def update(self, angle):
    self.angle = angle

  def draw(self, screen):
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    screen.blit(self.image,
      (self.rect.centerx - self.image.get_width() / 2,
      self.rect.centery - self.image.get_height() / 2)
     )

def ball_in_pocket(ball, pocket):
    ball_x_dist = abs(ball.body.position[0] - pocket[0])
    ball_y_dist = abs(ball.body.position[1] - pocket[1])
    ball_dist = math.sqrt((ball_x_dist ** 2) + (ball_y_dist ** 2))
    if ball_dist <= 75 / 2.:
        return True
    else:
        return False

def main():
    lives = 3
    cue_ball_reset = False
    potted_balls = []
    cue_angle = 90
    power = False
    force = 0
    max_force = 10000
    force_dir = 1
    moving = False

    # setup game balls
    balls = []
    rows = 5
    # cue ball
    pos = (888, WINDOW_HEIGHT / 2)
    cue_ball = create_ball(ballsize / 2, pos)
    balls.append(cue_ball)
    for col in range(5):
        for row in range(rows):
            pos = (250 + (col * ballsize), 262 + (row * ballsize) + (col * ballsize / 2))
            new_ball = create_ball(ballsize / 2., pos)
            balls.append(new_ball)
        rows -= 1

    power_bar = pygame.Surface((10, 20))
    power_bar.fill(RED)

    for c in cushions:
        create_cushion(c)

    cue = Cue(balls[0].body.position)
    
    done = False
    while not done:
        # fill background
        screen.fill(WHITE)
        # draw pool table
        screen.blit(table_img, (0, 0))
        
        # 1. event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                power = True
            if event.type == pygame.MOUSEBUTTONUP:
                power = False

        # 2. logic
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]

        # check if any balls have been potted
        for i, ball in enumerate(balls):
            for pocket in pockets:
                if ball_in_pocket(ball, pocket):
                    if i == 0: # cue ball
                        lives += -1
                        cue_ball_reset = True
                        ball.body.position = (-100, -100)
                        ball.body.velocity = (0.0, 0.0)
                    else:
                        space.remove(ball.body)
                        balls.remove(ball)
                        potted_balls.append(ball_imgs[i])
                        ball_imgs.pop(i)
        moving = False
        for ball in balls:
            if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0:
                moving = True
        
        # calculate pool cue angle
        mouse_pos = pygame.mouse.get_pos()
        cue.rect.center = balls[0].body.position
        x_dist = balls[0].body.position[0] - mouse_pos[0]
        y_dist = -(balls[0].body.position[1] - mouse_pos[1])
        cue_angle = math.degrees(math.atan2(y_dist, x_dist))    

        # draw balls
        for i, ball in enumerate(balls):
            screen.blit(ball_imgs[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

        # power up pool cue
        if power == True and moving == False:
            force += 100 * force_dir
            if force >= max_force or force <= 0:
                force_dir *= -1
            # draw power bars
            for i in range(math.ceil(force / 2000)):
                screen.blit(power_bar,
                (balls[0].body.position[0] - 30 + (i * 15),
                balls[0].body.position[1] + 30))
        elif power == False and moving == False:
            x_impulse = math.cos(math.radians(cue_angle))
            y_impulse = math.sin(math.radians(cue_angle))
            balls[0].body.apply_impulse_at_local_point((force * -x_impulse, force * y_impulse), (0, 0))
            force = 0
            force_direction = 1
        
        if cue_ball_reset == True:
            #reposition cue ball
            balls[0].body.position = (888, WINDOW_HEIGHT / 2)
            cue_ball_reset = False
        
        # 3. drawing
        # draw pannel
        pygame.draw.rect(screen, GRAY, (0, WINDOW_HEIGHT, WINDOW_WIDTH, PANEL))
        write("LIVES: " + str(lives), myFont, BLACK, WINDOW_WIDTH - 200, WINDOW_HEIGHT + 10)

        # draw potted balls
        for i, ball in enumerate(potted_balls):
            screen.blit(ball, (10 + (i * 50), WINDOW_HEIGHT + 10))

        # check for game over
        if lives <= 0:
            write("GAME OVER", bigFont, BLACK, WINDOW_WIDTH / 2 - 150, WINDOW_HEIGHT / 2 - 50)
            done = True

        # check if all balls are potted
        if len(balls) == 1:
            write(" YOU WIN!", bigFont, WHITE, WINDOW_WIDTH / 2 - 150, WINDOW_HEIGHT / 2 - 50)
            done = True

        cue.update(cue_angle)
        if(moving == False):
            cue.draw(screen)

        # 4.
        pygame.display.flip()
        clock.tick(60)
        space.step(1 / 60)

    time.sleep(1)
    pass

if __name__ == "__main__":
    main()