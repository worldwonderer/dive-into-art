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
    endian_prefix = '<' if ei_data == 1 else '>'
    ei_version = struct.unpack('<B', f.read(1))[0]
    ei_osabi = struct.unpack('<B', f.read(1))[0]
    ei_osabiversion = struct.unpack('<B', f.read(1))[0]
    return endian_prefix


def read_elf_header(f):
    endian_prefix = read_e_ident(f)
    f.seek(16)
    e_type = struct.unpack(endian_prefix+'H', f.read(2))[0]
    e_machine = struct.unpack(endian_prefix+'H', f.read(2))[0]
    e_version = struct.unpack(endian_prefix+'I', f.read(4))[0]
    e_entry = struct.unpack(endian_prefix+'Q', f.read(8))[0]
    e_phoff = struct.unpack(endian_prefix+'Q', f.read(8))[0]
    e_shoff = struct.unpack(endian_prefix+'Q', f.read(8))[0]
    e_flags = struct.unpack(endian_prefix+'I', f.read(4))[0]
    e_ehsize = struct.unpack(endian_prefix+'H', f.read(2))[0]
    e_phentsize = struct.unpack(endian_prefix+'H', f.read(2))[0]
    e_phnum = struct.unpack(endian_prefix+'H', f.read(2))[0]
    e_shentsize = struct.unpack(endian_prefix+'H', f.read(2))[0]
    e_shnum = struct.unpack(endian_prefix+'H', f.read(2))[0]
    e_shtrndx = struct.unpack(endian_prefix+'H', f.read(2))[0]
    return endian_prefix, e_shoff, e_shnum, e_phoff, e_phnum


def read_program_header_table(f, off, size, endian_prefix):
    f.seek(off)
    for _ in range(size):
        p_type = struct.unpack(endian_prefix+'I', f.read(4))[0]
        p_flags = struct.unpack(endian_prefix+'I', f.read(4))[0]
        p_offset = struct.unpack(endian_prefix+'Q', f.read(8))[0]
        p_vaddr = struct.unpack(endian_prefix+'Q', f.read(8))[0]
        p_paddr = struct.unpack(endian_prefix+'Q', f.read(8))[0]
        p_filesz = struct.unpack(endian_prefix+'Q', f.read(8))[0]
        p_memsz = struct.unpack(endian_prefix+'Q', f.read(8))[0]
        p_align = struct.unpack(endian_prefix+'Q', f.read(8))[0]
        current = f.tell()
        data = read_data(f, p_offset, p_filesz)
        f.seek(current)


def read_section_header_table(f, off, size, endian_prefix):
    f.seek(off)
    for _ in range(size):
        sh_name = struct.unpack(endian_prefix+'I', f.read(4))[0]
        sh_type = struct.unpack(endian_prefix+'I', f.read(4))[0]
        sh_flags = struct.unpack(endian_prefix+'Q', f.read(8))[0]
        sh_addr = struct.unpack(endian_prefix+'Q', f.read(8))[0]
        sh_offset = struct.unpack(endian_prefix+'Q', f.read(8))[0]
        sh_size = struct.unpack(endian_prefix+'Q', f.read(8))[0]
        sh_link = struct.unpack(endian_prefix+'I', f.read(4))[0]
        sh_info = struct.unpack(endian_prefix+'I', f.read(4))[0]
        sh_addralign = struct.unpack(endian_prefix+'Q', f.read(8))[0]
        sh_entsize = struct.unpack(endian_prefix+'Q', f.read(8))[0]
        current = f.tell()
        data = read_data(f, sh_offset, sh_size)
        f.seek(current)


def read_data(f, off, size):
    f.seek(off)
    return b''.join([t[0] for t in struct.iter_unpack('<s', f.read(size))])


def main(so_file_path):
    with open(so_file_path, 'r+b') as f:
        with mmap.mmap(f.fileno(), 0) as mm:
            endian_prefix, shoff, shnum, phoff, phsize = read_elf_header(mm)
            read_program_header_table(mm, phoff, phsize, endian_prefix)
            read_section_header_table(mm, shoff, shnum, endian_prefix)


if __name__ == '__main__':
    main("main.so")
