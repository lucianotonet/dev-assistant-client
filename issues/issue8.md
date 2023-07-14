# Issue 8

## Issue Description

Durante a implementação de correções e melhorias no código, notamos que a abordagem atual de aplicar alterações ao código envolve a exclusão e recriação do arquivo inteiro. Embora isso garanta que as alterações sejam aplicadas corretamente, não é a abordagem mais eficiente.

Uma abordagem mais eficiente seria ler o arquivo, aplicar as alterações necessárias ao conteúdo lido e, em seguida, escrever o conteúdo alterado de volta ao arquivo. Isso evitaria a necessidade de excluir e recriar o arquivo inteiro, economizando recursos e tempo.

Esta issue é para investigar a possibilidade de implementar essa abordagem mais eficiente para aplicar alterações ao código.