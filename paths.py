import getpass
import os

username = getpass.getuser()


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
               r'--chip esp32 --baud 921600  --before default_reset --after hard_reset write_flash  -z '
               r'--flash_mode dio --flash_freq 80m --flash_size 4MB 0x1000 ' + path + '.ino'
               r'.bootloader.bin 0x8000 ' + path + '.ino'
               r'.partitions.bin 0xe000 ' + caminho_tool_esp32 + ' 0x10000 ' + path + '.ino'
               r'.bin"')
    return comando
