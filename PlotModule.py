import matplotlib
matplotlib.use('Agg')
import matplotlib.backends.backend_agg as agg
import pylab
import pygame
from pygame.locals import *

from BasicModule import BasicModule

class PlotModule(BasicModule):
    def __init__(self, screen, x, y, state):
        super(PlotModule, self).__init__(screen)

        self.x, self.y = x, y
        self.state = state
        self.fig = pylab.figure(figsize=[5, 4], dpi=50)
        self.ax = self.fig.gca()

    def update(self):
        if self.state.helper['plot']:
            self.ax.clear()
            for U, I in self.state.helper['UI'].items():
                self.ax.plot(U, I, 'r.')
            canvas = agg.FigureCanvasAgg(self.fig)
            canvas.draw()
            renderer = canvas.get_renderer()
            raw_data = renderer.tostring_rgb()
            size = canvas.get_width_height()
            surf = pygame.image.fromstring(raw_data, size, "RGB")
            self.screen.blit(surf, (self.x, self.y))

