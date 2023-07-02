from datetime import datetime
import pygame
import numpy as np
import os

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 1000
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (99, 204, 255)
BLACK = (0, 0, 0)
ClockCenter = [WINDOW_WIDTH / 2., WINDOW_HEIGHT / 2.]
WIDTH_second = 250
HEIGHT_second = 3
WIDTH_minute = 200
HEIGHT_minute = 5
WIDTH_hour = 150
HEIGHT_hour = 10

now = datetime.now()

# pygame init
pygame.init()
pygame.display.set_caption("20191667 홍예선")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# assets 경로 설정
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')

# 효과음 로드
osound = pygame.mixer.Sound(os.path.join(assets_path, 'sound.wav'))

def getRectangle(width, height, x=0, y=0):
    points = np.array([[0    , height/2. ], 
                       [0    , -height/2.], 
                       [width, -height/2.], 
                       [width, height/2. ]], dtype='float')
    return points

def getRegularPolygonVertices(nv, r):
    v = []
    for i in range(nv):
        rad = (i - 2) * 2 * np.pi / nv
        x = np.cos(rad) * r
        y = np.sin(rad) * r
        v.append([x, y])
    vnp = np.array(v)
    return vnp

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

def draw(M, points, color=(0,0,0)):
    R = M[0:2, 0:2]
    t = M[0:2, 2]

    points_transformed = (R @ points.T).T + t
    
    pygame.draw.polygon(screen, color, points_transformed)

def main():
    timev = getRegularPolygonVertices(12, 300)

    for i in range (12):
        timev[i] += ClockCenter

    myFont = pygame.font.SysFont("arial", 30, True, False)

    sRect = getRectangle(WIDTH_second, HEIGHT_second)
    mRect = getRectangle(WIDTH_minute, HEIGHT_minute)
    hRect = getRectangle(WIDTH_hour, HEIGHT_hour)

    sdeg = -90. + now.second * 6.
    mdeg = -90. + now.minute * 6. + now.second * 0.1
    # sdeg = -90. + 55 * 6.
    # mdeg = -90. + 59 * 6. + 55 * 0.1
    hdeg = -90. + now.hour * 30. + now.minute * 0.5 + now.second * (0.5 / 60.)

    done = False
    while not done:
        # 1. event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        # 2. logic
        sdeg += 6. / 30.
        s3 = np.eye(3) @ Tmat(ClockCenter[0], ClockCenter[1]) @ Rmat(sdeg)

        mdeg += 0.1 / 30.
        m3 = np.eye(3) @ Tmat(ClockCenter[0], ClockCenter[1]) @ Rmat(mdeg)

        hdeg += (0.5 / 60.) / 30.
        h3 = np.eye(3) @ Tmat(ClockCenter[0], ClockCenter[1]) @ Rmat(hdeg)

        if sdeg > 269. and sdeg <= 270. and mdeg > 269. and mdeg <= 270:
            osound.play()

        # 3. drawing
        screen.fill(GRAY)
        pygame.draw.circle(screen, BLUE, ClockCenter, 350)
        draw(s3, sRect, (0,0,0))
        draw(m3, mRect, (0,0,0))
        draw(h3, hRect, (0,0,0))
        for i in range(12):
            timetxt = myFont.render(str(i + 1), True, BLACK)
            screen.blit(timetxt, (timev[i][0] - 8, timev[i][1] - 15))
        pygame.draw.circle(screen, (0, 0, 0), ClockCenter, 20)

        # 4.
        pygame.display.flip()
        clock.tick(30)

    pass


if __name__ == "__main__":
    main()
