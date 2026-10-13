"""
Calculadora ACR TI-RADS - versão web (Streamlit)

Usa as mesmas tabelas e funções de cálculo do tirads.py, então a regra
fica em um lugar só (e já está coberta pelos testes).

Para rodar no computador:  streamlit run app.py

AVISO: projeto educacional. Não use para decisões clínicas reais.
"""

import streamlit as st

from tirads import (
    COMPOSICAO,
    DESCRICAO_TR,
    ECOGENICIDADE,
    FOCOS_ECOGENICOS,
    FORMA,
    MARGEM,
    calcular_pontos,
    classificar,
    recomendar,
)

st.set_page_config(page_title="Calculadora ACR TI-RADS", page_icon="🩺")


def escolher(titulo, opcoes):
    """Mostra as opções de uma categoria como botões de rádio e retorna o número escolhido."""
    return st.radio(
        titulo,
        options=list(opcoes.keys()),
        # format_func define o texto que aparece para cada opção
        format_func=lambda numero: f"{opcoes[numero][0]} ({opcoes[numero][1]} pt)",
    )


st.title("🩺 Calculadora ACR TI-RADS")
st.caption("Uso educacional — não substitui avaliação médica.")

composicao = escolher("Composição", COMPOSICAO)

if composicao == 2:
    # Espongiforme: as demais categorias não somam pontos
    st.info("Nódulo espongiforme: as demais categorias não pontuam.")
    ecogenicidade, forma, margem, focos = 1, 1, 1, [1]
else:
    ecogenicidade = escolher("Ecogenicidade", ECOGENICIDADE)
    forma = escolher("Forma", FORMA)
    margem = escolher("Margem", MARGEM)

    # Focos ecogênicos: pode marcar mais de um (os pontos somam)
    st.write("**Focos ecogênicos** (marque todos os presentes)")
    focos = []
    for numero, (descricao, pontos) in FOCOS_ECOGENICOS.items():
        if numero == 1:
            continue  # "Nenhum" = nenhuma caixa marcada
        if st.checkbox(f"{descricao} ({pontos} pt)"):
            focos.append(numero)
    if not focos:
        focos = [1]

tamanho = st.number_input(
    "Maior diâmetro do nódulo (cm)", min_value=0.1, value=1.0, step=0.1, format="%.1f"
)

# O Streamlit roda o script de novo a cada clique, então o resultado
# está sempre atualizado — não precisa de botão "Calcular".
pontos = calcular_pontos(composicao, ecogenicidade, forma, margem, focos)
tr = classificar(pontos)
conduta = recomendar(tr, tamanho)

st.divider()
st.subheader("Resultado")
st.metric("Pontuação total", pontos)

# Cor do quadro conforme o nível de suspeição
if tr <= 2:
    st.success(DESCRICAO_TR[tr])
elif tr == 3:
    st.info(DESCRICAO_TR[tr])
elif tr == 4:
    st.warning(DESCRICAO_TR[tr])
else:
    st.error(DESCRICAO_TR[tr])

st.write(f"**Conduta:** {conduta}")
