"""
main.so

gcc -fPIC -shared main.c -o main.so
"""
import mmap
import struct


def is_elf(f):
    magic_code = f.read(4)
    if magic_code != b'\x7fELF':
        raise ValueError("not a valid elf file")


def read_e_ident(f):
    is_elf(f)
    ei_class = struct.unpack('<B', f.read(1))[0]
    ei_data = struct.unpack('<B', f.read(1))[0]
    ei_version = struct.unpack('<B', f.read(1))[0]
    ei_osabi = struct.unpack('<B', f.read(1))[0]
    ei_osabiversion = struct.unpack('<B', f.read(1))[0]


def read_elf_header(f):
    read_e_ident(f)
    f.seek(16)
    e_type = struct.unpack('<H', f.read(2))[0]
    e_machine = struct.unpack('<H', f.read(2))[0]
    e_version = struct.unpack('<I', f.read(4))[0]
    e_entry = struct.unpack('<Q', f.read(8))[0]
    e_phoff = struct.unpack('<Q', f.read(8))[0]
    e_shoff = struct.unpack('<Q', f.read(8))[0]
    e_flags = struct.unpack('<I', f.read(4))[0]
    e_ehsize = struct.unpack('<H', f.read(2))[0]
    e_phentsize = struct.unpack('<H', f.read(2))[0]
    e_phnum = struct.unpack('<H', f.read(2))[0]
    e_shentsize = struct.unpack('<H', f.read(2))[0]
    e_shnum = struct.unpack('<H', f.read(2))[0]
    e_shtrndx = struct.unpack('<H', f.read(2))[0]


def main(so_file_path):
    with open(so_file_path, 'r+b') as f:
        with mmap.mmap(f.fileno(), 0) as mm:
            read_elf_header(mm)


if __name__ == '__main__':
    main("main.so")
