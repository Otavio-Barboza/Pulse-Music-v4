from langdetect import detect_langs

def detectar_idioma(letra : str):
    try:
        resultado = detect_langs(letra)

        if resultado and resultado[0].prob > 0.8:
            return resultado[0].lang
        return None
    except Exception as e:
        print(e)
        return None
    
