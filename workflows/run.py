import sys
import time
from en2si import DefaultTranslator
import os
from utils import Log, TIME_FORMAT_TIME, Time, File

log = Log('edit_file')


def new_file(path_prefix: str):
    path = f'{path_prefix}.en.md'
    File(path).write_lines([
        f'# {path_prefix}',
    ])
    edit(path)

def edit(path: str):
    log.info(f'Editing {path}...')
    os.startfile(path)
    
    t = DefaultTranslator()
    last_update_time = None
    first = True
    while True:
        time.sleep(1)
        update_time = os.path.getmtime(path)
        if update_time == last_update_time:
            time_str = TIME_FORMAT_TIME.stringify(Time(update_time))
            print(
                f'\rNo change (Last updated at{time_str})', end='', flush=True
            )
            continue
        path_dest = t.translate_file(path)
        if first:
            os.startfile(path_dest)
            first = False
        last_update_time = os.path.getmtime(path)

def main(cmd: str, path: str):
    if cmd == 'new':
        new_file(path)
    elif cmd == 'edit':
        edit(path)
    else:
        raise Exception(f'Unknown command {cmd}')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise Exception('usage: en2si <new|edit> <path>')
    cmd = sys.argv[1]
    path = sys.argv[2]
    main(cmd, path)
