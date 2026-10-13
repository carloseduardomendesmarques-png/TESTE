# Diagnóstico diferencial em TC de tórax

Ferramenta educacional: o médico seleciona os **achados de TC de tórax**, a
**distribuição**, os **achados associados**, o **tempo de evolução** e os
**dados clínicos**, e o programa lista as hipóteses diagnósticas com
probabilidade **alta, média ou baixa**, mostrando o que pesou a favor e contra.

> ⚠️ Uso educacional. As probabilidades são estimativas a partir de pesos
> definidos com base na literatura, não probabilidades medidas. Não substitui
> o julgamento clínico-radiológico.

## Arquivos

| Arquivo | O que faz |
|---|---|
| `base_conhecimento.py` | Vocabulário de achados (Glossário Fleischner), ~40 doenças com seus pesos e as referências |
| `motor.py` | Soma os pesos, classifica em alta/média/baixa e gera avisos |
| `app.py` | Página web (Streamlit) |
| `test_ddx.py` | Testes, incluindo 22 casos clássicos que devem ficar em 1º lugar |

## Como rodar

A partir da raiz do repositório:

```bash
pip install -r requirements.txt
streamlit run ddx_torax/app.py        # página web
python -m unittest discover ddx_torax # testes
```

## Como a pontuação funciona

Cada doença tem pesos de **−3 a +3** para cada item:

| Peso | Significado |
|---:|---|
| 3 | muito característico |
| 2 | sugestivo |
| 1 | compatível, mas inespecífico |
| −1 | pouco comum |
| −2 | fala contra |
| −3 | praticamente afasta |

A pontuação é a soma dos pesos dos itens selecionados. A doença só aparece se
pelo menos um **padrão de imagem** contar a favor dela.

- **Alta:** ≥ 7 pontos e ≥ 80% da maior pontuação do caso
- **Média:** ≥ 4 pontos
- **Baixa:** 1 a 3 pontos

## Como ajustar a base

Para mudar um peso ou incluir uma doença, edite `base_conhecimento.py` e rode
os testes. Se um caso clássico deixar de ficar em 1º lugar, o teste avisa.

## Referências

- Hansell DM et al. Fleischner Society: glossary of terms for thoracic imaging. Radiology 2008.
- Bankier AA et al. Fleischner Society: glossary of terms for thoracic imaging (atualização). Radiology 2024.
- Webb WR, Müller NL, Naidich DP. High-Resolution CT of the Lung.
- Raghu G et al. IPF (update) and progressive pulmonary fibrosis. ATS/ERS/JRS/ALAT. AJRCCM 2022.
- Lynch DA et al. Diagnostic criteria for IPF: Fleischner Society White Paper. Lancet Respir Med 2018.
- Raghu G et al. Diagnosis of hypersensitivity pneumonitis in adults. ATS/JRS/ALAT. AJRCCM 2020.
- Travis WD et al. ATS/ERS classification of the idiopathic interstitial pneumonias. AJRCCM 2013.
- Simpson S et al. RSNA consensus on chest CT findings related to COVID-19. Radiol Cardiothorac Imaging 2020.
- Gupta N et al. Diffuse cystic lung disease (Parts I e II). AJRCCM 2015.
- Silva CIS et al. Consenso brasileiro ilustrado sobre a terminologia da TC de tórax. J Bras Pneumol 2010.
