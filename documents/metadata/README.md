# Organização e Estrutura de Metadados Salvos em Cada JSON


1. **songs.json**

    - JSON base de toda a aplicação;
    - Os dados gerais necessitados pelo app são salvos neste arquivo.


2. **artists.json**

    - JSON usado como um cache de artistas;
    - Auxilio na identificação por novos artistas e gerencimento controlado no app.


3. **favorites.json**

    - Guarda as referencias das músicas favoritadas, auxiliando o processo e gerencimento das favoritas.


4. **lyrics.json**

    - JSON para manipular e armazenar as referências de letras musicais de cada música;
    - Gerencia releases (letras traduzidas).