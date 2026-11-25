# Atualizações da  P1
1. marcar_entregue apagava o pedido (perda de histórico) – corrigido.
2. Sem validação de estoque/quantidade ao adicionar ao carrinho – corrigido.
3. Views usam Model.objects.get(...) e dão erro 500 se o id não existe; trocar por get_object_or_404.
4. aplicar_cupom não confere validade nem o campo `utilizado` (e `utilizado` nunca vira True); total pode ficar negativo se desconto > total.
5. Qualquer pessoa abre o carrinho de outro trocando o id na URL (sem dono/validação)

### Perguntas do dono da loja (base do dashboard)
| Pergunta | Tipo | Métrica |
|---|---|---|
| Quanto faturei? Quantos pedidos? | KPI | Sum / Count |
| Quais produtos mais vendem? | Ranking | values + annotate + order_by |
| Como evoluem as vendas por mês? | Série | TruncMonth |
| Em que status estão os pedidos? | Distribuição | values + annotate |
| O que está com estoque baixo? | Lista | filter(estoque__lte) |