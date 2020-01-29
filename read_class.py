"""
Main.class

javac Main.java .
"""
constant_pool = list()


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
        'bytes': string,
        'index': index
    }


def read_constant_method_handle_info(f, tag, index):
    reference_kind = int(f.read(1).hex(), 16)
    reference_index = int(f.read(2).hex(), 16)
    return {
        'tag': tag,
        'reference_kind': reference_kind,
        'reference_index': reference_index,
        'index': index
    }


def read_constant_method_type_info(f, tag, index):
    descriptor_index = int(f.read(2).hex(), 16)
    return {
        'tag': tag,
        'descriptor_index': descriptor_index,
        'index': index
    }


def read_invoke_dynamic_info(f, tag, index):
    bootstrap_method_attr_index = int(f.read(2).hex(), 16)
    name_and_type_index = int(f.read(2).hex(), 16)
    return {
        'tag': tag,
        'bootstrap_method_attr_index': bootstrap_method_attr_index,
        'name_and_type_index': name_and_type_index,
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
    15: read_constant_method_handle_info,
    16: read_constant_method_type_info,
    18: read_invoke_dynamic_info
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
            2: 'ANNOTATION',
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
    index = 0
    attributes = list()
    while index < attributes_count:
        attribute_name_index = int(f.read(2).hex(), 16)
        attribute = read_attribute(f, attribute_name_index)
        attributes.append(attribute)
        index += 1
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
    attributes = list()
    index = 0
    while index < attributes_count:
        attribute_name_index = int(f.read(2).hex(), 16)
        attribute = read_attribute(f, attribute_name_index)
        attributes.append(attribute)
        index += 1
    return {
        'access_flags': access_flags,
        'name_index': name_index,
        'descriptor_index': descriptor_index,
        'attributes_count': attributes_count,
        'attributes': attributes
    }


def read_attribute_code(f, attribute_name_index):
    attribute_length = int(f.read(4).hex(), 16)
    max_stack = int(f.read(2).hex(), 16)
    max_locals = int(f.read(2).hex(), 16)
    code_length = int(f.read(4).hex(), 16)
    code = list()
    index = 0
    while index < code_length:
        code.append(f.read(1).hex())
        index += 1
    exception_table_length = int(f.read(2).hex(), 16)
    exception_table = list()
    index = 0
    while index < exception_table_length:
        exception_table.append({
            'start_pc': int(f.read(2).hex(), 16),
            'end_pc': int(f.read(2).hex(), 16),
            'handler_pc': int(f.read(2).hex(), 16),
            'catch_type': int(f.read(2).hex(), 16)
        })
        index += 1
    attributes_count = int(f.read(2).hex(), 16)
    attributes = list()
    while index < attributes_count:
        attribute_name_index = int(f.read(2).hex(), 16)
        attribute = read_attribute(f, attribute_name_index)
        attributes.append(attribute)
        index += 1
    return {
        'attribute_name_index': attribute_name_index,
        'attribute_length': attribute_length,
        'max_stack': max_stack,
        'max_locals': max_locals,
        'code_length': code_length,
        'code': code,
        'exception_table_legnth': exception_table_length,
        'exception_tables': exception_table,
        'attributes_count': attributes_count,
        'attributes': attributes
    }


def read_attribute_sourcefile(f, attribute_name_index):
    attribute_length = int(f.read(4).hex(), 16)
    sourcefile_index = int(f.read(2).hex(), 16)
    return {
        'attribute_name_index': attribute_name_index,
        'attribute_length': attribute_length,
        'sourcefile_index': sourcefile_index
    }


def read_attribute_line_number_table(f, attribute_name_index):
    attribute_length = int(f.read(4).hex(), 16)
    line_number_table_length = int(f.read(2).hex(), 16)
    line_number_table = list()
    index = 0
    while index < line_number_table_length:
        line_number_table.append({
            'start_pc': int(f.read(2).hex(), 16),
            'line_number': int(f.read(2).hex(), 16),
        })
        index += 1
    return {
        'attribute_name_index': attribute_name_index,
        'attribute_length': attribute_length,
        'line_number_table_length': line_number_table_length,
        'line_number_table': line_number_table
    }


def read_attribute_constant_value(f, attribute_name_index):
    attribute_length = int(f.read(4).hex(), 16)
    constantvalue_index = int(f.read(2).hex(), 16)
    return {
        'attribute_name_index': attribute_name_index,
        'attribute_length': attribute_length,
        'constantvalue_index': constantvalue_index
    }


def read_attribute_exceptions(f, attribute_name_index):
    attribute_length = int(f.read(4).hex(), 16)
    number_of_exceptions = int(f.read(2).hex(), 16)
    exception_index_table = list()
    index = 0
    while index < number_of_exceptions:
        exception_index_table.append(int(f.read(2).hex(), 16))
        index += 1
    return {
        'attribute_name_index': attribute_name_index,
        'attribute_length': attribute_length,
        'number_of_exceptions': number_of_exceptions,
        'exception_index_table': exception_index_table
    }


def read_attribute_signature(f, attribute_name_index):
    attribute_length = int(f.read(4).hex(), 16)
    signature_index = int(f.read(2).hex(), 16)
    return {
        'attribute_name_index': attribute_name_index,
        'attribute_length': attribute_length,
        'signature_index': signature_index
    }


def read_attribute_stack_map_table(f, attribute_name_index):
    attribute_length = int(f.read(4).hex(), 16)
    number_of_entries = int(f.read(2).hex(), 16)
    entries = list()
    index = 0
    while index < number_of_entries:
        frame_type = int(f.read(1).hex(), 16)
        entries.append(read_stack_map_frame(f, frame_type))
        index += 1
    return {
        'attribute_name_index': attribute_name_index,
        'attribute_length': attribute_length,
        'number_of_entries': number_of_entries,
        'entries': entries,
    }


def read_stack_map_frame(f, frame_type):
    stack_map_frame = {
        'frame_type': frame_type,
    }
    if 0 <= frame_type <= 63:
        # SAME
        pass
    elif 64 <= frame_type <= 127:
        # SAME_LOCALS_!_STACK_ITEM
        number_of_stack_items = 1
        stack_items = list()
        index = 0
        while index < number_of_stack_items:
            tag = int(f.read(1).hex(), 16)
            stack_items.append(read_verification_type_info(f, tag))
            index += 1
        stack_map_frame['stack'] = stack_items
    elif frame_type == 247:
        # SAME_LOCALS_1_STACK_ITEM_EXTENDED
        stack_map_frame['offset_delta'] = int(f.read(2).hex(), 16)
        number_of_stack_items = 1
        stack_items = list()
        index = 0
        while index < number_of_stack_items:
            tag = int(f.read(1).hex(), 16)
            stack_items.append(read_verification_type_info(f, tag))
            index += 1
        stack_map_frame['stack'] = stack_items
    elif 248 <= frame_type <= 250:
        # CHOP
        stack_map_frame['offset_delta'] = int(f.read(2).hex(), 16)
    elif frame_type == 251:
        # SAME_FRAME_EXTENDED
        stack_map_frame['offset_delta'] = int(f.read(2).hex(), 16)
    elif 252 <= frame_type <= 254:
        # APPEND
        stack_map_frame['offset_delta'] = int(f.read(2).hex(), 16)
        number_of_locals = frame_type - 251
        locals_ = list()
        index = 0
        while index < number_of_locals:
            tag = int(f.read(1).hex(), 16)
            locals_.append(read_verification_type_info(f, tag))
            index += 1
        stack_map_frame['locals'] = locals_
    elif frame_type == 255:
        # FULL_FRAME
        stack_map_frame['offset_delta'] = int(f.read(2).hex(), 16)
        number_of_locals = int(f.read(2).hex(), 16)
        stack_map_frame['number_of_locals'] = number_of_locals
        locals_ = list()
        index = 0
        while index < number_of_locals:
            tag = int(f.read(1).hex(), 16)
            locals_.append(read_verification_type_info(f, tag))
            index += 1
        stack_map_frame['locals'] = locals_

        number_of_stack_items = int(f.read(2).hex(), 16)
        stack_items = list()
        index = 0
        while index < number_of_stack_items:
            tag = int(f.read(1).hex(), 16)
            stack_items.append(read_verification_type_info(f, tag))
            index += 1
        stack_map_frame['stack'] = stack_items
    return stack_map_frame


def read_verification_type_info(f, tag):
    # Top_variable_info
    # Integer_variable_info
    # Float_variable_info
    # Long_variable_info
    # Double_variable_info
    # Null_variable_info
    # UninitializedThis_variable_info
    # Object_variable_info
    # Uninitialized_variable_info
    verification_type_info = {
        'tag': tag
    }
    if tag <= 6:
        pass
    elif tag == 7:
        verification_type_info['cpool_index'] = int(f.read(2).hex(), 16)
    elif tag == 8:
        verification_type_info['offset'] = int(f.read(2).hex(), 16)
    return verification_type_info


def read_attribute_inner_classes(f, attribute_name_index):
    attribute_length = int(f.read(4).hex(), 16)
    number_of_classes = int(f.read(2).hex(), 16)
    classes = list()
    index = 0
    while index < number_of_classes:
        classes.append({
            'inner_class_info_index': int(f.read(2).hex(), 16),
            'outer_class_info_index': int(f.read(2).hex(), 16),
            'inner_name_index': int(f.read(2).hex(), 16),
            'inner_class_access_flags': read_class_access_flags(f)
        })
        index += 1
    return {
        'attribute_name_index': attribute_name_index,
        'attribute_length': attribute_length,
        'number_of_classes': number_of_classes,
        'classes': classes
    }


def read_attribute_enclosing_method(f, attribute_name_index):
    attribute_length = int(f.read(4).hex(), 16)
    class_index = int(f.read(2).hex(), 16)
    method_index = int(f.read(2).hex(), 16)
    return {
        'attribute_name_index': attribute_name_index,
        'attribute_length': attribute_length,
        'class_index': class_index,
        'method_index': method_index
    }


def read_attribute_synthetic(f, attribute_name_index):
    attribute_length = int(f.read(4).hex(), 16)
    return {
        'attribute_name_index': attribute_name_index,
        'attribute_length': attribute_length
    }


def read_attribute_deprecated(f, attribute_name_index):
    attribute_length = int(f.read(4).hex(), 16)
    return {
        'attribute_name_index': attribute_name_index,
        'attribute_length': attribute_length
    }


def read_attribute_uncommon(f, attribute_name_index):
    # other uncommon attributes
    attribute_length = int(f.read(4).hex(), 16)
    attribute = f.read(attribute_length).hex()
    return {
        'attribute_name_index': attribute_name_index,
        'attribute_length': attribute_length,
        'attribute': attribute
    }


name_attribute_map = {
    'Code': read_attribute_code,
    'SourceFile': read_attribute_sourcefile,
    'LineNumberTable': read_attribute_line_number_table,
    'ConstantValue': read_attribute_constant_value,
    'Exceptions': read_attribute_exceptions,
    'Signature': read_attribute_signature,
    'StackMapTable': read_attribute_stack_map_table,
    'InnerClasses': read_attribute_inner_classes,
    'EnclosingMethod': read_attribute_enclosing_method,
    'Synthetic': read_attribute_synthetic,
    'Deprecated': read_attribute_deprecated
}


def read_attribute(f, attribute_name_index):
    attribute_name = constant_pool[attribute_name_index - 1]['bytes']
    parse_func = name_attribute_map.get(attribute_name, read_attribute_uncommon)
    return parse_func(f, attribute_name_index)


def main(class_file_path):
    with open(class_file_path, 'rb') as f:
        magic_code = f.read(4).hex()
        if not is_class(magic_code):
            raise ValueError("not a valid class file")
        minor_version = int(f.read(2).hex(), 16)
        major_version = int(f.read(2).hex(), 16)
        constant_pool_count = int(f.read(2).hex(), 16)
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
        attributes = list()
        index = 0
        while index < attributes_count:
            attribute_name_index = int(f.read(2).hex(), 16)
            attributes.append(read_attribute(f, attribute_name_index))
            index += 1


if __name__ == '__main__':
    main("Main.class")
