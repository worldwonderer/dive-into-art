"""
Main.dex

dx --dex --output=Main.dex io/github/worldwonderer/Main.class
"""
import struct


def is_dex(f):
    magic_code = f.read(4).decode()
    if magic_code != 'dex\n':
        raise ValueError("not a valid dex file")
    dex_version = f.read(4)[:3].decode()
    return dex_version


def read_header_item(f):
    dex_version = is_dex(f)
    checksum = hex(struct.unpack('<I', f.read(4))[0])
    signature = f.read(20).hex()
    file_size = struct.unpack('<I', f.read(4))[0]
    header_size = struct.unpack('<I', f.read(4))[0]
    endian_tag = struct.unpack('<I', f.read(4))[0]
    if endian_tag != 0x12345678:
        raise ValueError("not a little indian dex file")
    size_off_map = dict()
    for name in ['link_size', 'link_off', 'map_off', 'string_ids_size', 'string_ids_off',
                 'type_ids_size', 'type_ids_off', 'proto_ids_size', 'proto_ids_off',
                 'field_ids_size', 'field_ids_off', 'method_ids_size', 'method_ids_off',
                 'class_defs_size', 'class_defs_off', 'data_size', 'data_off']:
        size_off_map[name] = struct.unpack('<I', f.read(4))[0]
    return size_off_map


def read_string_id_item(f, offset, size):
    f.seek(offset)


def read_string_data_item(f, offset):
    pass


def main(dex_file_path):
    with open(dex_file_path, 'rb') as f:
        # header_item
        size_off_map = read_header_item(f)
        # string_id_item
        size, off = size_off_map['string_ids_size'], size_off_map['string_id_off']
        read_string_id_item(f, off, size)


if __name__ == '__main__':
    main("Main.dex")
