import os.path
import subprocess
from constants import AraraUpload as Upload

abpath = os.path.abspath('Codes') + "\\"
codes = os.listdir(abpath + "\\PlatformFiles")


# Função que faz upload de arquivos .ino
def auto_command(name, caminho=""):
    caminho_tool_esp32 = caminho + Upload.BOOT_APP
    caminho_esptoolexe = caminho + Upload.CAMINHO_ESPTOOL_DEV
    path = caminho + 'ArduinoFiles' + name + '/' + name

    comando = (caminho_esptoolexe + Upload.BAUD + Upload.CONFIG +
               Upload.MEMORY[0] + path + '.ino.bootloader.bin' +
               Upload.MEMORY[1] + path + '.ino.partitions.bin' +
               Upload.MEMORY[2] + caminho_tool_esp32 +
               Upload.MEMORY[3] + path + '.ino.bin')

    return comando


# Função que faz upload de arquivos criados no platformio
def auto_command_platformio(name="", caminho=""):
    caminho_esptoolexe = caminho + Upload.CAMINHO_ESPTOOL_DEV
    caminho_bootapp = caminho + Upload.BOOT_APP
    caminho_code = caminho + "PlatformFiles\\" + name + "\\"

    comando = (caminho_esptoolexe + Upload.BAUD + Upload.CONFIG +
               Upload.MEMORY[0] + caminho_code + "bootloader.bin" +
               Upload.MEMORY[1] + caminho_code + "partitions.bin" +
               Upload.MEMORY[2] + caminho_bootapp +
               Upload.MEMORY[3] + caminho_code + "firmware.bin")

    return comando


def flash_code_arara(name="", ferramenta=""):
    if ferramenta.lower() == "arduino":
        result = auto_command(name=name, caminho=abpath)
    else:
        result = auto_command_platformio(name=name, caminho=abpath)
    result_command = subprocess.run(result.split(), capture_output=True, text=True)
    return found_error(result_command.stdout)


# Função que retorna se algum erro ocorreu ou se o código foi upado com sucesso
def found_error(output):
    if "A fatal error occurred" in output:
        return "Fatal Exception"
    else:
        return "Flash"
