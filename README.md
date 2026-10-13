# TESTE

Repositório para estudar programação.

| Projeto | Pasta / arquivos |
|---|---|
| Calculadora ACR TI-RADS | `tirads.py`, `app.py` |
| Diagnóstico diferencial em TC de tórax | [`ddx_torax/`](ddx_torax/README.md) |

## Calculadora ACR TI-RADS

Calculadora de linha de comando em Python que classifica nódulos de tireoide
pelo sistema **ACR TI-RADS (2017)** e sugere a conduta (PAAF, seguimento ou nenhuma)
conforme o tamanho do nódulo.

> ⚠️ Projeto educacional. Não use para decisões clínicas.

### Como usar

Precisa do Python 3 instalado (nenhuma biblioteca extra).

```bash
python tirads.py
```

O programa pergunta composição, ecogenicidade, forma, margem, focos ecogênicos
e o maior diâmetro do nódulo, e então mostra a pontuação, o nível TR e a conduta.
Ao final, pergunta se você deseja avaliar outro nódulo.

### Versão web

A versão web (`app.py`) usa as mesmas regras do `tirads.py`, com botões e
resultado atualizado na hora. Para rodar no computador:

```bash
pip install -r requirements.txt
streamlit run app.py
```

O navegador abre sozinho em `http://localhost:8501`.

### Como rodar os testes

```bash
python -m unittest
```

### Regras usadas

| Pontos | Nível | PAAF se ≥ | Seguimento se ≥ |
|-------:|-------|----------:|----------------:|
| 0–1    | TR1   | —         | —               |
| 2      | TR2   | —         | —               |
| 3      | TR3   | 2,5 cm    | 1,5 cm          |
| 4–6    | TR4   | 1,5 cm    | 1,0 cm          |
| ≥ 7    | TR5   | 1,0 cm    | 0,5 cm          |
