from ..Model.genius import Genius
from ..Repository.letra_repository import LetraRepository
from ..Translate.tradutor import Tradutor
import requests

class LetrasServices:
    GENIUS = Genius()
    TRADUTOR = Tradutor()
    
    _callbacks = {
        'buscar_letra' : []
    }

    @classmethod
    def registrar_callback(cls, evento : str, callback : callable):
        cls._callbacks[evento].append(callback)

    @classmethod
    def _notificar(cls, dados, evento : str):
        for callback in cls._callbacks.get(evento, []):
            callback(dados)


    @classmethod
    def buscar_letra(cls, dados : dict) -> str | None:
        from ..Translate.detector_idioma import detectar_idioma
        from ..Cache.memoria_letras import LetrasMemoria

        try:    
            if dados.get('chave') in LetrasMemoria._letras:
                print('essa letra já está salva')
                return
            
            song = cls.GENIUS.search_song(
                title = dados.get('nome'),
                artist = dados.get('artista')
            )
            
            if not song:
                return
            
            cls.salvar_letra(
                chave_da_musica = dados.get('chave'),
                letra = song.lyrics,
                idioma_padrao = detectar_idioma(song.lyrics)
            )

            LetrasMemoria.carregar_memoria()
        except requests.exceptions.Timeout:
            print("Timeout ao buscar letra.")
            return
        except Exception as erro:
            print(f"Erro: {erro}")
            return 
    
    @classmethod
    def _definir_linguagem_saida(cls, saida : str):
        cls.TRADUTOR.target = saida

    @classmethod
    def traduzir(cls, letra : str) -> str | None:
        from Assets.App.Letras.Translate.detector_idioma import detectar_idioma

        cls.TRADUTOR.source = detectar_idioma(letra)
        
        if (
            cls.TRADUTOR.source is None
             or
            cls.TRADUTOR.target is None
        ):
            return
        return cls.TRADUTOR.translate(letra)
    
    @classmethod
    def salvar_letra(cls, letra, chave_da_musica, idioma_padrao):
        letras_existentes = LetraRepository.ler_json()

        letras_existentes[chave_da_musica] = {
            'letra_original' : letra,
            'idioma_original' : idioma_padrao,
            'traducoes' : []
        }

        LetraRepository.salvar_json(letras_existentes)

    @classmethod
    def atualizar_traducoes(cls, chave_da_musica : str, novo_idioma : str, nova_letra : str):
        letras_existentes = LetraRepository.ler_json()

        if novo_idioma not in letras_existentes[chave_da_musica]['traducoes']:
            letras_existentes[chave_da_musica]['traducoes'].append({
                'idioma' : novo_idioma,
                'letra' : nova_letra
            })

        LetraRepository.salvar_json(letras_existentes)