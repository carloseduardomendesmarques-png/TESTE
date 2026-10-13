"""
Calculadora ACR TI-RADS (versão 2017)

Programa de estudo em Python: classifica um nódulo de tireoide pelas
características do ultrassom e sugere a conduta conforme o tamanho.

AVISO: projeto educacional. Não use para decisões clínicas reais.
"""

# ---------------------------------------------------------------------------
# 1) Tabelas de pontuação
# Cada categoria é um dicionário: {número da opção: (descrição, pontos)}
# ---------------------------------------------------------------------------

COMPOSICAO = {
    1: ("Cístico ou quase completamente cístico", 0),
    2: ("Espongiforme", 0),
    3: ("Misto cístico e sólido", 1),
    4: ("Sólido ou quase completamente sólido", 2),
}

ECOGENICIDADE = {
    1: ("Anecoico", 0),
    2: ("Hiperecoico ou isoecoico", 1),
    3: ("Hipoecoico", 2),
    4: ("Muito hipoecoico", 3),
}

FORMA = {
    1: ("Mais largo que alto", 0),
    2: ("Mais alto que largo", 3),
}

MARGEM = {
    1: ("Lisa", 0),
    2: ("Mal definida", 0),
    3: ("Lobulada ou irregular", 2),
    4: ("Extensão extratireoidiana", 3),
}

# Nesta categoria o usuário pode escolher MAIS DE UMA opção (os pontos somam)
FOCOS_ECOGENICOS = {
    1: ("Nenhum ou artefato em cauda de cometa grande", 0),
    2: ("Macrocalcificações", 1),
    3: ("Calcificações periféricas (em anel)", 2),
    4: ("Focos ecogênicos puntiformes", 3),
}

# Para cada nível TR: (FNA se tamanho >= X cm, seguimento se tamanho >= Y cm)
# None significa "não se aplica".
LIMIARES = {
    1: (None, None),
    2: (None, None),
    3: (2.5, 1.5),
    4: (1.5, 1.0),
    5: (1.0, 0.5),
}

DESCRICAO_TR = {
    1: "TR1 - Benigno",
    2: "TR2 - Não suspeito",
    3: "TR3 - Levemente suspeito",
    4: "TR4 - Moderadamente suspeito",
    5: "TR5 - Altamente suspeito",
}


# ---------------------------------------------------------------------------
# 2) Funções de cálculo (não fazem input/print, por isso são fáceis de testar)
# ---------------------------------------------------------------------------

def calcular_pontos(composicao, ecogenicidade, forma, margem, focos):
    """Soma os pontos. `focos` é uma lista com as opções escolhidas."""
    # Regra do ACR: nódulo espongiforme não recebe pontos das outras categorias
    if composicao == 2:
        return 0

    pontos = COMPOSICAO[composicao][1]
    pontos += ECOGENICIDADE[ecogenicidade][1]
    pontos += FORMA[forma][1]
    pontos += MARGEM[margem][1]
    for foco in focos:
        pontos += FOCOS_ECOGENICOS[foco][1]
    return pontos


def classificar(pontos):
    """Converte a pontuação total no nível TR (1 a 5)."""
    if pontos <= 1:
        return 1
    elif pontos == 2:
        return 2
    elif pontos == 3:
        return 3
    elif pontos <= 6:
        return 4
    else:
        return 5


def recomendar(tr, tamanho_cm):
    """Retorna a conduta sugerida para o nível TR e o maior diâmetro do nódulo."""
    limite_paaf, limite_seguimento = LIMIARES[tr]

    if limite_paaf is None:
        return "Sem indicação de PAAF."
    if tamanho_cm >= limite_paaf:
        return f"PAAF indicada (nódulo >= {limite_paaf} cm)."
    if tamanho_cm >= limite_seguimento:
        return f"Seguimento ultrassonográfico (nódulo >= {limite_seguimento} cm)."
    return "Sem indicação de PAAF ou seguimento."


# ---------------------------------------------------------------------------
# 3) Funções de interação com o usuário (input / print)
# ---------------------------------------------------------------------------

def perguntar_opcao(titulo, opcoes):
    """Mostra o menu e repete a pergunta até receber uma opção válida."""
    print(f"\n{titulo}")
    for numero, (descricao, pontos) in opcoes.items():
        print(f"  {numero}) {descricao} [{pontos} pt]")

    while True:
        resposta = input("Escolha: ").strip()
        if resposta.isdigit() and int(resposta) in opcoes:
            return int(resposta)
        print("Opção inválida, tente novamente.")


def perguntar_varias_opcoes(titulo, opcoes):
    """Igual a perguntar_opcao, mas aceita várias respostas separadas por vírgula."""
    print(f"\n{titulo} (pode escolher mais de uma, ex.: 2,4)")
    for numero, (descricao, pontos) in opcoes.items():
        print(f"  {numero}) {descricao} [{pontos} pt]")

    while True:
        partes = input("Escolha: ").replace(" ", "").split(",")
        if all(p.isdigit() and int(p) in opcoes for p in partes):
            # set() remove repetições, sorted() deixa em ordem
            return sorted(set(int(p) for p in partes))
        print("Opção inválida, tente novamente.")


def perguntar_tamanho():
    """Pede o maior diâmetro do nódulo em centímetros."""
    while True:
        texto = input("\nMaior diâmetro do nódulo (cm): ").strip().replace(",", ".")
        try:
            tamanho = float(texto)
        except ValueError:
            print("Digite um número, por exemplo 1.8")
            continue
        if tamanho > 0:
            return tamanho
        print("O tamanho precisa ser maior que zero.")


def main():
    print("=" * 50)
    print("  Calculadora ACR TI-RADS")
    print("  (uso educacional - não substitui avaliação médica)")
    print("=" * 50)

    composicao = perguntar_opcao("Composição:", COMPOSICAO)

    if composicao == 2:
        # Espongiforme: as demais categorias não somam pontos
        print("\nNódulo espongiforme: demais categorias não pontuam.")
        ecogenicidade, forma, margem, focos = 1, 1, 1, [1]
    else:
        ecogenicidade = perguntar_opcao("Ecogenicidade:", ECOGENICIDADE)
        forma = perguntar_opcao("Forma:", FORMA)
        margem = perguntar_opcao("Margem:", MARGEM)
        focos = perguntar_varias_opcoes("Focos ecogênicos:", FOCOS_ECOGENICOS)

    tamanho = perguntar_tamanho()

    pontos = calcular_pontos(composicao, ecogenicidade, forma, margem, focos)
    tr = classificar(pontos)

    print("\n" + "-" * 50)
    print(f"Pontuação total: {pontos}")
    print(f"Classificação:   {DESCRICAO_TR[tr]}")
    print(f"Conduta:         {recomendar(tr, tamanho)}")
    print("-" * 50)


# Este bloco só roda quando o arquivo é executado diretamente
# (python tirads.py), e não quando ele é importado pelos testes.
if __name__ == "__main__":
    main()
