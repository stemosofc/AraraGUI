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
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks.append(joy)
            print("Habilitador")
            joystick_habilitado = True
        if event.type == pygame.JOYDEVICEREMOVED:
            joystick_habilitado = False
            print("AAAAA")
            pass
    return joystick_habilitado


def return_gamepad():
    return json.dumps({"Teste": ""})


# Retorna a leitura dos gamepad
def getjson():
    # event handler

    for joystick in joysticks:
        # player movement with analogue sticks
        eixo_esquerdax = round(joystick.get_axis(0), 3)
        eixo_esquerday = round(joystick.get_axis(1), 3)

        buttona = joystick.get_button(0)  # B
        buttonb = joystick.get_button(1)  # X
        buttony = joystick.get_button(3)  # Y
        buttonx = joystick.get_button(2)  # A

        data = {"LY": eixo_esquerday, "LX": eixo_esquerdax,
                "B": buttonb, "X": buttonx, "Y": buttony, "A": buttona}
        data = json.dumps(data)

        return data


def getjson_debugging():
    data = {"LeftAxisY": 1, "LeftAxisX": 1,
            "buttonB": 1, "buttonX": 1, "buttonY": 1, "buttonA": 1}
    data = json.dumps(data)

    return data
