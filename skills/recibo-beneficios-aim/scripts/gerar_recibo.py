from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
import zipfile

from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
UNIDADES = ["zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove"]
DEZ_A_DEZENOVE = ["dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"]
DEZENAS = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"]
CENTENAS = ["", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos", "seiscentos", "setecentos", "oitocentos", "novecentos"]


def inteiro_extenso(n: int) -> str:
    if n < 0 or n > 999_999:
        raise ValueError("O valor deve estar entre 0 e 999.999 reais")
    if n < 10:
        return UNIDADES[n]
    if n < 20:
        return DEZ_A_DEZENOVE[n - 10]
    if n < 100:
        return DEZENAS[n // 10] + (" e " + UNIDADES[n % 10] if n % 10 else "")
    if n == 100:
        return "cem"
    if n < 1000:
        return CENTENAS[n // 100] + (" e " + inteiro_extenso(n % 100) if n % 100 else "")
    milhares, resto = divmod(n, 1000)
    prefixo = "mil" if milhares == 1 else inteiro_extenso(milhares) + " mil"
    if not resto:
        return prefixo
    ligacao = " e " if resto < 100 or resto % 100 == 0 else " "
    return prefixo + ligacao + inteiro_extenso(resto)


def moeda_extenso(texto: str) -> tuple[str, str]:
    try:
        valor = Decimal(texto.replace(".", "").replace(",", ".")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except InvalidOperation as exc:
        raise ValueError(f"Valor inválido: {texto}") from exc
    if valor < 0:
        raise ValueError("O valor não pode ser negativo")
    reais = int(valor)
    centavos = int((valor - reais) * 100)
    partes = []
    if reais:
        partes.append(f"{inteiro_extenso(reais)} {'real' if reais == 1 else 'reais'}")
    if centavos:
        partes.append(f"{inteiro_extenso(centavos)} {'centavo' if centavos == 1 else 'centavos'}")
    if not partes:
        partes.append("zero reais")
    numerico = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return numerico, " e ".join(partes)


def data_pt(texto: str) -> tuple[str, str]:
    data = datetime.strptime(texto, "%d/%m/%Y")
    return data.strftime("%d/%m/%Y"), f"{data.day:02d} de {MESES[data.month - 1]} de {data.year}"


def set_texts(paragraph, values):
    nodes = paragraph.xpath(".//w:t", namespaces=NS)
    if len(values) > len(nodes):
        raise RuntimeError(f"O slot possui {len(nodes)} trechos e recebeu {len(values)}")
    for node, value in zip(nodes, values):
        node.text = value
        key = "{http://www.w3.org/XML/1998/namespace}space"
        if value.startswith(" ") or value.endswith(" "):
            node.set(key, "preserve")
        else:
            node.attrib.pop(key, None)
    for node in nodes[len(values):]:
        node.text = ""


def main():
    parser = argparse.ArgumentParser(description="Gera recibo de benefícios AIM")
    for field in ("nome", "valor", "beneficio", "inicio", "fim", "pagamento", "obra", "saida"):
        parser.add_argument(f"--{field}", required=True)
    parser.add_argument("--dias", required=True, type=int)
    args = parser.parse_args()
    if args.dias <= 0:
        parser.error("--dias deve ser maior que zero")

    valor, extenso = moeda_extenso(args.valor)
    inicio, _ = data_pt(args.inicio)
    fim, _ = data_pt(args.fim)
    _, pagamento = data_pt(args.pagamento)
    modelo = Path(__file__).resolve().parents[1] / "assets" / "modelo-recibo-aim.docx"
    saida = Path(args.saida).resolve()
    saida.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(modelo, "r") as zin:
        document = etree.fromstring(zin.read("word/document.xml"))
        body = document.find(f"{{{W}}}body")
        paragraphs = [node for node in body if node.tag == f"{{{W}}}p"]
        set_texts(paragraphs[2], ["R$ ", valor])
        set_texts(paragraphs[7], [
            "Recebi da empresa ", "AIM Properties Construtora e Administradora de Imóveis Ltda",
            ", a importância supra de R$ ", valor, ",(", extenso[:1].upper() + extenso[1:],
            "), correspondente a ", args.beneficio, " de ", f"{args.dias} ",
            "dia" if args.dias == 1 else "dias", " do ", f"{inicio} ao {fim} ", "no dia ",
            f"{pagamento} ", "na obra de ", args.obra.rstrip(".") + ".",
        ])
        set_texts(paragraphs[11], ["Rio de Janeiro, ", pagamento, "."])
        set_texts(paragraphs[15], [args.nome.rstrip("."), "."])
        updated = etree.tostring(document, xml_declaration=True, encoding="UTF-8", standalone=True)
        with zipfile.ZipFile(saida, "w") as zout:
            for item in zin.infolist():
                data = updated if item.filename == "word/document.xml" else zin.read(item.filename)
                zout.writestr(deepcopy(item), data)
    print(saida)


if __name__ == "__main__":
    main()
