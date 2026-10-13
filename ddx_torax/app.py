"""
Diagnóstico diferencial em TC de tórax - versão web (Streamlit)

Para rodar no computador (a partir da raiz do repositório):
    streamlit run ddx_torax/app.py

AVISO: ferramenta educacional. Não substitui o julgamento clínico-radiológico.
"""

import streamlit as st

from base_conhecimento import CATEGORIAS, REFERENCIAS, TEMPOS
from motor import avaliar, avisos, nome_item

st.set_page_config(page_title="DDx TC de Tórax", page_icon="🫁")

ICONE_NIVEL = {"Alta": "🔴", "Média": "🟠", "Baixa": "🟢"}

st.title("🫁 Diagnóstico diferencial em TC de tórax")
st.caption(
    "Ferramenta educacional — as probabilidades são estimativas baseadas em pesos "
    "da literatura e não substituem o julgamento clínico-radiológico."
)

# ---------------------------------------------------------------------------
# Entrada: o médico seleciona os itens de cada categoria
# ---------------------------------------------------------------------------

selecionados = set()

for titulo, itens in CATEGORIAS.items():
    escolhidos = st.multiselect(
        titulo,
        options=list(itens.keys()),
        format_func=nome_item,
        placeholder="Selecione...",
    )
    selecionados.update(escolhidos)

    # O tempo de evolução fica logo depois dos achados associados
    if titulo == "Achados associados":
        tempo = st.radio(
            "Tempo de evolução",
            options=[None, *TEMPOS.keys()],
            format_func=lambda t: "Não informado" if t is None else TEMPOS[t],
            horizontal=True,
        )
        if tempo:
            selecionados.add(tempo)

# ---------------------------------------------------------------------------
# Resultado
# ---------------------------------------------------------------------------

st.divider()
st.subheader("Hipóteses diagnósticas")

resultado = avaliar(selecionados)

if not resultado:
    st.write("Selecione ao menos um padrão de imagem para ver as hipóteses.")
else:
    for mensagem in avisos(selecionados, resultado):
        st.caption(f"⚠️ {mensagem}")

    for r in resultado:
        doenca = r["doenca"]
        titulo = f"{ICONE_NIVEL[r['nivel']]} **{doenca['nome']}** — probabilidade {r['nivel'].lower()} ({r['pontos']} pts)"

        with st.expander(titulo):
            st.caption(doenca["grupo"])
            st.write(f"💡 {doenca['dica']}")
            if r["a_favor"]:
                st.write("**A favor:** " + "; ".join(nome_item(i) for i in r["a_favor"]))
            if r["contra"]:
                st.write("**Contra:** " + "; ".join(nome_item(i) for i in r["contra"]))
            if r["procurar"]:
                st.write("**Achados típicos não descritos:** "
                         + "; ".join(nome_item(i) for i in r["procurar"]))

with st.expander("Como a pontuação funciona"):
    st.markdown(
        "Cada doença tem pesos de **−3 a +3** para cada achado, distribuição, tempo de "
        "evolução e dado clínico. A pontuação é a soma dos pesos dos itens selecionados.\n\n"
        "- **Alta:** ≥ 7 pontos e ≥ 80% da maior pontuação do caso\n"
        "- **Média:** ≥ 4 pontos\n"
        "- **Baixa:** 1 a 3 pontos\n\n"
        "A doença só aparece se pelo menos um **padrão de imagem** selecionado contar a favor dela."
    )

with st.expander("Referências"):
    for ref in REFERENCIAS:
        st.markdown(f"- {ref}")
