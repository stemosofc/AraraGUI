import getpass

username = getpass.getuser()
caminho_tool_esp32 = 'C:\\Users\\enzo\\PycharmProjects\\AraraDashboard\\Codes\\boot_app0.bin '


def returnpath(name):
    path = 'C:\\Users\\' + username + '\\PycharmProjects\\AraraDashboard\\Codes\\' + name + '/'
    comando = (r'cmd /c "python -m esptool --before default_reset --after hard_reset write_flash  -z --flash_mode dio '
               r'--flash_freq 80m 0x1000 ' + path + name +
               r'.ino.bootloader.bin 0x8000 ' + path + name +
               r'.ino.partitions.bin 0xe000 ' + caminho_tool_esp32 + '0x10000 ' + path + name + r'.ino.bin')
    return comando
