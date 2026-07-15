# import de back-end
from core.meta.repository.tasks import Task

# import geral
import re


class Filtering:

    SEPARATOR = " <SEP> "

    @classmethod
    def clean_feat(cls, artist: str) -> str:
        """
            Remove qualquer ocorrência de ft/feat/featuring e tudo que vier depois disso.
        """

        if not artist:
            return artist

        # Remove padrões como:
        # ft, ft., feat, feat., featuring (com ou sem parênteses)
        template = re.compile(
            r'\s*(?:\(|-)?\s*(?:ft\.?|feat\.?|featuring)\b.*',
            flags = re.IGNORECASE
        )

        cleaned_artist = re.sub(template, '', artist)

        return cleaned_artist.strip()

    @classmethod
    async def async_normalize_separators(cls, name: str):
        name = re.sub(r"\s+-\s+", cls.SEPARATOR, name)

        # Evita <SEP><SEP><SEP>
        name = re.sub(
            rf"(?:{re.escape(cls.SEPARATOR)})+",
            cls.SEPARATOR,
            name
        )

        return name.strip()
    
    @classmethod
    async def async_filter_title(cls, name : str):
        original_name = name
        emoji_template = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+", flags =  re.UNICODE)    
        templates = [
            r"official\s*video", r"lyric\s*video", r"audio", r"clipe\s*oficial", r"-\s*dvd", r"ao\s*vivo", r"no\s*rio\s*hq\s*\+\s*letras", r"mp3_?\d+k", r"official\s*video\s*music", r"dvd\s*o\s*nossos\s*tempo\s*é\s*hoje", r"official\s*music\s*video", r"tradução", r"legendado", r"clip\s*officiel", r"video", r"novo\s*dvd\s*1977", r"video\s*clipe\s*oficial", r"vevo", r"hd", r"summer\s*eletrohits", r"copia", r"audio\s*only", r"remastered\s*in", r"4k", r"official\s*lyric\s*video", r"oficial", r"uk", r"edit", r"sony\s*music\s*live", r"tribute\s*video", r"official\s*hd\s*video", r"radio\s*edit", r"videoclipe", r"-\s*clean", r"novosomdorappa"
        ]
        
        # Remove emojis e padrões unicode
        name = emoji_template.sub("", name)

        # Remove parênteses, colchetes e tags
        name = re.sub(r"\(.*?\)|\[.*?\]|\d+k|MP3|_", "", name, flags = re.IGNORECASE)  
            
        # Realiza a exclusão/filtragem de todos os padrões registrados na lista. 
        for template in templates:
            name = re.sub(template, '', name, flags = re.IGNORECASE)
        
        name =  re.sub(r"\b(feat|ft|com|part)\.?\b", "ft.", name, flags = re.IGNORECASE)  # Padroniza "feat."
        name = re.sub(r"\.mp3$", "", name, flags = re.IGNORECASE).strip()
        name = re.sub(r"\s+", " ", name).strip()

        if '.' in name.split()[-1]:
            name.removeprefix('.')

        name = await cls._async_normalizar_separadores(name)
        qtde_hifen = name.count(cls.SEPARATOR)

        if qtde_hifen == 0:
            return {
                'titulo_original' : original_name,
                'titulo_filtrado' : name,
                'artist' : None
            }
        elif qtde_hifen == 1:
            artist, title = name.split(cls.SEPARATOR, 1)
            return {
                'titulo_original' : original_name,
                'titulo_filtrado' : title.strip(),
                'artist' : artist.strip()
            }
        elif qtde_hifen > 1:
            parties = name.split(cls.SEPARATOR)
            artist = parties[0]
            title = " - ".join(parties[1:])

            return {
                "original_title": original_name,
                "filtered_title": title.strip(),
                "artist": artist.strip()
            }
        else:
            raise RuntimeError("Erro inesperado na filtragem")

    @classmethod
    async def async_filter_artist(cls, artist: str) -> str | None:
        if not artist:
            return None

        artist = artist.strip()

        if artist.isalpha() and artist != artist.upper():
            artist = re.sub(r"([a-z])([A-Z])", r"\1 \2", artist)

        if artist.find('(') != -1:
            artist = artist.replace('(', '').replace(')', '').replace('.', '').strip()
        
        if 'records' in artist.lower().split() or 'radar' in artist.lower().split():
            return None
        
        # Alta confiança
        if 'topic' in artist.lower().split():
            return re.sub(r"-\s*topic\b", "", artist, flags = re.IGNORECASE).strip()

        index = artist.lower().find('vevo')
        if index != -1:
            return artist[:index]

        if re.search(r"\b(oficial|official)\b", artist, re.IGNORECASE):
            return re.sub(r"\b(oficial|official)\b", "", artist, flags=re.IGNORECASE).strip()

        if 'norte' in artist.lower().split():
            return re.sub(r"-\s*norte\b", "", artist, flags = re.IGNORECASE).strip()
        
        return None
    
    @classmethod
    async def async_filter_file(cls, name : str, caminho : str):
        original_name = name.removesuffix('.mp3')

        separators = [r" - ", r" \| ", r" – ", r"•", r"ft."]
        # Expressão regular que identifica emojis e caracteres especiais Unicode
        emoji_template = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+", flags=re.UNICODE)    
        templates = [
            r"official\s*video", r"lyric\s*video", r"audio", r"clipe\s*oficial", r"-\s*dvd", r"ao\s*vivo", r"no\s*rio\s*hq\s*\+\s*letras", r"mp3_?\d+k", r"official\s*video\s*music", r"dvd\s*o\s*nossos\s*tempo\s*é\s*hoje", r"official\s*music\s*video", r"tradução", r"legendado", r"clip\s*officiel", r"video", r"novo\s*dvd\s*1977", r"video\s*clipe\s*oficial", r"viva", r"vevo", r"hd", r"summer\s*eletrohits", r"copia", r"audio\s*only", r"remastered\s*in", r"4k", r"official\s*lyric\s*video", r"oficial",r"uk", r"edit", r"sony\s*music\s*live", r"tribute\s*video", r"official\s*hd\s*video", r"radio\s*edit", r"videoclipe", r"-\s*clean", r"novosomdorappa"
        ]
        
        # Remove emojis e padrões unicode
        name = emoji_template.sub("", name)
        # Remove parênteses, colchetes e tags
        name = re.sub(r"\(.*?\)|\[.*?\]|\d+k|MP3|\_", "", name, flags = re.IGNORECASE)  
            
        # Realiza a exclusão/filtragem de todos os padrões registrados na lista.
        for template in templates:
            name = re.sub(template, '', name, flags = re.IGNORECASE)
        
        name =  re.sub(r"\b(feat|ft|com|part)\.?\b", "ft.", name, flags=re.IGNORECASE)  # Padroniza "feat."
        name = re.sub(r"\.mp3$", "", name, flags=re.IGNORECASE).strip()

        # split
        parties = [name]
        for separador in separators:
            div = re.split(separador, name, maxsplit = 1)

            if len(div) == 2:
                parties = div
                break
        
        if len(parties) == 2:
            artist, title = parties
        else:
            # Caso não seja claro a separação, inicia pesquisa de artist pela API da deezer.
            title = parties[0].strip()
            artist = 'Desconhecido'
        
        # limpeza final
        artist = cls.limpar_final(artist)
        title = cls.limpar_final(title)

        return {
            'artist' : artist,
            'title' : title
        }
    
    @classmethod
    def base_artist(cls, artist: str) -> str:
        if not artist:
            return
        
        artist = cls.clean_feat(artist)

        for sep in [",", " vs. ", " & "]:
            if sep in artist.lower():
                artist = artist.split(sep)[0]
                break

        return artist.strip()