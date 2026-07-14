from ...Services.gerenciador_contas import GerenciadorContas
from pathlib import Path
import json, aiofiles, os, requests

class Persistencia:
    CAMINHO_CONTA_ATUAL : str | None = f'Assets/Data/Contas/115700472009531668447/Music/musicas.json'

    @classmethod
    async def ler_json(cls, caminho : str) -> dict:
        async with aiofiles.open(caminho, 'r', encoding = 'utf-8') as j:
            return json.loads(await j.read())
    
    @classmethod
    def js(cls, caminho : str) -> dict:
        with open(caminho, 'r', encoding = 'utf-8') as j:
            return json.load(j)
        
    @classmethod
    async def salvar_json(cls, caminho : str, dados : dict):
        async with aiofiles.open(caminho, 'w', encoding = 'utf-8') as j:
            conteudo = json.dumps(
                dados,
                ensure_ascii = False,
                indent = 4
            )
            await j.write(conteudo)
    
    @classmethod
    async def gerenciar_dados_json_musicas(cls, grupos : dict):
        from ..Controller.status import Status
        from .tasks import GerenciaMetadados
        
        json_musicas_atual = await cls.ler_json(
            f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Music/musicas.json'
        )
        
        lista_objetos = [
            musica
            for grupo in grupos.values()
            for musica in grupo
        ]
        
        dados_finais = {}
        
        for musica in lista_objetos:
            print()
            print(musica.caminho, musica.arquivo_mp3_original)
            print()
            
            caminho_completo = os.path.normpath(
                os.path.join(
                    musica.caminho, 
                    musica.arquivo_mp3_original
                )
            )
            id_musica = GerenciaMetadados.gerar_track_id(caminho_completo)
            
            dados_finais[id_musica] = GerenciaMetadados._organizar_json_musicas(
                musica = musica
            )

        for id_antigo, dado_antigo in json_musicas_atual.items():
            if id_antigo not in dados_finais:
                dados_finais[id_antigo] = dado_antigo
        
        await cls.salvar_json(caminho = cls.CAMINHO_CONTA_ATUAL, dados = dados_finais)
    
    @classmethod
    async def atribuir_memoria(cls):
        from ..Memoria.memoria_global import memoria
        from ..Memoria.memoria_artistas import MemoriaArtistas

        dados = await cls.ler_json(f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Music/musicas.json')
        memoria.carregar(dados)

        await MemoriaArtistas.carregar()

    @classmethod
    def baixar_imagem(cls, url: str, caminho_destino: str) -> str | None:
        """
        Baixa uma imagem via URL e salva no caminho especificado.

        Args:
            url (str): URL da imagem
            caminho_destino (str): caminho completo (sem extensão ou com)

        Returns:
            str | None: caminho final salvo ou None se falhar
        """

        if not url:
            return None

        try:
            caminho = Path(caminho_destino)
            caminho.parent.mkdir(parents=True, exist_ok=True)

            response = requests.get(url, timeout=20)

            print(url)

            if response.status_code != 200:
                return None

            with open(caminho, "wb") as f:
                f.write(response.content)

            return str(caminho)
        except Exception as e:
            print("falha na conexão:", e)
            return None
    
    @classmethod
    def excluir_imagem(cls, caminho_img : str):
        try:
            if caminho_img and os.path.exists(caminho_img):
                os.remove(caminho_img)
                # print(f'Imagem removida: {caminho_img}')
            else:
                print(f'Imagem não encontrada: {caminho_img}')
        except Exception as erro:
            print(f'Erro ao remover a imagem: {erro}')

    
    # artistas
    @classmethod
    async def ler_artistas(cls) -> dict:
        return await cls.ler_json(
            f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Music/artistas.json'
        )
    
    @classmethod
    async def salvar_artistas(cls, data : dict):
        await cls.salvar_json(
            caminho = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Music/artistas.json',
            dados = data
        )