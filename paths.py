import getpass
import os
import esptool

username = getpass.getuser()


def returnpath(name):
    abs_esptool_path = os.path.abspath("_internal\\Codes/flash_arara.exe")
    caminho_tool_esp32 = '_internal\\Codes/boot_app0.bin '
    path = '_internal\\Codes\\' + name + '/' + name
    comando = (r'cmd /c ' + abs_esptool_path + ' --before default_reset --after hard_reset '
                                               r'write_flash -z --flash_mode '
                                               r'dio '
                                               r'--flash_freq 80m 0x1000 ' + path +
               r'.ino.bootloader.bin 0x8000 ' + path +
               r'.ino.partitions.bin 0xe000 ' + caminho_tool_esp32 + '0x10000 ' + path + r'.ino.bin')
    print(comando)
    return comando


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

# def returnpath_local(name):
#   caminho_tool_esp32 = 'Codes/boot_app0.bin '
#   path = 'Codes\\' + name + '/' + name
#   comando = (r'cmd /c ".venv\Scripts\flash_arara.exe --before '
#               r'default_reset --after hard_reset write_flash  -z --flash_mode dio '
#              r'--flash_freq 80m 0x1000 ' + path +
#              r'.ino.bootloader.bin 0x8000 ' + path +
#              r'.ino.partitions.bin 0xe000 ' + caminho_tool_esp32 + '0x10000 ' + path + r'.ino.bin'
#  return comando
