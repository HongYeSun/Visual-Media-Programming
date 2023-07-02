import pygame
import numpy as np

# pygame init
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 1000
center = [WINDOW_WIDTH / 2., WINDOW_HEIGHT / 2.]
GREEN = (100, 200, 100)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
pygame.display.set_caption("20191667 홍예선")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def getRegularPolygon(N, radius=1):
    v = np.zeros((N,2))
    for i in range(N):
        deg = i * 360. / N
        rad = deg * np.pi / 180.
        x = radius * np.cos(rad)
        y = radius * np.sin(rad)
        v[i] = [x, y]
    return v

def getClaw(width, height1, height2):
    points = np.array([[0, 0], [0, height1], 
                       [-width/2., height1], [-width/2., height1 + height2], 
                       [width/2., height1], [width/2., height1+ height2]], dtype='float')
    return points

def drawClaw(M, points, color):
    R = M[0:2, 0:2]
    t = M[0:2, 2]

    claw = (R @ points.T).T + t

    pygame.draw.line(screen, BLACK, claw[0], claw[1], 8)
    pygame.draw.line(screen, BLACK, claw[2], claw[3], 8)
    pygame.draw.line(screen, BLACK, claw[4], claw[5], 8)
    pygame.draw.line(screen, BLACK, claw[2], claw[4], 8)

def getRectangle(width, height, x=0, y=0):
    points = np.array([[0, height/2.], [0, -height/2.], [width, -height/2.], [width, height/2.]], dtype='float')
    return points

def Rmat(degree):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([ [c, -s, 0], 
                   [s, c, 0], 
                   [0, 0, 1]])
    return R

def Tmat(tx, ty):
    T = np.array([ [1, 0, tx], 
                   [0, 1, ty], 
                   [0, 0, 1]], dtype='float')
    return T

start = [WINDOW_WIDTH/2., 20.]
angle1 = 90.
width1 = 200
height1 = 70
rect1 = getRectangle(width1, height1)

gap12 = 30

angle2 = 0.
width2 = 200
height2 = 70
rect2 = getRectangle(width2, height2)

gap23 = 30

angle3 = 0.
width3 = 200
height3 = 70
rect3 = getRectangle(width3, height3, x=0, y=0)

claw_o = getClaw(100, 50, 30)
claw_c = getClaw(40, 50, 30)

select = 1
catch = False

def draw(M, points, color=(0,0,0), p0=None, flag=False):
    R = M[0:2, 0:2]
    t = M[0:2, 2]

    points_transformed = (R @ points.T).T + t
    if flag == False:
        pygame.draw.polygon(screen, color, points_transformed, 2)
    else:
        pygame.draw.polygon(screen, color, points_transformed)
    if p0 is not None:
        pygame.draw.line(screen, WHITE, p0, points_transformed[0])

done = False
while not done:
    # 1. event check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                select = 1
            elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                select = 2
            elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                select = 3
            
            if event.key == pygame.K_RIGHT:
                if select == 1:
                    angle1 -= 5
                elif select == 2:
                    angle2 -= 5
                else:
                    angle3 -= 5
            elif event.key == pygame.K_LEFT:
                if select == 1:
                    angle1 += 5
                elif select == 2:
                    angle2 += 5
                else:
                    angle3 += 5

            if event.key == pygame.K_SPACE:
                catch = not catch

            if event.key == pygame.K_ESCAPE:
                done = True
    #

    screen.fill(GRAY)

    # logic & draw
    M1 = np.eye(3) @ Tmat(start[0], start[1]) @ Rmat(angle1)
    draw(M1, rect1, RED, flag=(select == 1))
    
    M2 = M1 @ Tmat(width1 + gap12, 0) @ Rmat(angle2)
    draw(M2, rect2, YELLOW, flag=(select == 2))

    M3 = M2 @ Tmat(width2 + gap23, 0) @ Rmat(angle3)
    draw(M3, rect3, BLUE, flag=(select == 3))

    M4 = M3 @ Tmat(width3, 0) @ Rmat(270)
    if catch:
        drawClaw(M4, claw_c, BLACK)
    else:
        drawClaw(M4, claw_o, BLACK)
    
    # draw hinge
    pygame.draw.circle(screen, BLACK, start, 4)

    C = M1 @ Tmat(width1, 0)
    center1_1 = C[0:2, 2]
    pygame.draw.circle(screen, BLACK, center1_1, 4)
    C = C @ Tmat(gap12, 0)
    center1_2 = C[0:2, 2]
    pygame.draw.circle(screen, BLACK, center1_2, 4)
    pygame.draw.line(screen, BLACK, center1_1, center1_2, 1)

    C = M2 @ Tmat(width2, 0)
    center2_1 = C[0:2, 2]
    pygame.draw.circle(screen, BLACK, center2_1, 4)
    C = C @ Tmat(gap12, 0)
    center2_2 = C[0:2, 2]
    pygame.draw.circle(screen, BLACK, center2_2, 4)
    pygame.draw.line(screen, BLACK, center2_1, center2_2, 1)

    #
    pygame.display.flip()
    clock.tick(60)

# quit game
pygame.quit()
    