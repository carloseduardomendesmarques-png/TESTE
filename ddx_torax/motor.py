"""
Motor de pontuação: compara os itens selecionados com o perfil de cada doença.

Regras
------
1. Pontuação = soma dos pesos da doença para cada item selecionado.
2. A doença só entra na lista se ao menos um PADRÃO selecionado (achado
   principal) contar a favor dela. Distribuição ou clínica sozinhas não bastam.
3. Classificação:
     Alta   pontuação >= 7  e  >= 80% da maior pontuação do caso
     Média  pontuação >= 4
     Baixa  pontuação >= 1
   Doenças com pontuação <= 0 não aparecem.

Esses limites foram calibrados com os casos clássicos de test_ddx.py.
"""

from base_conhecimento import CLINICA, DISTRIBUICAO, DOENCAS, PADROES, TEMPOS, TODOS_ITENS

LIMITE_ALTA = 7
FRACAO_DO_MELHOR = 0.8
LIMITE_MEDIA = 4
LIMITE_BAIXA = 1

ORDEM_NIVEIS = {"Alta": 0, "Média": 1, "Baixa": 2}


def pontuar(doenca, selecionados):
    """Retorna (pontos, itens a favor, itens contra) de uma doença."""
    pesos = doenca["pesos"]
    a_favor = [item for item in selecionados if pesos.get(item, 0) > 0]
    contra = [item for item in selecionados if pesos.get(item, 0) < 0]
    pontos = sum(pesos.get(item, 0) for item in selecionados)
    return pontos, a_favor, contra


def achados_tipicos_ausentes(doenca, selecionados):
    """Achados de imagem com peso 3 para a doença que não foram selecionados."""
    return [
        item for item, peso in doenca["pesos"].items()
        if peso == 3 and item not in selecionados and item in PADROES
    ]


def avaliar(selecionados):
    """
    Recebe um conjunto com os ids selecionados (achados, distribuição,
    associados, tempo e clínica) e retorna a lista de diagnósticos
    ordenada do mais para o menos provável.
    """
    selecionados = set(selecionados)
    candidatos = []

    for doenca in DOENCAS:
        pontos, a_favor, contra = pontuar(doenca, selecionados)
        tem_padrao_a_favor = any(item in PADROES for item in a_favor)
        if tem_padrao_a_favor and pontos >= LIMITE_BAIXA:
            candidatos.append({
                "doenca": doenca,
                "pontos": pontos,
                "a_favor": sorted(a_favor, key=lambda i: -doenca["pesos"][i]),
                "contra": sorted(contra, key=lambda i: doenca["pesos"][i]),
                "procurar": achados_tipicos_ausentes(doenca, selecionados),
            })

    if not candidatos:
        return []

    melhor = max(c["pontos"] for c in candidatos)
    for c in candidatos:
        if c["pontos"] >= LIMITE_ALTA and c["pontos"] >= FRACAO_DO_MELHOR * melhor:
            c["nivel"] = "Alta"
        elif c["pontos"] >= LIMITE_MEDIA:
            c["nivel"] = "Média"
        else:
            c["nivel"] = "Baixa"

    candidatos.sort(key=lambda c: (ORDEM_NIVEIS[c["nivel"]], -c["pontos"]))
    return candidatos


def avisos(selecionados, resultado):
    """Alertas para quando a descrição é incompleta e o ranking fica pouco confiável."""
    mensagens = []
    selecionados = set(selecionados)

    if not selecionados & set(DISTRIBUICAO):
        mensagens.append("Nenhuma distribuição selecionada: ela costuma ser decisiva no diferencial.")
    if not selecionados & set(TEMPOS):
        mensagens.append("Tempo de evolução não informado.")
    if not selecionados & set(CLINICA):
        mensagens.append("Nenhum dado clínico selecionado.")

    altas = sum(1 for r in resultado if r["nivel"] == "Alta")
    if altas > 3:
        mensagens.append(
            f"{altas} diagnósticos com probabilidade alta: o quadro descrito é pouco específico. "
            "Acrescente achados para diferenciar."
        )
    return mensagens


def nome_item(item):
    """Converte o id de um item no texto que aparece na tela."""
    return TODOS_ITENS[item]
