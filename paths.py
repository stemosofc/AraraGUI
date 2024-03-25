import os
import subprocess


# This is the function used in Arara V1.0
def returnpath_py(name):
    caminho_tool_esp32 = 'Codes/boot_app0.bin '
    path = 'Codes\\' + name + '/' + name
    esptool_name = 'esptool'
    caminho_diretorio = os.path.abspath('_internal')
    comando = (r'cmd /c "cd ' + caminho_diretorio + ' & python -m ' + esptool_name +
               ' --before default_reset --after hard_reset '
               r'write_flash -z --flash_mode '
               r'dio '
               r'--flash_freq 80m 0x1000 ' + path +
               r'.ino.bootloader.bin 0x8000 ' + path +
               r'.ino.partitions.bin 0xe000 ' + caminho_tool_esp32 + '0x10000 ' + path + r'.ino.bin"')
    return comando


# This is function used in Arara V1.1
def returnpath_exe(name):
    caminho_tool_esp32 = '_internal\\Codes/boot_app0.bin '
    path = '_internal\\Codes\\' + name + '/' + name
    comando = (r'cmd /c "_internal\Codes\esptool.exe '
               r'--before default_reset --after hard_reset write_flash  -z '
               r'--flash_mode dio 0x1000 ' + path + '.ino'
               r'--chip esp32 --baud 921600  --before default_reset --after hard_reset write_flash  -z '
               r'--flash_mode dio --flash_freq 80m --flash_size 4MB 0x1000 ' + path + '.ino'
               r'.bin"')
    return comando


# This function is used in Arara v1.1.2
def returnpath_exe_auto(name, caminho=""):
    caminho_tool_esp32 = caminho + 'Codes/boot_app0.bin '
    caminho_esptoolexe = caminho + "Codes\\esptool.exe"
    path = caminho + 'Codes\\' + name + '/' + name
    memory = [" 0x1000 ", " 0x8000 ", " 0xe000 ", " 0x10000 "]
    comando = (r'cmd /c "' + caminho_esptoolexe +
               r' --before default_reset --after hard_reset write_flash  -z '
               r'--flash_mode dio' + memory[0] + path + '.ino'
                                                        r'.bootloader.bin' + memory[1] + path + '.ino'
                                                                                                r'.partitions.bin' +
               memory[2] + caminho_tool_esp32 + memory[3] + path + '.ino'
                                                                   r'.bin"')
    return comando


def auto_command(name, caminho=""):
    caminho_tool_esp32 = caminho + 'Codes/boot_app0.bin '
    caminho_esptoolexe = caminho + "Codes\\esptool.exe"
    path = caminho + 'Codes\\' + name + '/' + name
    memory = [" 0x1000 ", " 0x8000 ", " 0xe000 ", " 0x10000 "]
    comando = (caminho_esptoolexe + r' --baud 921600 --before default_reset --after hard_reset write_flash  -z '
               r'--flash_mode dio' + memory[0] + path + '.ino'
               r'.bootloader.bin' + memory[1] + path + '.ino.partitions.bin' +
               memory[2] + caminho_tool_esp32 + memory[3] + path + '.ino.bin')
    return comando


def flash_code_arara(name, caminho=""):
    result = auto_command(name, caminho)
    result_command = subprocess.run(result.split(), capture_output=True, text=True)
    return found_error(result_command.stdout)


def found_error(output):
    if "a fatal error occurred:" in output.lower():
        return "Fatal Exception"
    else:
        return "Flash"
