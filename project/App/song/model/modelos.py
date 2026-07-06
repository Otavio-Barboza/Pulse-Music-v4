from dataclasses import dataclass

@dataclass
class EstadoPlayer:
    musica_atual : object = None
    tocando : bool = False
    tempo_atual : float = 0.0
    duracao_total : float = 0.0
    volume : float = 1.0

@dataclass
class ConfiguracaoReproducao:
    aleatorio : bool = False
    repetir : bool = False