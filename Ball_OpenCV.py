#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import sys, pygame
from pygame.locals import *

#Required for screen shots
import pyautogui
import cv2
import numpy as np
 
# Constantes
WIDTH = 640
HEIGHT = 480
LEFT = 675
TOP = 280
 
# Clases
# ---------------------------------------------------------------------
 
class Bola(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/ball.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed = [0.5, -0.5]
 
    def actualizar(self, time, pala_jug, pala_cpu):
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time
 
        if pygame.sprite.collide_rect(self, pala_jug):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
 
        if pygame.sprite.collide_rect(self, pala_cpu):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
 
class Pala(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/pala.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = HEIGHT / 2
        self.speed = 0.5
 
    def mover(self, time, keys):
        if self.rect.top >= 0:
            if keys[K_UP]:
                self.rect.centery -= self.speed * time
        if self.rect.bottom <= HEIGHT:
            if keys[K_DOWN]:
                self.rect.centery += self.speed * time
 
    def ia(self, time, ball):
        if ball.speed[0] >= 0 and ball.rect.centerx >= WIDTH/2:
            if self.rect.centery < ball.rect.centery:
                self.rect.centery += self.speed * time
            if self.rect.centery > ball.rect.centery:
                self.rect.centery -= self.speed * time
 
# ---------------------------------------------------------------------
 
# Funciones
# ---------------------------------------------------------------------
 
def load_image(filename, transparent=False):
        try: image = pygame.image.load(filename)
        except pygame.error:
                raise SystemExit
        image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
        return image
 
# ---------------------------------------------------------------------
 
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pruebas Pygame")
 
    background_image = load_image('images/fondo_pong.png')
    bola = Bola()
    pala_jug = Pala(30)
    pala_cpu = Pala(WIDTH - 30)
 
    clock = pygame.time.Clock()

    i = 0
    image = pyautogui.screenshot(region=(LEFT,TOP, WIDTH, HEIGHT))
    image_new = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    alfa = 0.5
    beta = 1 - alfa

    while True:
        time = clock.tick(60)
        keys = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
 
        bola.actualizar(time, pala_jug, pala_cpu)
        pala_jug.mover(time, keys)
        pala_cpu.ia(time, bola)
        screen.blit(background_image, (0, 0))
        screen.blit(bola.image, bola.rect)
        screen.blit(pala_jug.image, pala_jug.rect)
        screen.blit(pala_cpu.image, pala_cpu.rect)
        pygame.display.flip()
        #pyautogui.screenshot(region=(365,180, 630, 440)).save(r'screen_shots/scrshot'+str(i)+ '.png')
        image_old = image_new
        image = pyautogui.screenshot(region=(LEFT,TOP, WIDTH, HEIGHT))
        image_new = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        dst = cv2.addWeighted(image_old, alfa, image_new, beta, 0.0)
        cv2.imwrite(r'screen_shots/scrshot'+ str(i)+ '.png', dst)

        i = i + 1
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()