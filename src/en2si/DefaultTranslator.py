import os
import tempfile
from functools import cache
import re
from googletrans import Translator
from utils import File, Log, hashx

log = Log('En2Si')


class DefaultTranslator:
    DIR_TEMP = os.path.join(tempfile.gettempdir(), 'en2si', 'default')
    LANG_SRC = 'en'
    LANG_DEST = 'si'

    @staticmethod
    def clean(s: str) -> str:
        s = s.strip()
        s = re.sub(r'\s+', ' ', s)
        return s

    def __init__(self):
        self.translator = Translator()

    @cache
    def translate_nocache(self, text_src: str) -> str:
        if text_src.strip() == '':
            return ''

        return self.translator.translate(
            text_src,
            src=DefaultTranslator.LANG_SRC,
            dest=DefaultTranslator.LANG_DEST,
        ).text

    @cache
    def get_file(self, text_src: str) -> File:
        h = hashx.md5(text_src)
        if not os.path.exists(DefaultTranslator.DIR_TEMP):
            os.makedirs(self.DIR_TEMP)
        path = os.path.join(DefaultTranslator.DIR_TEMP, h + '.txt')
        return File(path)

    @cache
    def translate(self, text_src: str) -> str:
        file = self.get_file(text_src)
        if file.exists:
            return file.read()
        else:
            text_dest = self.translate_nocache(text_src)
            file.write(text_dest)
            log.debug(f'"{text_src}"')
            log.debug(f' -> "{text_dest}"')
            log.debug(f' -> {file.path}')
            return text_dest

    @cache
    def translate_line(self, line_src: str) -> str:
        sentences_src = line_src.split('.')
        sentences_dest = [
            self.translate(sentence_src) for sentence_src in sentences_src
        ]
        line_dest = '. '.join(sentences_dest)
        line_dest = DefaultTranslator.clean(line_dest)
        return line_dest

    def translate_file(self, path_src: str):
        src_pattern = '.' + DefaultTranslator.LANG_SRC + '.'
        if src_pattern not in path_src:
            raise Exception(
                f'Invalid source file: {path_src}.'
                + ' Must contain "{src_pattern}"'
            )

        dest_pattern = '.' + DefaultTranslator.LANG_DEST + '.'
        lines_src = File(path_src).read_lines()
        lines_dest = [self.translate_line(line) for line in lines_src]
        path_dest = path_src.replace(src_pattern, dest_pattern)
        File(path_dest).write_lines(lines_dest)
        log.info(f'Wrote {path_dest}')
