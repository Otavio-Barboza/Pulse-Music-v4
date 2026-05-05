from .validacao import Validacao
import re

class Filtragem:
    SEPARADOR = " <SEP> "

    @classmethod
    def _limpar_feat(cls, artista: str) -> str:
        """
        Remove qualquer ocorrência de ft/feat/featuring e
        tudo que vier depois disso.
        """

        if not artista:
            return artista

        # Remove padrões como:
        # ft, ft., feat, feat., featuring (com ou sem parênteses)
        padrao = re.compile(
            r'\s*(?:\(|-)?\s*(?:ft\.?|feat\.?|featuring)\b.*',
            flags=re.IGNORECASE
        )

        artista_limpo = re.sub(padrao, '', artista)

        return artista_limpo.strip()

    @classmethod
    async def _async_normalizar_separadores(cls, nome : str):
        nome = re.sub(r"\s+-\s+", cls.SEPARADOR, nome)

        # Evita <SEP><SEP><SEP>
        nome = re.sub(
            rf"(?:{re.escape(cls.SEPARADOR)})+",
            cls.SEPARADOR,
            nome
        )

        return nome.strip()
    
    @classmethod
    async def _async_filtrar_titulo(cls, nome : str):
        nome_original = nome
        padrao_emoji = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+", flags=re.UNICODE)    
        padroes = [
            r"official\s*video", r"lyric\s*video", r"audio", r"clipe\s*oficial", r"-\s*dvd", r"ao\s*vivo", r"no\s*rio\s*hq\s*\+\s*letras", r"mp3_?\d+k", r"official\s*video\s*music", r"dvd\s*o\s*nossos\s*tempo\s*é\s*hoje", r"official\s*music\s*video", r"tradução", r"legendado", r"clip\s*officiel", r"video", r"novo\s*dvd\s*1977", r"video\s*clipe\s*oficial", r"vevo", r"hd", r"summer\s*eletrohits", r"copia", r"audio\s*only", r"remastered\s*in", r"4k", r"official\s*lyric\s*video", r"oficial", r"uk", r"edit", r"sony\s*music\s*live", r"tribute\s*video", r"official\s*hd\s*video", r"radio\s*edit", r"videoclipe", r"-\s*clean", r"novosomdorappa"
        ]
        
        # Remove emojis e padrões unicode
        nome = padrao_emoji.sub("", nome)

        # Remove parênteses, colchetes e tags
        nome = re.sub(r"\(.*?\)|\[.*?\]|\d+k|MP3|_", "", nome, flags = re.IGNORECASE)  
            
        # Realiza a exclusão/filtragem de todos os padrões registrados na lista.
        for padrao in padroes:
            nome = re.sub(padrao, '', nome, flags = re.IGNORECASE)
        
        nome =  re.sub(r"\b(feat|ft|com|part)\.?\b", "ft.", nome, flags=re.IGNORECASE)  # Padroniza "feat."
        nome = re.sub(r"\.mp3$", "", nome, flags = re.IGNORECASE).strip()
        nome = re.sub(r"\s+", " ", nome).strip()

        if '.' in nome.split()[-1]:
            nome.removeprefix('.')

        nome = await cls._async_normalizar_separadores(nome)
        qtde_hifen = nome.count(cls.SEPARADOR)

        if qtde_hifen == 0:
            return {
                'titulo_original' : nome_original,
                'titulo_filtrado' : nome,
                'artista' : None
            }
        elif qtde_hifen == 1:
            artista, titulo = nome.split(cls.SEPARADOR, 1)
            return {
                'titulo_original' : nome_original,
                'titulo_filtrado' : titulo.strip(),
                'artista' : artista.strip()
            }
        elif qtde_hifen > 1:
            partes = nome.split(cls.SEPARADOR)
            artista = partes[0]
            titulo = " - ".join(partes[1:])
            return {
                "titulo_original": nome_original,
                "titulo_filtrado": titulo.strip(),
                "artista": artista.strip()
            }
        else:
            raise RuntimeError("Erro inesperado na filtragem")

    @classmethod
    async def _async_filtrar_artista(cls, artista: str) -> str | None:
        if not artista:
            return None

        artista = artista.strip()

        if artista.isalpha() and artista != artista.upper():
            artista = re.sub(r"([a-z])([A-Z])", r"\1 \2", artista)

        if artista.find('(') != -1:
            artista = artista.replace('(', '').replace(')', '').replace('.', '').strip()
        
        if 'records' in artista.lower().split() or 'radar' in artista.lower().split():
            return None
        
        # Alta confiança
        if 'topic' in artista.lower().split():
            return re.sub(r"-\s*topic\b", "", artista, flags = re.IGNORECASE).strip()

        indice = artista.lower().find('vevo')
        if indice != -1:
            return artista[:indice]

        if re.search(r"\b(oficial|official)\b", artista, re.IGNORECASE):
            return re.sub(r"\b(oficial|official)\b", "", artista, flags=re.IGNORECASE).strip()

        if 'norte' in artista.lower().split():
            return re.sub(r"-\s*norte\b", "", artista, flags = re.IGNORECASE).strip()
        
        return None
    
    @classmethod
    async def _async_filtrar_arquivo(cls, nome : str, caminho : str):
        nome_original = nome.removesuffix('.mp3')

        separadores = [r" - ", r" \| ", r" – ", r"•", r"ft."]
        # Expressão regular que identifica emojis e caracteres especiais Unicode
        padrao_emoji = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+", flags=re.UNICODE)    
        padroes = [
            r"official\s*video", r"lyric\s*video", r"audio", r"clipe\s*oficial", r"-\s*dvd", r"ao\s*vivo", r"no\s*rio\s*hq\s*\+\s*letras", r"mp3_?\d+k", r"official\s*video\s*music", r"dvd\s*o\s*nossos\s*tempo\s*é\s*hoje", r"official\s*music\s*video", r"tradução", r"legendado", r"clip\s*officiel", r"video", r"novo\s*dvd\s*1977", r"video\s*clipe\s*oficial", r"viva", r"vevo", r"hd", r"summer\s*eletrohits", r"copia", r"audio\s*only", r"remastered\s*in", r"4k", r"official\s*lyric\s*video", r"oficial",r"uk", r"edit", r"sony\s*music\s*live", r"tribute\s*video", r"official\s*hd\s*video", r"radio\s*edit", r"videoclipe", r"-\s*clean", r"novosomdorappa"
        ]
        
        # Remove emojis e padrões unicode
        nome = padrao_emoji.sub("", nome)
        # Remove parênteses, colchetes e tags
        nome = re.sub(r"\(.*?\)|\[.*?\]|\d+k|MP3|\_", "", nome, flags = re.IGNORECASE)  
            
        # Realiza a exclusão/filtragem de todos os padrões registrados na lista.
        for padrao in padroes:
            nome = re.sub(padrao, '', nome, flags = re.IGNORECASE)
        
        nome =  re.sub(r"\b(feat|ft|com|part)\.?\b", "ft.", nome, flags=re.IGNORECASE)  # Padroniza "feat."
        nome = re.sub(r"\.mp3$", "", nome, flags=re.IGNORECASE).strip()

        # split
        partes = [nome]
        for separador in separadores:
            div = re.split(separador, nome, maxsplit = 1)

            if len(div) == 2:
                partes = div
                break
        
        if len(partes) == 2:
            artista, titulo = partes
        else:
            # Caso não seja claro a separação, inicia pesquisa de artista pela API da deezer.
            titulo = partes[0].strip()
            artista = 'Desconhecido'
        
        # limpeza final
        artista = cls.limpar_final(artista)
        titulo = cls.limpar_final(titulo)

        return {
            'artista' : artista,
            'titulo' : titulo
        }
    
    @classmethod
    def artista_base(cls, artista : str) -> str:
        if not artista:
            return
        
        artista = cls._limpar_feat(artista)

        for sep in [",", " vs. ", " & "]:
            if sep in artista.lower():
                artista = artista.split(sep)[0]
                break

        return artista.strip()