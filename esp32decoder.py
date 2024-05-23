import argparse
import re
import os
import subprocess
import sys
from termcolor import colored

# update the following default values to what is relevant for your system
toolchain_default = (r"C:\Users\enzo\AppData\Local\Arduino15\packages\esp32\tools\xtensa-esp32-elf-gcc\esp-2021r2"
                     r"-patch5-8.4.0\bin")
elf_default = r"C:\Users\enzo\OneDrive\Documentos\PlatformIO\Projects\AraraPlaca\.pio\build\arara\firmware.elf"


class ESP32CrashParser(object):
    def __init__(self, toolchain_path, elf_path):
        self.toolchain_path = toolchain_path
        self.gdb_path = (r"C:\Users\enzo\AppData\Local\Arduino15\packages\esp32\tools\xtensa-esp32-elf-gcc\esp-2021r2"
                         r"-patch5-8.4.0\bin\xtensa-esp32-elf-gdb.exe")
        self.addr2line_path = (r"C:\Users\enzo\AppData\Local\Arduino15\packages\esp32\tools\xtensa-esp32-elf-gcc\esp"
                               r"-2021r2-patch5-8.4.0\bin\xtensa-esp32-elf-addr2line.exe")

        if not os.path.exists(self.gdb_path):
            raise Exception("GDB for ESP not found in {} - {} does not exist.\nUse --toolchain to point to "
                            "your toolchain folder.".format(self.toolchain_path, self.gdb_path))

        if not os.path.exists(self.addr2line_path):
            raise Exception("addr2line for ESP not found in {} - {} does not exist.\nUse --toolchain to point to "
                            "your toolchain folder.".format(self.toolchain_path, self.addr2line_path))

        self.elf_path = elf_path
        # if it is not an elf file we search the path for the newest elf file
        if not elf_path.endswith(".elf"):
            self.elf_path = self.find_newest_elf(elf_path)
        if not os.path.exists(self.elf_path):
            raise Exception("ELF file not found: '{}'".format(self.elf_path))

    def print_with_colors(self, text):
        method_start = text.find(":") + 1
        method_end = text.find(" at ")
        line_start = text.rindex(":") + 1
        address = text[2:method_start]
        method = text[method_start:method_end]
        middle = text[method_end:line_start]
        line_nr = text[line_start:]
        highlight_color = "light_yellow"
        print("    ", address, colored(method, "light_yellow"), middle, 'line', colored(line_nr, "light_yellow"))

    def parse_text(self, text):
        m = re.search('Backtrace: (.*)', text)
        if m:
            print()
            print("Stack trace:")
            print()
            for la in self.parse_stack(m.group(1)):
                self.print_with_colors(str(la))
            print()
        else:
            print("No stack trace found.")

    '''
    Decode one stack or backtrace.
    
    See: https://github.com/me-no-dev/EspExceptionDecoder/blob/master/src/EspExceptionDecoder.java#L402
    '''

    def parse_stack(self, text):
        r = re.compile('40[0-2][0-9a-fA-F]{5}')
        m = r.findall(text)
        return self.decode_function_addresses(m)

    def decode_function_address(self, address):
        args = [self.addr2line_path, "-e", self.elf_path, "-aipfC", address]
        return subprocess.check_output(args).strip()

    def decode_function_addresses(self, addresses):
        out = []
        for a in addresses:
            out.append(self.decode_function_address(a))
        return out

    '''
    GDB Should produce line number: https://github.com/me-no-dev/EspExceptionDecoder/commit/a78672da204151cc93979a96ed9f89139a73893f
    However it does not produce anything for me. So not using it for now.
    '''

    def decode_function_addresses_with_gdb(self, addresses):
        args = [self.gdb_path, "--batch"]

        # Disable user config file which might interfere here
        args.extend(["-iex", "set auto-load local-gdbinit off"])

        args.append(self.elf_path)

        args.extend(["-ex", "set listsize 1"])
        for address in addresses:
            args.append("-ex")
            args.append("l *0x{}".format(address))
        args.extend(["-ex", "q"])

        print("Running: {}".format(args))
        out = subprocess.check_output(args)
        print(out)

    @staticmethod
    def find_newest_elf(start_path):
        if start_path.endswith(".elf"):
            return start_path
        latest = 0
        result = ""
        for (dir_path, dir_names, file_names) in os.walk(start_path):
            for file_name in file_names:
                if file_name.endswith(".elf"):
                    file_path = os.path.join(dir_path, file_name)
                    time = os.path.getmtime(file_path)
                    if time > latest:
                        latest = time
                        result = file_path
        if result == "":
            print("No elf file found in ", start_path)
        else:
            print("elf =", result)
        return result


def main():
    print()
    parser = argparse.ArgumentParser()
    parser.add_argument("--toolchain", help="Path to the Xtensa toolchain",
                        default=toolchain_default)
    elf_file = ESP32CrashParser.find_newest_elf(elf_default)
    parser.add_argument("--elf", help="Path to the ELF file of the firmware", default=elf_file)
    parser.add_argument("input")
    args = parser.parse_args()

    crash_parser = ESP32CrashParser(args.toolchain, args.elf)
    crash_parser.parse_text(args.input)


if __name__ == '__main__':
    main()
