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


def read_field_access_flags(f):
    access_flags_hex = f.read(2).hex()
    access_flags = list()
    flags = {
        0: {
            1: 'SYNTHETIC',
            4: 'ENUM',
        },
        2: {
            1: 'FINAL',
            4: 'VOLATILE',
            8: 'TRANSIENT'
        },
        3: {
            1: 'PUBLIC',
            2: 'PRIVATE',
            4: 'PROTECTED',
            8: 'STATIC'
        }
    }
    for index in range(len(access_flags_hex)):
        b = access_flags_hex[index]
        if index in flags:
            for flag in flags[index]:
                if int(b, 16) & flag != 0:
                    access_flags.append(flags[index][flag])
    return access_flags


def read_class_access_flags(f):
    access_flags_hex = f.read(2).hex()
    access_flags = list()
    flags = {
        0: {
            1: 'SYNTHETIC',
            2: 'ANOOTATION',
            4: 'ENUM'
        },
        1: {
            2: 'INTERFACE',
            4: 'ABSTRACT'
        },
        2: {
            1: 'FINAL',
            2: 'SUPER'
        },
        3: {
            1: 'PUBLIC'
        }
    }
    for index in range(len(access_flags_hex)):
        b = access_flags_hex[index]
        if index in flags:
            for flag in flags[index]:
                if int(b, 16) & flag != 0:
                    access_flags.append(flags[index][flag])
    return access_flags


def read_method_access_flag(f):
    access_flags_hex = f.read(2).hex()
    access_flags = list()
    flags = {
        0: {
            1: 'SYNTHETIC',
        },
        1: {
            1: 'NATIVE',
            4: 'ABSTRACT',
            8: 'STRICT',
        },
        2: {
            1: 'FINAL',
            2: 'SYNCHRONIZED',
            4: 'BRIDGE',
            8: 'VARARGS',
        },
        3: {
            1: 'PUBLIC',
            2: 'PRIVATE',
            4: 'PROTECTED',
            8: 'STATIC'
        }
    }
    for index in range(len(access_flags_hex)):
        b = access_flags_hex[index]
        if index in flags:
            for flag in flags[index]:
                if int(b, 16) & flag != 0:
                    access_flags.append(flags[index][flag])
    return access_flags


def read_field(f):
    access_flags = read_field_access_flags(f)
    name_index = int(f.read(2).hex(), 16)
    descriptor_index = int(f.read(2).hex(), 16)
    attributes_count = int(f.read(2).hex(), 16)
    index = 1
    attributes = list()
    while index < attributes_count:
        attribute = read_attributes(f)
        attributes.append(attribute)
    return {
        'access_flags': access_flags,
        'name_index': name_index,
        'descriptor_index': descriptor_index,
        'attributes_count': attributes_count,
        'attributes': attributes
    }


def read_method(f):
    access_flags = read_method_access_flag(f)
    name_index = int(f.read(2).hex(), 16)
    descriptor_index = int(f.read(2).hex(), 16)
    attributes_count = int(f.read(2).hex(), 16)
    index = 0
    attributes = list()
    while index < attributes_count:
        attribute = read_attributes(f)
        attributes.append(attribute)
        index += 1
    return {
        'access_flags': access_flags,
        'name_index': name_index,
        'descriptor_index': descriptor_index,
        'attributes_count': attributes_count,
        'attributes': attributes
    }


def read_attributes(f):
    attribute_name_index = int(f.read(2).hex(), 16)
    attribute_length = int(f.read(4).hex(), 16)
    info = f.read(attribute_length)
    return {
        'attribute_name_index': attribute_name_index,
        'attribute_length': attribute_length,
        'info': info
    }


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
        access_flags = read_class_access_flags(f)
        this_class = int(f.read(2).hex(), 16)
        super_class = int(f.read(2).hex(), 16)
        interface_count = int(f.read(2).hex(), 16)
        interfaces = list()
        index = 0
        while index < interface_count:
            interfaces.append(int(f.read(2).hex(), 16))
            index += 1
        fields_count = int(f.read(2).hex(), 16)
        fields = list()
        index = 0
        while index < fields_count:
            fields.append(read_field(f))
            index += 1
        methods_count = int(f.read(2).hex(), 16)
        methods = list()
        index = 0
        while index < methods_count:
            methods.append(read_method(f))
            index += 1
        attributes_count = int(f.read(2).hex(), 16)
        # to be implemented
        # parse attributes


if __name__ == '__main__':
    main()
