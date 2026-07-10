# import geral
from langdetect import detect_langs


def language_detect(lyric: str):
    try:
        result = detect_langs(lyric)

        if result and result[0].prob > 0.8:
            return result[0].lang
        return None
    except Exception as e:
        print(e)
        return None
    
