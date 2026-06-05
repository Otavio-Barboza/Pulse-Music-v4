from langdetect import detect
from deep_translator import GoogleTranslator
from Assets.App.Letras.Controller.letras_services import LetrasServices

if __name__ == "__main__":
    musica = input("Música: ")
    artista = input("Artista: ")

    letra = LetrasServices.buscar_letra(
        nome_artista = artista,
        nome_musica = musica
    )

    if not letra:
        print("Letra não encontrada.")
        exit()

    print("\n=== LETRA ===\n")
    print(letra)

    LetrasServices._definir_linguagem_saida(
        saida = 'pt' 
    )
    letra_traduzida = LetrasServices.traduzir(letra)

    print("\n===  LETRA TRADUZIDA  ===\n")
    print(letra_traduzida)