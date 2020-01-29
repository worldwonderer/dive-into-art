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


def main(dex_file_path):
    with open(dex_file_path, 'rb') as f:
        dex_version = is_dex(f)


if __name__ == '__main__':
    main("Main.dex")
