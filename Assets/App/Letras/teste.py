from langdetect import detect
from deep_translator import GoogleTranslator
import dotenv, os, lyricsgenius

dotenv.load_dotenv(r'Assets\App\Env\.env')
GENIUS_TOKEN = os.getenv('teste')

def obter_letra(musica, artista):

    genius = lyricsgenius.Genius(
        GENIUS_TOKEN,
        skip_non_songs = True,
        excluded_terms = ["(Remix)", "(Live)"],
        remove_section_headers = True
    )

    song = genius.search_song(musica, artista)

    if not song:
        return None

    return song.lyrics


def detectar_idioma(letra):
    try:
        return detect(letra)
    except:
        return None


def traduzir_letra(letra, origem, destino="pt"):
    return GoogleTranslator(
        source=origem,
        target=destino
    ).translate(letra)


if __name__ == "__main__":
    musica = input("Música: ")
    artista = input("Artista: ")

    letra = obter_letra(musica, artista)

    if not letra:
        print("Letra não encontrada.")
        exit()

    idioma = detectar_idioma(letra)

    print("\n=== IDIOMA ===")
    print(idioma)

    print("\n=== LETRA ===\n")
    print(letra)

    letra_traduzida = traduzir_letra(
        letra = letra,
        origem = idioma,
        destino = 'pt'
    )

    print("\n===  LETRA TRADUZIDA  ===\n")
    print(letra_traduzida)