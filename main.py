import asyncio
import json
from typing import  Dict, List

import pysrt
import deepl


class WrongOutputLanguage(deepl.exceptions.DeepLException):
    def __init__(self,target_language):
        self.target_language = target_language
        super().__init__(f"Target language {self.target_language} not available")


class SubtitleLine:
    def __init__(self, index:int, start, end, position:str, text:str):
        self.index = index
        self.start = start
        self.end = end
        self.position = position
        self.text = text


class SubtitleTranslate:
    SUB_DICT : Dict[int, SubtitleLine]= {}

    def __init__(self, subtitle: pysrt.open, target_lang:str):
        self.target_language = target_lang
        self.subtitle = subtitle

    def build(self):
        for item in self.subtitle:
            self.SUB_DICT[item.index] = SubtitleLine(**item.__dict__)

    async def get_line_translation(self,sub: SubtitleLine):
        try:
            translator = deepl.Translator(API_KEY)
            # print(translator.translate_text(sub.text, target_lang=self.target_language))
            return translator.translate_text(sub.text, target_lang=self.target_language)
        except deepl.exceptions.DeepLException:
            raise WrongOutputLanguage(target_language=self.target_language)

    async def get_whole_translation(self) -> List[str]:
        return await asyncio.gather(*[self.get_line_translation(self.SUB_DICT[index]) for index in self.SUB_DICT.keys()])




sub_url = "E:\PycharmProjects\Subtranslate\heart.of.stone.2023.1080p.web.h264-huzzah_Dutch.srt"



with open ("./config.json", "r") as file:
    config = json.load(file)

API_KEY = config["API_KEY"]
DEEPL_DOMAIN = config["DEEPL_FREE_DOMAIN"]

async def main():
    subtitle = pysrt.open(sub_url)
    subtitle = subtitle[:10]

    my_translator = SubtitleTranslate(subtitle,"EN-US")
    my_translator.build()
    result = await my_translator.get_whole_translation()
    for item in result:
        print(item.text, sep="\n")

if __name__ == '__main__':
    asyncio.run(main())
