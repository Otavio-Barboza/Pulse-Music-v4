# Estrutura da classe Scanner: fluxo de operação e funções importantes



**Fluxo de operação:**
-

### Antes de iniciar as descrições, a principal função que será destrinchada é:

    async def validate_data_json(cls, data: dict):
        data: config_play.json
        ...

- **Função base e linear do fluxo de execução para identificação de novas músicas ou músicas removidas + execução de recarregamento de cache e notificação de callbacks.**

---


### 1. Identificação Inicial de Dados:

- Nesse primeiro processo ocorre a identificação da pasta e quantidade de músicas da respectiva pasta.

    - **Pasta:** refere-se à/ao localização/diretório das músicas destinadas.
    - **Quantidade de Músicas:** conforme a pasta de músicas é feito o comando ___os.listdir()___ + a funçao nativa ___len()___ para obter a quantidade de músicas presentes na pasta (retorna-se um valor do tipo ___inteito [int]___). 


### 2. Atualização da Quantidade de Músicas ao config_play.json:

- Com a leitura do json já realizada, é atualizada a quantidade de músicas do valor do ___len()___ realizado anteriormente.


### 3. Verificação das Músicas (novas e removidos):

- Executa-se neste momento a função ___identify_songs()___ para retornar se houve músicas removidas ou adicionadas.
    
    ### OBS (parâmetro validate):
    - Se ___True___ considera um retorno e procura por novas músicas;
    - Se ___False___ considera um retorno e procura por músicas excluída;


### 4. Músicas Removidas:
- Lista de músicas novas para remover

    ### 4.1 chaves para remover:
    - Conjunto de chaves para serem removidas é obtido pela função ___get_key_for_path().___

    ### 4.2 Validação do Status de Operação do Scanner:
    - Return nulo caso o scanner já esteja ocupado, isso para evitar conflitos. 
    
    ### 4.3 Execução da Função delete_music():
    - Função para executar as remoções dos conteúdos de cada música da lista de remoção.
    
    ### 4.4 Recarregamento de Caches:
    - Executa o carregamento dos caches de artistas e global após as alterações.


### 5. Músicas Novas:
- Lista de músicas novas para adicionar
    
    ### 5.1 Validação do Status de Operação do Scanner:
    - Return nulo caso o scanner já esteja ocupado, isso para evitar conflitos. 

    ### 5.2 Execução da função new_song:
    - Função intermediária para o início do pipeline processar as novas músicas.
    
    ### 5.3 Recarregamento de Caches:
    - Executa o carregamento dos caches de artistas e global após as alterações.


### 6. Callbacks:
__Callbacks para atualização de dados são executados. Assim são os respectivos a seguir:__

1. Atualização da data de edição do config_play.json;
2. Salva config_play.json;
3. Se o modo __PlaylistState__.___playlist_loaded___ estiver aberta ( ___PlaylistLoaded.OPEN___ ), ou seja, a playlist do respectivo card clicado com as suas músicas carregadas é executado o callback de atualizar a listagem de músicas exibidas seja para adicionar ou remover;
4. Execução do callback da quantidade de músicas da respectiva playlist alterada (card);



---



**Funções Importantes:**
-


### 1. identify_songs():
- **Função para identificar músicas novas ou removidas. Por meio dos sets ela retorna a diferença entre um e outro o conforme o validate.**
  
    ### 1.1 Parâmetros:
    - path (str);
    - validate (bool) 

    ### 1.2 Fluxo de Execução da Função:
    1. Criação dos sets (músicas da pasta e músicas do songs.json) e leitura do songs.json;
    2. Adição dos caminhos para o set do songs.json; 
    3. Adição dos caminhos para o set da pasta de músicas;
    4. Criação da lista com a diferença entre os sets conforme o valor de validate;
    
    ### 1.3 Return:
    - list[str] - lista final de caminhos novos ou removidos.


### 2. get_key_for_path():
- **Função para retornar as chaves de cada músicas para remoção.**

    ### 2.1 Parâmetros:
    - paths (list[str])

    ### 2.2 Fluxo de Execução da Função:
    1. Criação do set das chaves e leitura do songs.json;
    2. Loop for - junção do caminho via Path - adição ao set o caminho completo

    ### 2.3 Return:
    - set[str] Conjunto com as chaves de cada música a ser removida.


### 3. new_song():
- **Função intermediaria do scanner com o pipeline.**

    ### 3.1 Parâmetros:
    - path (str)
    - list (list[str])

    ### 3.2 Fluxo de Execução da Função:
    1. for para cada playlist no ___os.listdir()___ do diretório playlists;
    2. Leitura dos config_play.json de cada playlist;
    3. Comparação entre caminhos, se iguais é definido o playlist_id e para o loop for;
    4. Inicia a execução do pipeline para as novas músicas.

### 4. delete_music():
- **Função para gerenciar o processo de exclusão de músicas.**
    
    ### 4.1 Parâmetros:
    - keys (set[str])

    ### 4.2 Fluxo de Execução da Função:
    1. Definição de status e quantidade de tarefas ativas do scanner;
    2. Notificando conteúdo do drawer do scanner;
    3. Chama a função do ___item 5.___ a seguir;
    4. Definição de status e quantidade de tarefas ativas do scanner.


### 5. identify_artists_albums_existings(keys_to_remove):
- **Função para identificar artistas e álbuns existentes ou não e exclusão de dados não existentes.**

    ### 5.1 Parâmetros:
    - keys_to_remove (set[str])

    ### 5.2 Fluxo de Execução da Função:
    1. Criação dos dicionários base de artistas e álbuns;
    2. Leitura de songs.json e lyrics.json;
    3. Atribuindo todas as imagens existentes (via songs.json) aos dicionários criados;
    4. Loop for em songs.json;
    5. Variaveis auxiliares contendo o nome do artista e do álbum de cada música são criadas no loop;
    6. Variaveis auxiliares contendo o caminho completo do artista e do álbum de cada música são criadas no loop;
    
    7. Se a chave estar contida em ___keys_to_remove___:
        
        7.1. Variáveis auxiliares para pegar a diferença de do set se chaves, ou seja, as chaves restantes, remanescentes da diferença;
        
        7.2 Nome e caminho das capas são atribuídos em uma variável auxiliar;

        7.3 Se a quantidade de álbuns remanescentes for igual a 0, esclui a imagem do álbum. Isto é, caso não exista mais nenhuma música do mesmo álbum, o respectivo poderá ser excluído;

        7.4 Se a quantidade de artistas remanescentes for igual a 0, esclui a imagem do artista. Isto é, caso não exista mais nenhuma música do mesmo artista, o respectivo poderá ser excluído;

        7.5 Exclusão das capas de cada música do loop;

        7.6 Adiciona-se a chave da atual música do loop à variável ___keys_for_remove___.

    8. Loop for em ___keys_for_remove___ para deletar cada chave (música) os seus dados em songs.json e lyrics.json;
    9. Salva os dados atualizados nos JSONs (songs.json e lyrics.json);
    10. Notificação de callbacks (grids).