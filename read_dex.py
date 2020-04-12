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


def read_parameters(f, off):
    f.seek(off)
    size = struct.unpack('<I', f.read(4))[0]
    type_item_list = list()
    for i in range(size):
        type_item_list.append({'type_idx': struct.unpack('<H', f.read(2))[0]})
    return {
        'size': size,
        'type_item_list': type_item_list
    }


def read_proto_id_item(f):
    item = {
        'shorty_idx': struct.unpack('<I', f.read(4))[0],
        'return_type_idx': struct.unpack('<I', f.read(4))[0],
        'parameters_off': struct.unpack('<I', f.read(4))[0],
    }
    if item['parameters_off'] != 0:
        item['parameters'] = read_parameters(f, item['parameters_off'])
    return item


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


def read_class_def_items(f, offset, size):
    items = list()
    for i in range(size):
        f.seek(offset+4*8*i)
        item = read_class_def_item(f)
        items.append(item)
    return items


def read_class_def_item(f):
    item = {
        'class_idx': struct.unpack('<I', f.read(4))[0],
        'access_flags': struct.unpack('<I', f.read(4))[0],
        'superclass_idx': struct.unpack('<I', f.read(4))[0],
        'interfaces_off': struct.unpack('<I', f.read(4))[0],
        'source_file_idx': struct.unpack('<I', f.read(4))[0],
        'annotations_off': struct.unpack('<I', f.read(4))[0],
        'class_data_off': struct.unpack('<I', f.read(4))[0],
        'static_values_off': struct.unpack('<I', f.read(4))[0],
    }
    item['class_data'] = read_class_data(f, item['class_data_off'])
    return item


def read_class_data(f, off):
    f.seek(off)
    static_fields_size = read_uleb128(f)
    instance_fields_size = read_uleb128(f)
    direct_methods_size = read_uleb128(f)
    virtual_methods_size = read_uleb128(f)
    static_fields = list()
    for i in range(static_fields_size):
        static_fields.append({
            'field_ifx_diff': read_uleb128(f),
            'access_flags': read_uleb128(f)
        })
    instance_fields = list()
    for i in range(instance_fields_size):
        instance_fields.append({
            'field_ifx_diff': read_uleb128(f),
            'access_flags': read_uleb128(f)
        })
    direct_methods = list()
    for i in range(direct_methods_size):
        item = {
            'method_idx_diff': read_uleb128(f),
            'access_flags': read_uleb128(f),
            'code_off': read_uleb128(f)
        }
        current_offset = f.tell()
        item['code'] = read_code(f, item['code_off'])
        f.seek(current_offset)
        direct_methods.append(item)
    virtual_methods = list()
    for i in range(virtual_methods_size):
        item = {
            'method_idx_diff': read_uleb128(f),
            'access_flags': read_uleb128(f),
            'code_off': read_uleb128(f)
        }
        current_offset = f.tell()
        item['code'] = read_code(f, item['code_off'])
        f.seek(current_offset)
        virtual_methods.append(item)
    return {
        'static_fields_size': static_fields_size,
        'instance_fields_size': instance_fields_size,
        'direct_methods_size': direct_methods_size,
        'virtual_methods_size': virtual_methods_size,
        'static_fields': static_fields,
        'instance_fields': instance_fields,
        'direct_methods': direct_methods,
        'virtual_methods': virtual_methods
    }


def read_code(f, off):
    f.seek(off)
    item = {
        'registers_size': struct.unpack('<H', f.read(2))[0],
        'ins_size': struct.unpack('<H', f.read(2))[0],
        'outs_size': struct.unpack('<H', f.read(2))[0],
        'tries_size': struct.unpack('<H', f.read(2))[0],
        'debug_info_off': struct.unpack('<I', f.read(4))[0],
        'debug_info': dict(),
        'insns_size': struct.unpack('<I', f.read(4))[0],
        'insns': list()
    }
    for i in range(item['insns_size']):
        item['insns'].append(struct.unpack('<H', f.read(2))[0])
    f.seek(item['debug_info_off'])
    item['debug_info'] = {
        'line_start': read_uleb128(f),
        'parameters_size': read_uleb128(f),
        'opcode': list(),
    }
    for i in range(3):
        item['debug_info']['opcode'].append(f.read(1)[0])
    return item


def read_dex_map(f, off):
    f.seek(off)
    size = struct.unpack('<I', f.read(4))[0]
    dex_map_list = list()
    for i in range(size):
        dex_map_list.append({
            'type': struct.unpack('<H', f.read(2))[0],
            'unused': struct.unpack('<H', f.read(2))[0],
            'size': struct.unpack('<I', f.read(4))[0],
            'offset': struct.unpack('<I', f.read(4))[0],
        })
    return {
        'size': size,
        'dex_map_list': dex_map_list
    }


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
        size, off = size_off_map['class_defs_size'], size_off_map['class_defs_off']
        class_defs_items = read_class_def_items(f, off, size)
        dex_map = read_dex_map(f, size_off_map['map_off'])


if __name__ == '__main__':
    main("Main.dex")
