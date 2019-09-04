import pygame
import sys

from BasicModule import BasicModule, get_screen
from RectModule import LabelModule, ButtonModule, DisplayModule
from ScrollBarModule import ScrollBarModule
from StateModule import State
from Tube import Tube
from PlotModule import PlotModule

class VoltageControler(BasicModule):
    def __init__(self, screen, x, y, text, max_value, state):
        super(VoltageControler, self).__init__(screen)

        label = LabelModule(screen, x=x, y=y, text=text)
        scrollbar = ScrollBarModule(screen, x=x+60, y=y, max_value=max_value, set_value=state.set_param(text))
        digit_displayer = DisplayModule(screen, x=x+210, y=y, get_text=lambda:"{:.2f}".format(getattr(state, text)))

        self.add_sub_module('label', label)
        self.add_sub_module('scrollbar', scrollbar)
        self.add_sub_module('digit_displayer', digit_displayer)

    def update(self):
        self.sub_module.label.show_text()
        self.sub_module.scrollbar.update()
        self.sub_module.digit_displayer.update()
        self.sub_module.digit_displayer.show_text()


class CurrentDisplayer(BasicModule):
    def __init__(self, screen, x, y, state):
        super(CurrentDisplayer, self).__init__(screen)

        self.add_sub_module('current_displayer',
                            DisplayModule(screen, x=x+20, y=y+20,
                                          get_text=lambda:"{:.2f}".format(getattr(state, 'Ie'))))
        self.add_sub_module('plot_button', ButtonModule(screen, x=x+180, y=y+20, state=state))
        self.add_sub_module('plot', PlotModule(screen, x=x+20, y=y+80, state=state))

    def update(self):
        self.sub_module.current_displayer.update()
        self.sub_module.current_displayer.show_text()
        self.sub_module.plot_button.update()
        self.sub_module.plot_button.show_button()
        self.sub_module.plot.update()




class Panel(BasicModule):
    def __init__(self, screen, state):
        super(Panel, self).__init__(screen)

        self.add_sub_module('Uf', VoltageControler(screen, x=10, y=320, text='Uf', max_value=1, state=state))
        self.add_sub_module('Ug', VoltageControler(screen, x=10, y=400, text='Ug', max_value=3, state=state))
        self.add_sub_module('Ua', VoltageControler(screen, x=10, y=480, text='Ua', max_value=60, state=state))
        self.add_sub_module('Ue', VoltageControler(screen, x=10, y=560, text='Ue', max_value=15, state=state))

        self.add_sub_module('Ie', CurrentDisplayer(screen, x=300, y=300, state=state))

        self.add_sub_module('tube', Tube(screen, state))

    def update(self):
        for sub_module in self.sub_module.values():
            sub_module.update()

def test():
    pygame.init()

    screen = get_screen()

    # objects
    state = State()
    panel = Panel(screen, state)
    listeners = panel.listener
    pygame.display.set_caption("test_label_module")

    while True:
        screen.fill((123,234,213))
        panel.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            for listener in listeners:
                listener(event)
        pygame.display.flip()


if __name__ == "__main__":
    test()