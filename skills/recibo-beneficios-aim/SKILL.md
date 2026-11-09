---
name: recibo-beneficios-aim
description: Cria recibos de adiantamento de benefícios em DOCX e PDF, preservando um modelo institucional autorizado e preenchendo colaborador, valor, benefício, dias, período, pagamento e obra. Use para recibos de refeição, transporte ou ambos; não use para reembolsos/SRD nem fornecedores.
metadata:
  short-description: Gera recibos de benefícios em Word e PDF
---

# Recibos de benefícios

Gere o recibo a partir de `assets/modelo-recibo-aim.docx`; não recrie o visual. O template corporativo não acompanha a versão pública: o usuário deve adicionar uma cópia autorizada nesse caminho.

## Dados necessários

Obtenha nome do colaborador, valor, benefício, dias, início e fim do período, data de pagamento/emissão e obra. Reutilize contexto somente em continuação clara. Pergunte quando uma suposição puder emitir recibo incorreto.

## Gerar DOCX

Execute:

```powershell
python scripts/gerar_recibo.py `
  --nome "Colaborador Exemplo" --valor "416,50" `
  --beneficio "refeição e transporte" --dias 10 `
  --inicio "19/08/2026" --fim "01/09/2026" `
  --pagamento "21/08/2026" --obra "Obra Exemplo" `
  --saida "recibo.docx"
```

Mantenha valor numérico e por extenso, período, pagamento e campos de assinatura do modelo.

## PDF e verificação

Quando solicitado, execute `scripts/exportar_pdf.ps1`, renderize o PDF e inspecione a página inteira.

- Confirme uma página A4.
- Confira nome, valor, dias, período, pagamento, benefício e obra.
- Confirme que não há cortes, sobreposição ou alteração indevida no cabeçalho, marca d'água, assinaturas e rodapé.
- Entregue apenas o formato solicitado; para impressão, prefira PDF.

## Privacidade

Não versione modelo sem autorização, recibos preenchidos, nomes, valores, assinaturas ou outros dados de produção.

