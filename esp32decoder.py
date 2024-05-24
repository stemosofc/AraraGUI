import argparse
import re
import subprocess
from termcolor import colored

# update the following default values to what is relevant for your system
elf_default = r"C:\Users\enzo\OneDrive\Documentos\PlatformIO\Projects\AraraPlaca\.pio\build\arara\firmware.elf"


def print_with_colors(text):
    method_start = text.find(":") + 1
    method_end = text.find(" at ")
    line_start = text.rindex(":") + 1
    address = text[2:method_start]
    method = text[method_start:method_end]
    middle = text[method_end:line_start]
    line_nr = text[line_start:]
    print("    ", colored(address, "green"), colored(method, "red"), colored(middle, "yellow"), 'line',
          colored(line_nr, "magenta"))


class ESP32CrashParser(object):
    def __init__(self, elf_path):
        self.gdb_path = r"Codes/xtensa-esp32-elf-gdb.exe"
        self.addr2line_path = r"Codes/xtensa-esp32-elf-addr2line.exe"
        self.elf_path = elf_path

    def parse_text(self, text):
        m = re.search('Backtrace: (.*)', text)
        if m:
            print()
            print("Stack trace:")
            print()
            for la in self.parse_stack(m.group(1)):
                print_with_colors(str(la))
            print()
        else:
            print("No stack trace found.")

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()

    crash_parser = ESP32CrashParser(elf_default)
    crash_parser.parse_text(args.input)


main()
