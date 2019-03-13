# rv-schubert-sdk
SDK de integração com a RV Tecnologia por meio de sua `API XML`

### Dependências
Atualmente o SDK é dependente dos seguintes pacotes:

```
- xmltodict
- json
- requests
- pendulum
```


### Considerações
O objeto `Recarga`, retorna as datas por padrão usando a lib `pendulum` pois é mais pratico para calculos de datas se 
houver necessidade.

O objeto `Recarga` nada mais é que um helper para acessar a resposta padrão da `API` da `RV`.

### Integrações e tarefas pendentes
#### Transações
- [X] 1  - Consulta de Produtos e Operadoras
- [X] 3  - Venda de PINs
- [ ] 5  - Venda de RECARGA ONLINE
- [ ] 6  - Consulta de Status
- [ ] 7  - Confirmação / Desfazimento de Transações
- [ ] 8  - Lista de Transações Pendentes
- [ ] 9  - Consulta Limite de Crédito
- [ ] 10 - Consulta Lista de Boletos
- [ ] 11 - Consulta de Boleto
- [ ] 12 - Emissão Boleto Antecipado
- [ ] 13 - Consulta Totais por Dia
- [ ] 15 - Detalhe Venda
- [ ] 16 - Resumo Vendas
- [ ] 17 - Relatório Vendas
- [ ] 18 - Lista Vendas

#### Implementar erros customizados para facilitar tratamento
- [ ] 1 Fone Incompleto / Invalido
- [ ] 2 Limite de Crédito Insuficiente
- [ ] 3 Estoque Insuficiente
- [ ] 4 Telefone não autorizado
- [ ] 5 Senha Inválida
- [ ] 6 Máximo número de conexões atingida
- [ ] 7 Sistema em Manutenção
- [ ] 8 Operadora / Produto não encontrado
- [ ] 9 Código inválido
- [ ] 10 Valor Inválido
- [ ] 11 Timeout
- [ ] 13 Compra Expirada
- [ ] 14 Compra inexistente
- [ ] 15 Usuario/Loja não encontrados
- [ ] 16 Parâmetros Insuficientes
- [ ] 17 Compra já confirmada
- [ ] 18 Boleto não Encontrado
- [ ] 19 Parametros não enviados via POST
- [ ] 20 Codigo de Transacao não informado
- [ ] 21 Versão não informada
- [ ] 22 Usuário sem nível de acesso
- [ ] 23 Cobrança ainda não visualizada
- [ ] 24 Transação não permitida