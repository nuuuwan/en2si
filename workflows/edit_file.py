import sys
import time
from en2si import DefaultTranslator
import os
from utils import Log, TIME_FORMAT_TIME, Time

log = Log('edit_file')


def main(path: str):
    log.info(f'Editing {path}...')
    t = DefaultTranslator()
    last_update_time = None
    while True:
        time.sleep(1)
        update_time = os.path.getmtime(path)
        if update_time == last_update_time:
            time_str = TIME_FORMAT_TIME.stringify(Time(update_time))
            print(
                f'\rNo change (Last updated at{time_str})', end='', flush=True
            )
            continue
        t.translate_file(path)
        last_update_time = os.path.getmtime(path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Path not specified.')
    path = sys.argv[1]
    main(path)
