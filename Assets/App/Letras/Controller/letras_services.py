from ..Model.genius import Genius
from ..Repository.letra_repository import LetraRepository
from ..Translate.tradutor import Tradutor
import requests

class LetrasServices:
    _tela_expandida = False
    GENIUS = Genius()
    TRADUTOR = Tradutor()

    _LINGUAGENS_DIPONIVEIS : dict[str, str] = TRADUTOR._languages
    
    _callbacks = {}

    @classmethod
    def registrar_callback(cls, evento : str, callback : callable):
        if evento not in cls._callbacks:
            cls._callbacks[evento] = []
        cls._callbacks[evento].append(callback)

    @classmethod
    def _notificar(cls, dados, evento : str):
        for callback in cls._callbacks.get(evento, []):
            callback(dados)

    @classmethod
    def set_tela_expandida(cls, valor : bool):
        cls._tela_expandida = valor

    @classmethod
    def buscar_letra(cls, dados : dict) -> str | None:
        from ..Translate.detector_idioma import detectar_idioma
        from ..Cache.memoria_letras import LetrasMemoria

        try:    
            if dados.get('chave') in LetrasMemoria._letras:
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

            if cls._tela_expandida:
                cls._notificar(
                    evento = 'att_letra',
                    dados = None
                )

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

    @classmethod
    def executar_traducao(cls, idioma : str):
        from ..Cache.memoria_letras import LetrasMemoria
        from ...Audio.Controller.sessao import SessaoReproducao

        if SessaoReproducao.estado.musica_atual is None:
            return 'Nenhuma música carregada para efetuar traducao'
        
        letra_traduzida_existente = LetrasMemoria.retornar_letra_traduzida(idioma)
        
        if letra_traduzida_existente is not None:
            print('carregando letra existente')
            return letra_traduzida_existente
        
        letra = LetrasMemoria.retornar_letra()

        if not letra:
            return 'A respectiva letra não foi encontrada. Portanto, não é possível traduzir!'
        
        letra_traduzida = cls.traduzir(letra)

        if not letra_traduzida:
            return 'Falha na tradução, tente novamente!'
        
        cls.atualizar_traducoes(
            chave_da_musica = SessaoReproducao.estado.musica_atual.chave,
            novo_idioma = idioma,
            nova_letra = letra_traduzida
        )

        return letra_traduzida