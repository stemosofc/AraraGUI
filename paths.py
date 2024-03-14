import getpass

username = getpass.getuser()


def returnpath(name):
    path = 'C:\\Users\\' + username + '\\PycharmProjects\\AraraDashboard\\Codes\\' + name + '/'
    comando = (r'cmd /c "python -m esptool --before default_reset --after hard_reset write_flash  -z --flash_mode dio '
               r'--flash_freq 80m --flash_size 4MB 0x1000 ' + path + name +
               r'.ino.bootloader.bin 0x8000 ' + path + name +
               r'.ino.partitions.bin 0xe000 ' +
               r'C:\Users\enzo\AppData\Local\Arduino15\packages\esp32\hardware\esp32\2.0.14/tools/partitions/boot_app0'
               r'.bin 0x10000 ' + path + name + r'.ino.bin')
    return comando
