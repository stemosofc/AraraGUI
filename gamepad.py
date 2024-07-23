import json
import pygame

# Inicia o módulo do pygame
pygame.init()

# initialise the joystick module
pygame.joystick.init()
joysticks = []
joystick_habilitado = False


def event_gamepad():
    global joystick_habilitado
    global joysticks
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks.append(joy)
            joystick_habilitado = True
        if event.type == pygame.JOYDEVICEREMOVED:
            joysticks = []
            joystick_habilitado = False
            pass
    return joystick_habilitado


# Retorna a leitura dos gamepad
def getgamepadvalues():
    # event handler

    for joystick in joysticks:
        # player movement with analogue sticks
        eixo_esquerdax = round(joystick.get_axis(0), 2)
        eixo_esquerday = round(joystick.get_axis(1), 2)
        eixo_direitax = round(joystick.get_axis(2), 2)
        eixo_direitay = round(joystick.get_axis(3), 2)

        buttona = joystick.get_button(0)  # B
        buttonb = joystick.get_button(1)  # X
        buttony = joystick.get_button(3)  # Y
        buttonx = joystick.get_button(2)  # A

        data = {"LY": eixo_esquerday, "LX": eixo_esquerdax, "RX": eixo_direitax, "RY": eixo_direitay,
                "B": buttonb, "X": buttonx, "Y": buttony, "A": buttona}
        data = json.dumps(data)

        return data
