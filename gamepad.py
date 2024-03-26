import json
import pygame

pygame.init()

# initialise the joystick module
pygame.joystick.init()
joysticks = []


def getjson():
    # event handler
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks.append(joy)
    for joystick in joysticks:
        # player movement with analogue sticks
        eixo_esquerdax = joystick.get_axis(0)
        eixo_esquerday = joystick.get_axis(1)

        buttona = joystick.get_button(0)  # B
        buttonb = joystick.get_button(1)  # X
        buttony = joystick.get_button(3)  # Y
        buttonx = joystick.get_button(2)  # A

        data = {"LeftAxisY": eixo_esquerday, "LeftAxisX": eixo_esquerdax,
                "buttonB": buttonb, "buttonX": buttonx, "buttonY": buttony, "buttonA": buttona}
        data = json.dumps(data)

        return data


def getjson_debugging():
    data = {"LeftAxisY": 1, "LeftAxisX": 1,
            "buttonB": 1, "buttonX": 1, "buttonY": 1, "buttonA": 1}
    data = json.dumps(data)

    return data
