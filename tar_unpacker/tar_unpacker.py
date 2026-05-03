#!/usr/bin/env python3

import argparse
import os
import sys
import time


class TarParser:
    _HEADER_FMT1 = '100s8s8s8s12s12s8sc100s255s'
    _HEADER_FMT2 = '6s2s32s32s8s8s155s12s'
    _HEADER_FMT3 = '6s2s32s32s8s8s12s12s112s31x'
    _READ_BLOCK = 16 * 2 ** 20

    _FILE_TYPES = {
        b'0': 'Regular file',
        b'1': 'Hard link',
        b'2': 'Symbolic link',
        b'3': 'Character device node',
        b'4': 'Block device node',
        b'5': 'Directory',
        b'6': 'FIFO node',
        b'7': 'Reserved',
        b'D': 'Directory entry',
        b'K': 'Long linkname',
        b'L': 'Long pathname',
        b'M': 'Continue of last file',
        b'N': 'Rename/symlink command',
        b'S': "`sparse' regular file",
        b'V': "`name' is tape/volume header name"
    }

    def __init__(self, filename):
        """
        Открывает tar-архив `filename` и производит его предобработку (если требуется).
        """
        self.filename = filename
        self.files_data = []

        with open(filename, 'rb') as f:
            long_name = None
            while True:
                header = f.read(512)
                if not header.strip(b'\0'):
                    break

                type_flag = header[156:157]

                if type_flag == b'L':
                    long_name_size = int(header[124:136].strip(b'\0'), 8)
                    long_name_bytes = f.read((long_name_size + 511) // 512 * 512)[:long_name_size]
                    long_name = long_name_bytes.decode('utf-8', errors='replace').strip()
                    continue

                name = header[:100].strip(b'\0').decode('utf-8', errors='replace')
                if long_name:
                    name = long_name.strip()
                    long_name = None

                name = name.replace('\x00', '').strip()

                file_size = int(header[124:136].strip(b'\0'), 8)
                self.files_data.append({
                    'name': name,
                    'type': type_flag,
                    'header': header,
                    'offset': f.tell(),
                    'size': file_size
                })

                f.seek((file_size + 511) // 512 * 512, 1)

    def extract(self, dest=os.getcwd()):
        """
        Распаковывает данный tar-архив в каталог `dest`.
        """
        with open(self.filename, 'rb') as f:
            for file in self.files_data:
                if file['type'] == b'5':
                    os.makedirs(os.path.join(dest, file['name']), exist_ok=True)
                else:
                    file_path = os.path.join(dest, file['name'])
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, 'wb') as out_file:
                        f.seek(file['offset'])
                        out_file.write(f.read(file['size']))

    def files(self):
        """
        Возвращает итератор имён файлов (с путями) в архиве.
        """
        return [file['name'] for file in self.files_data]

    def file_stat(self, filename):
        """
        Возвращает информацию о файле `filename` в архиве.

        Пример (некоторые поля могут отсутствовать, подробности см. в описании формата tar):
        [
            ('Filename', '/NSimulator'),
            ('Type', 'Directory'),
            ('Mode', '0000755'),
            ('UID', '1000'),
            ('GID', '1000'),
            ('Size', '0'),
            ('Modification time', '29 Mar 2014 03:52:45'),
            ('Checksum', '5492'),
            ('User name', 'victor'),
            ('Group name', 'victor')
        ]
        """
        if filename not in self.files():
            raise ValueError(filename)

        with open(self.filename, 'rb') as f:
            for file in self.files_data:
                if file['name'] == filename:
                    header = file['header']
                    mode = header[100:108].strip(b'\0').decode()
                    user_id = int(header[108:116].strip(b'\0'), 8)
                    group_id = int(header[116:124].strip(b'\0'), 8)
                    size = int(header[124:136].strip(b'\0'), 8)
                    checksum = int(header[148:155].strip(b'\0'), 8)
                    type_flag = header[156:157]
                    user_name = header[265:297].strip(b'\0').decode('utf-8')
                    group_name = header[297:329].strip(b'\0').decode('utf-8')
                    mod_time = time.strftime(
                        "%d %b %Y %H:%M:%S",
                        time.gmtime(int(header[136:148].strip(b'\0'), 8))
                    )

                    info = [
                        ('Filename', filename),
                        ('Type', self._FILE_TYPES[type_flag]),
                        ('Mode', mode),
                        ('UID', str(user_id)),
                        ('GID', str(group_id)),
                        ('Size', str(size)),
                        ('Modification time', mod_time),
                        ('Checksum', str(checksum)),
                        ('User name', user_name),
                        ('Group name', group_name)
                    ]
                    return info


def print_file_info(stat, f=sys.stdout):
    max_width = max(map(lambda s: len(s[0]), stat))
    for field in stat:
        print("{{:>{}}} : {{}}".format(max_width).format(*field), file=f)


def main():
    parser = argparse.ArgumentParser(
        usage='{} [OPTIONS] FILE'.format(os.path.basename(sys.argv[0])),
        description='Tar extractor'
    )
    parser.add_argument('-l', '--list', action='store_true', dest='ls',
                        help='list the contents of an archive')
    parser.add_argument('-x', '--extract', action='store_true', dest='extract',
                        help='extract files from an archive')
    parser.add_argument('-i', '--info', action='store_true', dest='info',
                        help='get information about files in an archive')
    parser.add_argument('fn', metavar='FILE',
                        help='name of an archive')

    args = parser.parse_args()
    if not (args.ls or args.extract or args.info):
        sys.exit("Error: action must be specified")

    try:
        tar = TarParser(args.fn)

        if args.info:
            for fn in sorted(tar.files()):
                print_file_info(tar.file_stat(fn))
                print()
        elif args.ls:
            for fn in sorted(tar.files()):
                print(fn)

        if args.extract:
            tar.extract()
    except Exception as e:
        sys.exit(e)


if __name__ == '__main__':
    main()
