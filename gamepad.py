import pygame
import time

# Inicia o módulo do pygame
pygame.init()

class Gamepad:
    
    def __init__(self):
        pygame.joystick.init()
        self.joysticks = []
        self.joystick_habilitado = False


    def event_gamepad(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks.append(joy)
                self.joystick_habilitado = True
            if event.type == pygame.JOYDEVICEREMOVED:
                self.joysticks = []
                self.joystick_habilitado = False
            time.sleep(0.02)
        return self.joystick_habilitado


    def geteventgamepad(self):
        return self.joystick_habilitado


    def getgamepadvalues(self):
        for joystick in self.joysticks:
            # player movement with analogue sticks
            eixo_esquerdax = round(joystick.get_axis(0), 2)
            eixo_esquerday = round(joystick.get_axis(1), 2)
            eixo_direitax = round(joystick.get_axis(2), 2)
            eixo_direitay = round(joystick.get_axis(3), 2)

            buttona = joystick.get_button(0)
            buttonb = joystick.get_button(1)
            buttony = joystick.get_button(3)
            buttonx = joystick.get_button(2)

            data = {"LY": eixo_esquerday, "LX": eixo_esquerdax, "RX": eixo_direitax, "RY": eixo_direitay,
                    "B": buttonb, "X": buttonx, "Y": buttony, "A": buttona}

            return data
