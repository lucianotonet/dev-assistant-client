# Issue 7

## Adicionar git_diff no módulo git

Atualmente, o módulo git não possui um método para gerar diffs do git. Esta funcionalidade é necessária para implementar a solução proposta na Issue 1 para o manuseio de arquivos grandes.

### Proposta

Adicionar um método `git_diff` ao módulo git que gera um diff do git para um arquivo específico. Este método deve aceitar o caminho do arquivo como argumento e retornar o diff do git como uma string.

Além disso, outros métodos necessários devem ser adicionados ao módulo git para suportar esta funcionalidade.