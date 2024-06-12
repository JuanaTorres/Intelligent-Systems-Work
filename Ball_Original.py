#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import sys, pygame
from pygame.locals import *
import csv
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
import pandas as pd
 
# Constantes
WIDTH = 640
HEIGHT = 480
 
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
        self.choque=False
        
 
    def actualizar(self, time, pala_jug, pala_cpu):
        
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
            self.choque=False
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time
 
        if pygame.sprite.collide_rect(self, pala_jug):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
            self.choque=True
            
 
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
        #data=pd.read_csv("./informacion.csv")
        #data.head()
        #x=data.drop('Rebote_en_pala_jug',axis=1)
        #y=data['Rebote_en_pala_jug']
        #self.model = LogisticRegression()
 
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
    def ia_jugador(self, time, ball):
        posicion_y_pala_jug=0
        posicion_y_bola=0
        subir=0
        if ball.speed[0] <= 0 and ball.rect.centerx <= WIDTH / 2:
            posicion_y_pala_jug=self.rect.centery
            posicion_y_bola=ball.rect.centery
            if self.rect.centery < ball.rect.centery:
                self.rect.centery += self.speed * time
                subir=1
            if self.rect.centery > ball.rect.centery:
                self.rect.centery -= self.speed * time
                subir=0
            with open('informacion.csv', 'a+', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([posicion_y_pala_jug, posicion_y_bola, subir])
    def entrenar(self):
        data=pd.read_csv("./informacion.csv")
        data.head()
        x=data.drop('subir',axis=1)
        y=data['subir']
        self.model = LogisticRegression()
        self.model.fit(preprocessing.normalize(x), y)
        #self.model.fit(preprocessing.normalize(x), y)
        print('f(paddle_center, ball_center) = {} + {} * paddle_center + {} * ball_center'.format(
            round(self.model.intercept_[0], 4),
            round(self.model.coef_[0][0], 4),
            round(self.model.coef_[0][1], 4)
        ))
    def iaMover(self, time, ball):
        if ball.speed[0] <= 0 and ball.rect.centerx <= WIDTH / 2:
            paddle_center = self.rect.centery
            ball_center =ball.rect.centery

            prediction = self.model.predict(preprocessing.normalize([[paddle_center, ball_center]]))
            #prediction = self.model.predict(preprocessing.normalize([[paddle_center, ball_center]]))
            print('input: [{}, {}], prediction: {}'.format(paddle_center, ball_center, prediction))

            if prediction == 0:
                self.rect.centery -= self.speed * time
            if prediction == 1:
                self.rect.centery += self.speed * time


 
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
    pala_jug.entrenar()  # Añade los paréntesis para llamar al método
    pala_cpu.entrenar()
    clock = pygame.time.Clock()
    '''with open('informacion.csv', 'w+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Centro_pala_jug', 'Centro_bola', 'subir'])'''
    while True:
        
        
        time = clock.tick(60)
        keys = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
 
        bola.actualizar(time, pala_jug, pala_cpu)
        pala_jug.iaMover(time, bola)
        pala_cpu.ia(time, bola)
        screen.blit(background_image, (0, 0))
        screen.blit(bola.image, bola.rect)
        screen.blit(pala_jug.image, pala_jug.rect)
        screen.blit(pala_cpu.image, pala_cpu.rect)
        pygame.display.flip()
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()