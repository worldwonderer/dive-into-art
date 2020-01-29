"""
Main.dex

dx --dex --output=Main.dex io/github/worldwonderer/Main.class
"""


def is_dex(f):
    magic_code = f.read(4).decode()
    if magic_code != 'dex\n':
        raise ValueError("not a valid dex file")
    dex_version = f.read(4)[:3].decode()
    return dex_version


def read_header_item(f):
    dex_version = is_dex(f)
    checksum = f.read(4).hex()
    signature = f.read(20).hex()
    file_size = int(f.read(4)[::-1].hex(), 16)
    header_size = int(f.read(4)[::-1].hex(), 16)
    endian_tag = int(f.read(4).hex(), 16)
    if endian_tag != 0x78563412:
        raise ValueError("not a standard dex file")
    link_size = int(f.read(4)[::-1].hex(), 16)
    link_off = int(f.read(4)[::-1].hex(), 16)
    map_off = int(f.read(4)[::-1].hex(), 16)
    string_ids_size = int(f.read(4)[::-1].hex(), 16)
    string_ids_off = int(f.read(4)[::-1].hex(), 16)
    type_ids_size = int(f.read(4)[::-1].hex(), 16)
    type_ids_off = int(f.read(4)[::-1].hex(), 16)
    proto_ids_size = int(f.read(4)[::-1].hex(), 16)
    proto_ids_off = int(f.read(4)[::-1].hex(), 16)
    field_ids_size = int(f.read(4)[::-1].hex(), 16)
    field_ids_off = int(f.read(4)[::-1].hex(), 16)
    method_ids_size = int(f.read(4)[::-1].hex(), 16)
    method_ids_off = int(f.read(4)[::-1].hex(), 16)
    class_defs_size = int(f.read(4)[::-1].hex(), 16)
    class_defs_off = int(f.read(4)[::-1].hex(), 16)
    data_size = int(f.read(4)[::-1].hex(), 16)
    data_off = int(f.read(4)[::-1].hex(), 16)


def main(dex_file_path):
    with open(dex_file_path, 'rb') as f:
        # header_item
        read_header_item(f)


if __name__ == '__main__':
    main("Main.dex")
