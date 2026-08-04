# Fluxo de Execução de armazenamento das imagens


### Capas de Músicas (covers):

- São extraídas já ao inicio do pipeline;
- Todas capas são provenientes enquanto metadados imbutidos nos arquivos.


### Imagens Provenientes da Deezer (artistas e álbuns):

- Durante a operação do pipeline, independente da fase (excessão à fase 0), após a definição do artistas final, requere-se a API da Deezer par abter as imagens dos artistas e álbuns;
- Com a captação dos dados, e definição dos dados no objeto SongMetadata em edição, efetua-se o download da imagem e salva-a fisicamente no diretório: 
    
    1. **Artistas:**

            Seu Diretório\\APPDATA\\LOCAL\\Barboza Software\\Pulse Music\\account\\Sua Conta Logada\\images\\artists
    
        - Os artistas são salvos com os seus IDs gerenciados pelo cache global junto ao artists.json.

    2. **Álbuns:**
            
            Seu Diretório\\APPDATA\\LOCAL\\Barboza Software\\Pulse Music\\account\\Sua Conta Logada\\images\\albums

        - Os álbuns são salvos com o seu nome devido apresentarem uma complexidade menor em relação aos seus nomes do que em relação aos artistas.

- Essas imagens são exibidas nas abas na tela principal da aplicação e permitindo a funcionalidade de clicar em alguma das imagens expandindo a tela com as músicas daquele artista/álbum em específico com opção da reprodução em fila dessas músicas.


### Fluxo de Carregamento das Imagens nas Abas Principais do App:

1. **Artistas:**

    - Faz a leitura da pasta onde fica armazenada as imagens (os.listdir(pasta de destino));
    - Com a leitura, faz a busca de cada imagem. Como já são salvas pelos IDs, apenas buscas pela chave em que for o ID da respectiva imagem no cache de artistas;
    - Se identificada, remove-se o sufixo (.jpg, .png, .jpeg...) e adiciona ao controls da grid. Senão descarta a imagem.

2. **Álbuns:**

    - Faz a leitura da pasta onde fica armazenada as imagens;
    - Realiza a remoção do sufixo (.jpg, .png, .jpeg...). Para esse modo não necessita de nenhum processo extra como o de artistas;
    - Finaliza adicionando-a ao controls da grid.

#### OBS: Se a imagem não conter nenhum dos sufixos citados, automaticamente é descartada, isso para evitar erros e inconsistências no aplicativo em suas funcionalidades.