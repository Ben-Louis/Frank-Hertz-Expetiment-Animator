import pygame
from ParticalModule import Atom, Electron
from BasicModule import BasicModule
from pygame.sprite import Group
import random
from math import pi, sin, cos

class Tube(BasicModule):
    def __init__(self, screen, state):
        super(Tube, self).__init__(screen)
        self.state = state

        self.line_up = pygame.draw.line(self.screen, (0,0,0), (20, 20), (580, 20))
        self.line_down = pygame.draw.line(self.screen, (0,0,0), (20, 280), (580, 280))
        self.line_collect = pygame.draw.line(self.screen, (0,0,0), (560, 20), (560, 280))
        self.line_arid = pygame.draw.line(self.screen, (100,100,100), (440, 40), (440, 260))
        self.line_control = pygame.draw.line(self.screen, (100,100,100), (140, 40), (140, 260))

        self.image = pygame.image.load('images/light.png')
        self.image_rect = self.image.get_rect()
        self.image_rect.centery = 150
        self.image_rect.centerx = 20

        self.atoms = Group()
        self.electrons = Group()

        self.generate_atoms()
        self.delete_electrons = []
        self.collected_electrons = []

    def draw(self):
        self.screen.blit(self.image, self.image_rect)
        self.screen.fill((0, 0, 0), self.line_up)
        self.screen.fill((0, 0, 0), self.line_down)
        self.screen.fill((0, 0, 0), self.line_collect)
        self.screen.fill((100,100,100), self.line_arid)
        self.screen.fill((100,100,100), self.line_control)

    def generate_atoms(self):
        for _ in range(300):
            self.atoms.add(Atom(self.screen, x=random.random()*500+40, y=random.random()*240+30))

    def generate_electrons(self, ratio):
        for _ in range(2):
            if random.random() < ratio:
                self.electrons.add(Electron(self.screen, x=random.random()*60+20, y=random.random()*60+120, tube=self))


    def update(self):
        self.draw()
        self.atoms.update()
        self.electrons.update()
        for e in self.delete_electrons:
            self.electrons.remove(e)
        self.generate_electrons(ratio=self.state.Uf)

        # collide
        if random.random() > 0:
            collisions = pygame.sprite.groupcollide(self.electrons, self.atoms, False, False, collided=collided)
            for e, atoms in collisions.items():
                v = e.velocity
                v0 = 16.7
                theta = 2 * pi * random.random()
                # elastic
                if v < v0 or random.random() < 0.2:                    
                    e.vx = v * cos(theta)
                    e.vy = v * sin(theta)
                # non-elastic
                else:
                    e.vx = (v**2-v0**2)**0.5 * cos(theta)
                    e.vy = (v**2-v0**2)**0.5 * sin(theta)
                    for a in atoms:
                        a.activate_step = 100

        if len(self.collected_electrons) > 10:
            self.state.Ie = float(len(self.collected_electrons)) / (self.collected_electrons[-1] - self.collected_electrons[0])
            if self.state.helper['plot']:
                I = self.state.helper['UI'].get(self.state.Ua, 0)
                if I > 0:
                    self.state.helper['UI'][self.state.Ua] = I*0.9 + self.state.Ie*0.1
                else:
                    self.state.helper['UI'][self.state.Ua] = self.state.Ie



def collided(e, a):
    dist = ((e.ball_rect.centerx - a.ball_rect.centerx) ** 2 + (e.ball_rect.centery - a.ball_rect.centery) ** 2) ** 0.5
    return dist < 4