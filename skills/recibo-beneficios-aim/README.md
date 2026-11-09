# Recibos de benefícios

Preenche um modelo DOCX autorizado e gera recibos de refeição, transporte ou ambos, com valor por extenso e opção de PDF.

## Aplicabilidades

- adiantamento de refeição e transporte;
- períodos com quantidade definida de dias;
- geração em lote a partir do mesmo modelo;
- documento pronto para impressão e assinatura.

## Requisitos

- Python 3;
- pacote `lxml`;
- Microsoft Word no Windows para a exportação PDF;
- template autorizado em `assets/modelo-recibo-aim.docx`.

Instale a dependência:

```powershell
python -m pip install lxml
```

O template original foi intencionalmente omitido da versão pública porque continha identidade institucional e metadados embutidos. Adicione somente um modelo que você tenha autorização para redistribuir ou usar localmente.

## Exemplo

> Use `$recibo-beneficios-aim` para gerar um recibo de transporte de 10 dias, usando os dados fictícios fornecidos, e entregue em PDF.

## Cuidados

Valide sempre valores, datas e período. Não publique recibos gerados, assinaturas ou dados de colaboradores.

