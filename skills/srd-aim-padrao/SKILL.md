---
name: srd-aim-padrao
description: Cria e atualiza solicitações de reembolso (SRDs) em formulário A4 compacto, anexa comprovantes e mantém histórico por colaborador. Use para SRD, reembolso ou planilha de controle nesse padrão; não use para recibos de benefícios.
metadata:
  short-description: Cria SRDs e controles de reembolso
---

# SRD em padrão compacto

Monte solicitações de reembolso com formulário A4 vertical, comprovantes anexos e, quando solicitado, controle mensal. Leia [a referência](references/referencia-do-padrao.md) para campos, anexos e nomes de arquivo.

## Regras

- Gere um PDF por SRD, com formulário na primeira página e comprovantes depois.
- Entregue Excel quando solicitado ou necessário para edição.
- Separe por número, colaborador, projeto ou finalidade conforme o pedido.
- Preserve exatamente os dados fornecidos.
- Nunca invente número, valor, comprovante, projeto ou dados bancários. Pergunte se faltar algo indispensável; declare pendências não bloqueantes.
- Não preencha assinaturas, carimbos ou aprovações.
- Identifique pagamento feito por terceiro.
- Use o valor efetivamente pago e não duplique nota e comprovante.

## Formulário

- Use A4 vertical, margens de impressão e layout compacto.
- Inclua cabeçalho, solicitante, documento fiscal, projeto/núcleo, pagamento, data e número.
- Use as colunas `ITEM`, `NATUREZA`, `DESCRIÇÃO`, `DATA` e `VALOR`.
- Inclua total, contexto e blocos de assinatura.
- Evite texto pequeno, cortes e sobreposição.
- Escolha natureza objetiva e descreva item, fornecedor/plataforma e finalidade.

## Controle mensal

Quando solicitado, crie `Última por colaborador` e `Histórico`. No histórico use: Colaborador, Número SRD, Data, Projeto/Núcleo, Valor, Descrição, Responsável, Status e Arquivo PDF. Aplique filtros, cabeçalho congelado, moeda numérica e status claros.

## Validação e privacidade

Confira soma, número, projeto, solicitante, datas e comprovantes; revise o PDF visualmente. Nunca versione SRDs preenchidas, comprovantes, documentos, PIX, dados bancários ou assinaturas reais.

