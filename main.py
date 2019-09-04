import sys
import pygame

from Panel import Panel
from StateModule import State
from BasicModule import get_screen

def main():
    pygame.init()

    screen = get_screen()

    # objects
    state = State()
    panel = Panel(screen, state)
    listeners = panel.listener
    pygame.display.set_caption("Frank-Hertz Experiment Simulation")

    while True:
        screen.fill((100,170,220))
        panel.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            for listener in listeners:
                listener(event)
        pygame.display.flip()

if __name__ == "__main__":
    main()
