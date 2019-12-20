class_file_path = 'Main.class'


def is_class(magic_code):
    return magic_code == 'cafebabe'


def read_constant_class(f, tag, index):
    name_index = int(f.read(2).hex(), 16)
    return {
        'tag': tag,
        'name_index': name_index,
        'index': index,
    }


def read_constant_ref(f, tag, index):
    class_index = int(f.read(2).hex(), 16)
    name_and_type_index = int(f.read(2).hex(), 16)
    return {
        'tag': tag,
        'class_index': class_index,
        'name_and_type_index': name_and_type_index,
        'index': index,
    }


def read_constant_string(f, tag, index):
    string_index = int(f.read(2).hex(), 16)
    return {
        'tag': tag,
        'string_index': string_index,
        'index': index
    }


def read_constant_num(f, tag, index):
    b = f.read(4)
    return {
        'tag': tag,
        'bytes': b,
        'index': index
    }


def read_constant_long_num(f, tag, index):
    hb = f.read(4)
    lb = f.read(4)
    return {
        'tag': tag,
        'high_bytes': hb,
        'low_bytes': lb,
        'index': index
    }


def read_constant_name_and_type(f, tag, index):
    name_index = int(f.read(2).hex(), 16)
    descriptor_index = int(f.read(2).hex(), 16)
    return {
        'tag': tag,
        'name_index': name_index,
        'descriptor_index': descriptor_index,
        'index': index
    }


def read_constant_utf8_info(f, tag, index):
    length = int(f.read(2).hex(), 16)
    string = f.read(length).decode('ascii')
    return {
        'tag': tag,
        'length': length,
        'string': string,
        'index': index
    }


tag_constant_map = {
    7: read_constant_class,
    9: read_constant_ref,  # Fieldref
    10: read_constant_ref,  # Methodref
    11: read_constant_ref,  # InterfaceMethodref,
    8: read_constant_string,
    3: read_constant_num,  # Integer
    4: read_constant_num,  # Float
    5: read_constant_long_num,  # Long
    6: read_constant_long_num,  # Double,
    12: read_constant_name_and_type,
    1: read_constant_utf8_info,
}


def read_access_flag(f):
    access_flags_hex = f.read(2).hex()
    access_flags = list()
    flags = {
        0: {
            '1': 'SYNTHETIC',
            '2': 'ANOOTATION',
            '4': 'ENUM'
        },
        1: {
            '2': 'INTERFACE',
            '4': 'ABSTRACT'
        },
        2: {
            '1': 'FINAL',
            '2': 'SUPER'
        },
        3: {
            '1': 'PUBLIC'
        }
    }
    for index in range(4):
        b = access_flags_hex[index]
        if b != '0':
            access_flags.append(
                flags[index][b]
            )
    return access_flags


def main():
    with open(class_file_path, 'rb') as f:
        magic_code = f.read(4).hex()
        if not is_class(magic_code):
            raise ValueError("not a valid class file")
        minor_version = int(f.read(2).hex(), 16)
        major_version = int(f.read(2).hex(), 16)
        constant_pool_count = int(f.read(2).hex(), 16)
        constant_pool = list()
        # start to read constant pool
        index = 1
        while index < constant_pool_count:
            tag = int(f.read(1).hex(), 16)
            parse_func = tag_constant_map[tag]
            constant_pool.append(parse_func(f, tag, index))
            index += 1
        access_flags = read_access_flag(f)
        this_class = int(f.read(2).hex(), 16)
        super_class = int(f.read(2).hex(), 16)
        interface_count = int(f.read(2).hex(), 16)
        # to be implemented
        # parse interfaces, fields, methods, attributes


if __name__ == '__main__':
    main()
