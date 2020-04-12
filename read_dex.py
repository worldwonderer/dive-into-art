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


def read_uleb128(f):
    values = []
    value = int.from_bytes(f.read(1), byteorder='little', signed=False)
    values.append(value)
    while value >= 0x7f:
        value = int.from_bytes(f.read(1), byteorder='little', signed=False)
        values.append(value)
    i = len(values)
    result = 0
    values = values[::-1]
    for value in values:
        i = i - 1
        result |= (value & 0x7f) << (i * 7)
    return result


def read_string_id_items(f, offset, size):
    items = list()
    for i in range(size):
        f.seek(offset+4*i)
        item = read_string_id_item(f)
        items.append(item)
    return items


def read_string_id_item(f):
    string_data_off = struct.unpack('<I', f.read(4))[0]
    string_data_item = read_string_data_item(f, string_data_off)
    return {
        'string_data_off': string_data_off,
        'string_data_item': string_data_item
    }


def read_string_data_item(f, offset):
    f.seek(offset)
    utf16_size = read_uleb128(f)
    string_data = ''.join([t[0].decode() for t in struct.iter_unpack('<s', f.read(utf16_size))])
    return {
        'utf16_size': utf16_size,
        'string_data': string_data
    }


def read_type_id_items(f, offset, size):
    items = list()
    for i in range(size):
        f.seek(offset+4*i)
        item = read_type_id_item(f)
        items.append(item)
    return items


def read_type_id_item(f):
    descriptor_idx = struct.unpack('<I', f.read(4))[0]
    return {
        'descriptor_idx': descriptor_idx
    }


def read_proto_id_items(f, offset, size):
    items = list()
    for i in range(size):
        f.seek(offset+4*3*i)
        item = read_proto_id_item(f)
        items.append(item)
    return items


def read_proto_id_item(f):
    return {
        'shorty_idx': struct.unpack('<I', f.read(4))[0],
        'return_type_idx': struct.unpack('<I', f.read(4))[0],
        'parameters_off': struct.unpack('<I', f.read(4))[0]
    }


def read_field_id_item(f):
    return {
        'class_idx': struct.unpack('<H', f.read(2))[0],
        'type_idx': struct.unpack('<H', f.read(2))[0],
        'name_idx': struct.unpack('<I', f.read(4))[0]
    }


def read_field_id_items(f, offset, size):
    items = list()
    for i in range(size):
        f.seek(offset+4*2*i)
        item = read_field_id_item(f)
        items.append(item)
    return items


def read_method_id_item(f):
    return {
        'class_idx': struct.unpack('<H', f.read(2))[0],
        'proto_idx': struct.unpack('<H', f.read(2))[0],
        'name_idx': struct.unpack('<I', f.read(4))[0]
    }


def read_method_id_items(f, offset, size):
    items = list()
    for i in range(size):
        f.seek(offset+4*2*i)
        item = read_method_id_item(f)
        items.append(item)
    return items

def main(dex_file_path):
    with open(dex_file_path, 'rb') as f:
        # header_item
        size_off_map = read_header_item(f)
        # string_id_item
        size, off = size_off_map['string_ids_size'], size_off_map['string_ids_off']
        string_id_items = read_string_id_items(f, off, size)
        size, off = size_off_map['type_ids_size'], size_off_map['type_ids_off']
        type_id_items = read_type_id_items(f, off, size)
        size, off = size_off_map['proto_ids_size'], size_off_map['proto_ids_off']
        proto_id_items = read_proto_id_items(f, off, size)
        size, off = size_off_map['field_ids_size'], size_off_map['field_ids_off']
        field_id_items = read_field_id_items(f, off, size)
        size, off = size_off_map['method_ids_size'], size_off_map['method_ids_off']
        method_id_items = read_method_id_items(f, off, size)
        print(method_id_items)


if __name__ == '__main__':
    main("Main.dex")
