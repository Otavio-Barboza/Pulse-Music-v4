# Pulse Music v4

Projeto desenvolvido como Trabalho de Conclusão de Curso; 
Efetuando ainda no Ensino Médio Técnico Integrado (Informática);
No Instituto Federal do Paraná - Campus Jacarezinho.

Este ainda é um trabalho em desenvolvimento, portanto, pode conter erros, explicações rasas e funcionalidades pré-implementadas ou em fase beta de desenvolvimento.
As versões estáveis estão destacadas no título em caixa alta (ESTÁVEL ou FINAL).

# Ateção!

Observe o .gitignore se for usar o código;
No repostório está subindo apenas arquivos de exemplos;
O exemplos estão para suprir quaisquer vazamento de dados captados;


# Qual a proposta?

A proposta consiste no desenvolvimento de um plyer de música;
Baseia-se na linguagem de programação Python para back-end;
Utiliza-se de um framework do Python (FLET) para criar a interface gráfica;
Usa de arquivos .json para armazenamento de dados temporários e locais, além de arquivos .png/.jpg e base64 para imagens locais.

A base operacional do player é inspirada em players/reprodutores tradicionais.
EX: Reprodutor Multimídia do Windows, Sansung Music, Reprodutor MP3 entre outros...


# Modelo de captação de dados e gerenciamento de metadados

Modelo base de captação de dados: Pipeline estruturado em fases.

Para enriquecimento e diferencial, foi aplicado o uso das APIs:
-> Deezer (artistas e álbuns);
-> Genius (letra da música);

Outra fonte de dados são os metadados utilizados, principalmente buscando obter o máximo de informações de cada música;
Dentre os metadados predominam os modelos ID3. Os metadados são captado em:

(a) Título da música / nome intregral do arquivo .mp3;
(b) Artista embutido nativamente;
(c) Imagem da capa da música;

Um modelo aplicado além do requerimento das APIs, onde a Genius possui a sua operação específica, e a Deezer, funcionando mais como um fallback (validador).
Antes de usar a API da Deezer, no processo da captação do dados, é executado classificações e filtragens (via re [biblioteca do Python] / regex) do nome do arquivo .mp3 ou do título, com isso pode-se obter artista e nome da música, o que é posteriormente requerido a Deezer, captado as imagens além dela atuar como validador junto a similaridade (SequenceMatcher) para definir o dado final.

Quando passado toda essa execução, possui a gravação dos dados em arquivo do formato JSON, e gerenciamento de dados em memória, o que facilita na exibição destes na aplicação.

OBS: Os dados captados são inseridos diretamente ao arquivo de música, o que permite uma releitura futura mais rápida, matendo fluidez do app.

Um recurso dinâmico, é o scanner, atuando como um monitor em tempo real, onde o usuário pode adicionar ou remover as músicas da pasta com o aplicativo aberto, assim a aplicação realizando todos os tramites automaticamente.


# Operação do Player

I. O player lê a pasta de músicas (sua playlist) e aplica um algoritmo que capta todos os dados (artistas, álbuns e suas imagens).
A letra da música é captada ao tocar a música (para aliviar o alto fluxo de componentes em operação simultânea). --- (Funcionalidade ainda falta ser reimplementada).
II. Voçê pode criar múltiplas playlists e personalizá-las com as imagens de capa musical e álbum além da cofiguração da cor de fundo do card da playlist e sua opacidade da cor (senão existir alguma img salva, possui imagem e cor definidas por padrão).
III. A aplicação possui a visualização de artistas e álbuns (imagens) e cada um com as suas músicas que forem possíveis de serem identificadas.
IV. A reprodução básica de áudio está presente, além da opção de favoritar e ouvir por artista ou álbum (AINDA EM REIMPLEMENTAÇÃO).
V. Possui recurso de pesquisar músicas, redirecionando a pesquisa no YouTube conforme a música atribuída.
VI. Possui overlays interativos para informação e avisos.
VII. A tela de configurações para gerenciamento de login, personalização (AINDA A SER IMPLEMENTADO), suporte (envio de email), configurações gerais e sobre o aplicativo.
VIII. Também há a possibilidade de visualizar a letra da música.