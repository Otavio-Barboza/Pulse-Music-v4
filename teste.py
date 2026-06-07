from langdetect import detect
from deep_translator import GoogleTranslator
from Assets.App.Letras.Controller.letras_services import LetrasServices

if __name__ == "__main__":
    # musica = input("Música: ")
    # artista = input("Artista: ")

    # letra = LetrasServices.buscar_letra(
    #     nome_artista = artista,
    #     nome_musica = musica
    # )

    # if not letra:
    #     print("Letra não encontrada.")
    #     exit()

    # print("\n=== LETRA ===\n")
    # print(letra)

    # LetrasServices._definir_linguagem_saida(A
    #     saida = 'ptt' 
    # )
    # letra_traduzida = LetrasServices.traduzir(letra)

    # print("\n===  LETRA TRADUZIDA  ===\n")
    # print(letra_traduzida)

    # traduzir chaves
    dicio = GoogleTranslator()._languages
    c = {}
    for chave, item in dicio.items():
        chave_corrigida = chave.replace(' ', '_')
        c[chave_corrigida] = item

    print(c)
    print(GoogleTranslator()._languages)
    # print(GoogleTranslator()._languages)