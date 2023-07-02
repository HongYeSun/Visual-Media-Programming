import pygame
import numpy as np
import os

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 1000
center = [WINDOW_WIDTH / 2., WINDOW_HEIGHT / 2.]
GRAY = (200, 200, 200)
BACK = (12, 22, 28)
WHITE = (255, 255, 255)

# assets 경로 설정
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')

# 이미지 로드
spaceship = pygame.image.load(os.path.join(assets_path, 'spaceship.png'))
spaceship = pygame.transform.scale(spaceship, (150, 150))

# pygame init
pygame.init()
pygame.display.set_caption("20191667 홍예선")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def Rmat(degree):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([ [c, -s, 0], [s, c, 0], [0, 0, 1]])
    return R

def Tmat(tx, ty):
    T = np.array([ [1, 0, tx], [0, 1, ty], [0, 0, 1]], dtype='float')
    return T

def getRegularPolygon(N, radius=1):
    v = np.zeros((N,2))
    for i in range(N):
        deg = i * 360. / N
        rad = deg * np.pi / 180.
        x = radius * np.cos(rad)
        y = radius * np.sin(rad)
        v[i] = [x, y]
    return v

def draw(M, points, color=(0,0,0), p0=None):
    R = M[0:2, 0:2]
    t = M[0:2, 2]

    points_transformed = (R @ points.T).T + t
    pygame.draw.polygon(screen, color, points_transformed, 2)
    if p0 is not None:
        pygame.draw.line(screen, WHITE, p0, points_transformed[0])

def main():
    Sun = getRegularPolygon(20, 60)
    Planet1 = getRegularPolygon(8, 50)
    Moon1 = getRegularPolygon(3, 30)
    Planet2 = getRegularPolygon(8, 50)
    Moon2_1 = getRegularPolygon(3, 20)
    Moon2_2 = getRegularPolygon(3, 30)
    Moon3 = getRegularPolygon(3, 10)

    angleS = 0.
    angleP1 = 0.
    angleP2 = 0.
    angleM1 = 0.
    angleM2_1 = 0.
    angleM2_2 = 0.
    angleM3 = 0.
    angleSP1 = 0.
    angleSP2 = 30.
    angleP1M1 = 0.
    angleP2M2_1 = 0.
    angleP2M2_2 = 60.
    angleM2_1M3 = 30.
    angleSS = 0.

    distSP1 = 200.
    distSP2 = 400.
    distP1M1 = 100.
    distP2M2_1 = 100.
    distP2M2_2 = 150.
    distM2_1M3 = 40.
    distSS = 400.

    done = False
    while not done:
        angleS += 10.
        angleP1 += 5.
        angleP2 += 3.
        angleM1 += 5.
        angleM2_1 += 4.
        angleM2_2 += 5.
        angleM3 += 3.
        angleSP1 += 2.
        angleSP2 += 3.
        angleP1M1 += 2.
        angleP2M2_1 += 3.
        angleP2M2_2 += 2.
        angleM2_1M3 += 3.
        angleSS += 5.

        # 1. event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        # 2. logic
        Msun = Tmat(center[0], center[1]) @ Rmat(angleS)
        x = center[0] + np.cos(angleSS * 2 * np.pi / 360) * distSS
        y = center[1] + np.sin(angleSS * 2 * np.pi / 360) * distSS * 1/2.

        MP1 = Tmat(center[0], center[1]) @ Rmat(angleSP1) @ Tmat(distSP1, 0) @ Rmat(-angleSP1 + angleP1)
        MM1 = MP1 @ Rmat(angleP1M1) @ Tmat(distP1M1, 0) @ Rmat(-angleP1M1 -angleP1 + angleM1)

        MP2 = Tmat(center[0], center[1]) @ Rmat(angleSP2) @ Tmat(distSP2, 0) @ Rmat(-angleSP2 + angleP2)
        MM2_1 = MP2 @ Rmat(angleP2M2_1) @ Tmat(distP2M2_1, 0) @ Rmat(-angleP2M2_1 -angleP2 + angleM2_1)
        MM2_2 = MP2 @ Rmat(angleP2M2_2) @ Tmat(distP2M2_2, 0) @ Rmat(-angleP2M2_2 -angleP2 + angleM2_2)
        MM3 = MM2_1 @ Rmat(angleM2_1M3) @ Tmat(distM2_1M3, 0) @ Rmat(-angleM2_1M3 -angleM2_2 + angleM3)
    
        # 3. drawing
        screen.fill(BACK)
        draw(Msun, Sun, (255, 255, 100), Msun[:2, 2])

        draw(MP1, Planet1, (100, 5, 50), MP1[:2, 2])
        draw(MM1, Moon1, (100, 100, 100), MM1[:2, 2])

        draw(MP2, Planet2, (100, 5, 50), MP2[:2, 2])
        draw(MM2_1, Moon2_1, (100, 100, 100), MM2_1[:2, 2])
        draw(MM2_2, Moon2_2, (100, 100, 100), MM2_2[:2, 2])
        draw(MM3, Moon3, (100, 100, 100), MM3[:2, 2])

        screen.blit(spaceship, [x, y])

        pygame.draw.circle(screen, WHITE, center, distSP1, width=1)
        pygame.draw.circle(screen, WHITE, center, distSP2, width=1)

        # 4.
        pygame.display.flip()
        clock.tick(30)

    pass


if __name__ == "__main__":
    main()