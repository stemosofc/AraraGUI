class Janela:
    SIZE = "450x450"
    BACKGROUND = "#1a1a1a"
    TITLE = 'Arara v2.0'
    HIGHTLIGHTTHICKNESS = 0


class ButtonExit:
    POSICAO_Y = 200
    POSICAO_X = 311
    BACKGROUND = "#1a1a1a"
    HIGHTLIGHTTHICKNESS = 0
    BORDER_WIDTH = 0


class ButtonConnect:
    POSICAO_X = 13
    POSICAO_Y = 200
    BACKGROUND = "#1a1a1a"
    HIGHTLIGHTTHICKNESS = 0
    BORDER_WIDTH = 0


class ButtonUpload:
    POSICAO_Y = 200
    POSICAO_X = 162
    BACKGROUND = "#1a1a1a"
    HIGHTLIGHTTHICKNESS = 0
    BORDER_WIDTH = 0


class ButtonEnable:
    POSICAO_y = 120
    POSICAO_X = 162
    BACKGROUND = "#1a1a1a"
    HIGHTLIGHTTHICKNESS = 0
    BORDER_WIDTH = 0


class GamepadLabel:
    POSICAO_Y = 284
    POSICAO_X = 111
    BACKGROUND = "#1a1a1a"
    HIGHTLIGHTTHICKNESS = 0


class MenuBar:
    POSICAO_Y = 0
    POSICAO_X = 0
    WIDTH = 470
    HEIGHT = 60
    BACKGROUND = "#ffffff"
    HIGHLIGHT_COLOUR = "#fff"
    HIGHTLIGHTTHICKNESS = 0


class AraraLogo:
    BACKGROUND = "#ffffff"
    POSICAO_X_IMAGEM = 20
    POSICAO_Y_IMAGEM = 10
    BACKGROUND_TEXT = "#ffffff"
    POSICAO_X_TEXT = 75
    POSICAO_Y_TEXT = 22


class AraraError:
    TITLE = "Arara Error"
    MESSAGE_WIFI_DISCONNECT = "Não é possível utilizar esse comando! Verifique a conexão WiFi"
    GAMEPAD_WIFI_DISCONNECT = "Placa desconectada! Verifique o WiFi!"


class AraraWarnings:
    pass


class Ararainfo:
    pass


class AraraUpload:
    MEMORY = [" 0x1000 ", " 0x8000 ", " 0xe000 ", " 0x10000 "]
    CAMINHO_ESPTOOL_DEV = "esptool.exe"
    BAUD = " --baud 921600 "
    CONFIG = "--before default_reset --after hard_reset write_flash -z --flash_mode dio"
    BOOT_APP = "boot_app0.bin"
