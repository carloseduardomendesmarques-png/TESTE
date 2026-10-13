"""
Base de conhecimento: achados de TC de tórax, dados clínicos e doenças.

Como funciona
-------------
Cada doença tem um dicionário `pesos` que liga um item (achado, distribuição,
achado associado, tempo de evolução ou dado clínico) a um peso:

     3  muito característico / quase obrigatório
     2  sugestivo
     1  compatível, mas inespecífico
    -1  pouco comum
    -2  fala contra
    -3  praticamente afasta

Itens que não aparecem no dicionário valem 0 (neutros).

IMPORTANTE: os pesos são estimativas didáticas montadas a partir das
referências listadas em REFERENCIAS. Eles não são probabilidades medidas
e devem ser revisados por um radiologista. Uso educacional.
"""

# ---------------------------------------------------------------------------
# 1) Vocabulário: itens que o médico pode selecionar
#    (termos baseados no Glossário Fleischner)
# ---------------------------------------------------------------------------

PADROES = {
    "vidro_fosco": "Opacidades em vidro fosco",
    "consolidacao": "Consolidação",
    "pavimentacao": "Pavimentação em mosaico (crazy-paving)",
    "reticulacao": "Reticulação",
    "faveolamento": "Faveolamento",
    "bronquiectasia_tracao": "Bronquiectasias / bronquiolectasias de tração",
    "espessamento_septal_liso": "Espessamento septal interlobular liso",
    "espessamento_septal_nodular": "Espessamento septal nodular / irregular",
    "micronodulos_centrolobulares": "Micronódulos centrolobulares (mal definidos / em vidro fosco)",
    "arvore_brotamento": "Árvore em brotamento",
    "micronodulos_perilinfaticos": "Micronódulos perilinfáticos (fissuras, subpleurais, peribroncovasculares)",
    "micronodulos_randomicos": "Micronódulos randômicos / miliares",
    "nodulos_multiplos": "Nódulos múltiplos (≥ 1 cm)",
    "nodulo_massa_solitaria": "Nódulo ou massa solitária",
    "cavitacao": "Cavitação",
    "sinal_halo": "Sinal do halo",
    "halo_invertido": "Sinal do halo invertido (atol)",
    "opacidades_perilobulares": "Opacidades perilobulares",
    "cistos": "Cistos pulmonares",
    "enfisema": "Enfisema",
    "atenuacao_mosaico": "Atenuação em mosaico",
    "aprisionamento_aereo": "Aprisionamento aéreo (expiração)",
    "sinal_tres_densidades": "Sinal das três densidades (headcheese)",
    "bronquiectasias": "Bronquiectasias (não de tração)",
    "espessamento_bronquico": "Espessamento de paredes brônquicas",
    "impactacao_mucoide": "Impactação mucoide",
    "nodulos_calcificados": "Nódulos calcificados",
    "conglomerados": "Massas conglomeradas (fibrose maciça progressiva)",
}

DISTRIBUICAO = {
    "dist_superior": "Predomínio em lobos superiores",
    "dist_inferior": "Predomínio em lobos inferiores",
    "dist_periferica": "Predomínio periférico / subpleural",
    "dist_poupa_subpleural": "Poupa a região subpleural imediata",
    "dist_peribroncovascular": "Predomínio peribroncovascular",
    "dist_central": "Central / peri-hilar (asa de borboleta)",
    "dist_lobo_medio_lingula": "Predomínio em lobo médio e língula",
    "dist_difusa": "Difusa / sem predomínio",
    "dist_unilateral": "Unilateral / focal / lobar",
}

ASSOCIADOS = {
    "derrame_pleural": "Derrame pleural",
    "placas_pleurais": "Placas pleurais (calcificadas ou não)",
    "linfonodomegalia": "Linfonodomegalia mediastinal / hilar",
    "linfonodos_calcificados": "Linfonodos calcificados (incl. em casca de ovo)",
    "pneumotorax": "Pneumotórax",
    "cardiomegalia": "Cardiomegalia / sinais de congestão",
    "esofago_dilatado": "Esôfago dilatado",
}

TEMPOS = {
    "agudo": "Agudo (< 4 semanas)",
    "subagudo": "Subagudo (4 a 12 semanas)",
    "cronico": "Crônico (> 12 semanas)",
}

CLINICA = {
    "febre": "Febre",
    "hipoxemia_grave": "Insuficiência respiratória aguda grave",
    "imuno_hiv": "HIV com CD4 < 200",
    "imuno_neutropenia": "Neutropenia / transplante de medula / quimioterapia",
    "imuno_outro": "Outra imunossupressão (corticoide, transplante de órgão sólido, biológicos)",
    "tabagismo": "Tabagismo (atual ou prévio)",
    "exposicao_antigenica": "Exposição a aves, mofo ou antígenos orgânicos",
    "exposicao_silica": "Exposição a sílica / poeiras minerais",
    "exposicao_asbesto": "Exposição a asbesto",
    "trabalhador_rural": "Trabalhador rural / contato com solo (micoses endêmicas)",
    "contato_tb": "Contato com tuberculose / população de risco",
    "autoimune": "Doença autoimune / colagenose (AR, ES, miosite, Sjögren...)",
    "vasculite_sinais": "Sinusite, hematúria ou insuficiência renal (suspeita de vasculite)",
    "drogas": "Medicamento pneumotóxico (amiodarona, metotrexato, quimio/imunoterapia)",
    "cardiopatia": "Insuficiência cardíaca / sobrecarga de volume",
    "neoplasia": "Neoplasia maligna conhecida",
    "hemoptise": "Hemoptise / queda de hemoglobina",
    "eosinofilia_asma": "Asma e/ou eosinofilia",
    "infeccoes_repeticao": "Tosse produtiva crônica / infecções de repetição",
    "fonte_embolica": "Fonte embólica (cateter, endocardite, drogas IV, infecção de partes moles)",
    "broncoaspiracao": "Risco de aspiração (disfagia, etilismo, rebaixamento de consciência)",
    "idade_60": "Idade > 60 anos",
    "mulher_jovem": "Mulher em idade fértil",
}

# Ordem e títulos das seções na tela
CATEGORIAS = {
    "Padrões / achados principais": PADROES,
    "Distribuição": DISTRIBUICAO,
    "Achados associados": ASSOCIADOS,
    "Dados clínicos": CLINICA,
}

# Todos os itens juntos (útil para validar e para mostrar nomes)
TODOS_ITENS = {**PADROES, **DISTRIBUICAO, **ASSOCIADOS, **TEMPOS, **CLINICA}


# ---------------------------------------------------------------------------
# 2) Doenças
# ---------------------------------------------------------------------------

DOENCAS = [
    # ===================== INFECCIOSAS =====================
    {
        "nome": "Pneumonia bacteriana",
        "grupo": "Infecciosa",
        "pesos": {
            "consolidacao": 3, "arvore_brotamento": 1, "micronodulos_centrolobulares": 1,
            "vidro_fosco": 1, "cavitacao": 1, "derrame_pleural": 1, "dist_unilateral": 2,
            "reticulacao": -2, "faveolamento": -3, "cistos": -2,
            "agudo": 3, "subagudo": -1, "cronico": -3,
            "febre": 2,
        },
        "dica": "Consolidação lobar/segmentar com broncograma aéreo em quadro agudo febril.",
    },
    {
        "nome": "Pneumonia aspirativa",
        "grupo": "Infecciosa",
        "pesos": {
            "consolidacao": 2, "arvore_brotamento": 2, "micronodulos_centrolobulares": 1,
            "vidro_fosco": 1, "cavitacao": 1, "dist_inferior": 1, "dist_unilateral": 1,
            "esofago_dilatado": 2,
            "agudo": 2, "subagudo": 1,
            "broncoaspiracao": 3, "febre": 1,
        },
        "dica": "Segmentos pendentes (posteriores dos lobos superiores e superiores/basais dos inferiores).",
    },
    {
        "nome": "Pneumonia viral",
        "grupo": "Infecciosa",
        "pesos": {
            "vidro_fosco": 2, "consolidacao": 1, "micronodulos_centrolobulares": 2,
            "arvore_brotamento": 1, "espessamento_bronquico": 1, "pavimentacao": 1,
            "dist_difusa": 1,
            "faveolamento": -3, "cavitacao": -2, "linfonodomegalia": -1,
            "agudo": 3, "cronico": -3,
            "febre": 2,
        },
        "dica": "Vidro fosco multifocal e micronódulos centrolobulares; padrão varia com o agente.",
    },
    {
        "nome": "COVID-19",
        "grupo": "Infecciosa",
        "pesos": {
            "vidro_fosco": 3, "consolidacao": 1, "pavimentacao": 1, "halo_invertido": 2,
            "opacidades_perilobulares": 1, "dist_periferica": 2, "dist_inferior": 1,
            "arvore_brotamento": -2, "micronodulos_centrolobulares": -1, "cavitacao": -2,
            "derrame_pleural": -1, "linfonodomegalia": -1, "faveolamento": -3,
            "agudo": 3, "subagudo": 1, "cronico": -2,
            "febre": 2,
        },
        "dica": "Padrão típico (RSNA): vidro fosco periférico bilateral, ± consolidação, pavimentação ou halo invertido.",
    },
    {
        "nome": "Pneumocistose (Pneumocystis jirovecii)",
        "grupo": "Infecciosa",
        "pesos": {
            "vidro_fosco": 3, "pavimentacao": 2, "cistos": 2, "dist_central": 1,
            "dist_superior": 1, "dist_poupa_subpleural": 1,
            "derrame_pleural": -2, "linfonodomegalia": -1, "arvore_brotamento": -1,
            "agudo": 1, "subagudo": 2, "cronico": -2,
            "imuno_hiv": 3, "imuno_outro": 2, "imuno_neutropenia": 1, "febre": 1,
        },
        "dica": "Vidro fosco difuso/peri-hilar poupando a periferia; cistos (pneumatoceles) em até 1/3.",
    },
    {
        "nome": "Tuberculose pós-primária (ativa)",
        "grupo": "Infecciosa",
        "pesos": {
            "arvore_brotamento": 3, "cavitacao": 3, "consolidacao": 2,
            "micronodulos_centrolobulares": 2, "nodulos_multiplos": 1, "dist_superior": 2,
            "linfonodomegalia": 1, "derrame_pleural": 1,
            "faveolamento": -3,
            "subagudo": 2, "cronico": 2,
            "contato_tb": 2, "imuno_hiv": 1, "imuno_outro": 1, "febre": 1, "hemoptise": 1,
        },
        "dica": "Cavitação em segmentos apicais/posteriores com disseminação broncogênica (árvore em brotamento).",
    },
    {
        "nome": "Tuberculose miliar",
        "grupo": "Infecciosa",
        "pesos": {
            "micronodulos_randomicos": 3, "dist_difusa": 1, "linfonodomegalia": 1,
            "agudo": 1, "subagudo": 2,
            "imuno_hiv": 2, "imuno_outro": 1, "contato_tb": 2, "febre": 2,
        },
        "dica": "Micronódulos de 1–3 mm difusos e randômicos. Diferencial: metástases miliares e micoses.",
    },
    {
        "nome": "Micobacteriose não tuberculosa (nodular-bronquiectásica)",
        "grupo": "Infecciosa",
        "pesos": {
            "bronquiectasias": 3, "arvore_brotamento": 3, "micronodulos_centrolobulares": 2,
            "cavitacao": 1, "nodulos_multiplos": 1, "espessamento_bronquico": 1,
            "dist_lobo_medio_lingula": 3,
            "agudo": -2, "cronico": 3,
            "infeccoes_repeticao": 1, "idade_60": 1,
        },
        "dica": "Bronquiectasias e árvore em brotamento em lobo médio/língula, típico em mulheres idosas.",
    },
    {
        "nome": "Aspergilose angioinvasiva",
        "grupo": "Infecciosa",
        "pesos": {
            "nodulos_multiplos": 2, "sinal_halo": 3, "consolidacao": 1, "cavitacao": 1,
            "halo_invertido": 1,
            "agudo": 3, "cronico": -2,
            "imuno_neutropenia": 3, "imuno_outro": 1, "febre": 1,
        },
        "dica": "Nódulos com halo em neutropênico febril; crescente aéreo surge na recuperação. Halo invertido: pensar em mucormicose.",
    },
    {
        "nome": "Aspergilose broncopulmonar alérgica (ABPA)",
        "grupo": "Infecciosa",
        "pesos": {
            "impactacao_mucoide": 3, "bronquiectasias": 3, "micronodulos_centrolobulares": 1,
            "arvore_brotamento": 1, "atenuacao_mosaico": 1, "dist_superior": 1, "dist_central": 1,
            "agudo": -1, "cronico": 2,
            "eosinofilia_asma": 3,
        },
        "dica": "Bronquiectasias centrais em lobos superiores com muco (às vezes hiperatenuante) em asmático.",
    },
    {
        "nome": "Êmbolos sépticos",
        "grupo": "Infecciosa",
        "pesos": {
            "nodulos_multiplos": 3, "cavitacao": 3, "sinal_halo": 1, "dist_periferica": 2,
            "dist_inferior": 1, "derrame_pleural": 1,
            "agudo": 3, "cronico": -2,
            "fonte_embolica": 3, "febre": 2,
        },
        "dica": "Nódulos periféricos em diferentes fases de cavitação, com vaso nutridor.",
    },
    {
        "nome": "Paracoccidioidomicose",
        "grupo": "Infecciosa",
        "pesos": {
            "halo_invertido": 2, "cavitacao": 2, "nodulos_multiplos": 1, "reticulacao": 1,
            "espessamento_septal_liso": 1, "micronodulos_centrolobulares": 1, "enfisema": 1,
            "dist_central": 2,
            "agudo": -2, "subagudo": 1, "cronico": 2,
            "trabalhador_rural": 3, "tabagismo": 1,
        },
        "dica": "Forma crônica do adulto: opacidades bilaterais simétricas peri-hilares, cavidades, halo invertido e fibrose.",
    },

    # ===================== INTERSTICIAIS =====================
    {
        "nome": "Fibrose pulmonar idiopática (padrão PIU)",
        "grupo": "Intersticial",
        "pesos": {
            "faveolamento": 3, "reticulacao": 2, "bronquiectasia_tracao": 2,
            "dist_inferior": 2, "dist_periferica": 2,
            "vidro_fosco": -1, "micronodulos_centrolobulares": -2, "consolidacao": -2,
            "cistos": -1, "atenuacao_mosaico": -2, "sinal_tres_densidades": -3,
            "micronodulos_perilinfaticos": -2, "dist_superior": -2,
            "dist_peribroncovascular": -2, "dist_poupa_subpleural": -3,
            "agudo": -3, "cronico": 3,
            "idade_60": 2, "tabagismo": 1, "exposicao_antigenica": -1, "autoimune": -1,
        },
        "dica": "PIU: faveolamento subpleural basal ± bronquiectasias de tração. Excluir colagenose, exposições e drogas.",
    },
    {
        "nome": "Pneumonia intersticial não específica (PINE)",
        "grupo": "Intersticial",
        "pesos": {
            "vidro_fosco": 3, "reticulacao": 2, "bronquiectasia_tracao": 2,
            "dist_poupa_subpleural": 3, "dist_inferior": 2, "dist_peribroncovascular": 1,
            "esofago_dilatado": 2,
            "faveolamento": -2, "micronodulos_centrolobulares": -1, "cistos": -1,
            "agudo": -2, "subagudo": 1, "cronico": 2,
            "autoimune": 3, "drogas": 1,
        },
        "dica": "Vidro fosco e reticulação basais com preservação subpleural; procurar colagenose (esôfago dilatado: ES).",
    },
    {
        "nome": "Pneumonite de hipersensibilidade fibrótica",
        "grupo": "Intersticial",
        "pesos": {
            "reticulacao": 2, "bronquiectasia_tracao": 2, "faveolamento": 1,
            "sinal_tres_densidades": 3, "atenuacao_mosaico": 2, "aprisionamento_aereo": 2,
            "micronodulos_centrolobulares": 2, "vidro_fosco": 1,
            "dist_superior": 1, "dist_peribroncovascular": 1, "dist_difusa": 1,
            "agudo": -2, "cronico": 3,
            "exposicao_antigenica": 3,
        },
        "dica": "Fibrose sem predomínio basal claro + sinal das três densidades ou aprisionamento aéreo lobular.",
    },
    {
        "nome": "Pneumonite de hipersensibilidade não fibrótica",
        "grupo": "Intersticial",
        "pesos": {
            "micronodulos_centrolobulares": 3, "vidro_fosco": 2, "atenuacao_mosaico": 2,
            "aprisionamento_aereo": 2, "sinal_tres_densidades": 3,
            "dist_difusa": 1, "dist_superior": 1,
            "faveolamento": -3, "reticulacao": -1, "bronquiectasia_tracao": -2,
            "arvore_brotamento": -2,
            "agudo": 1, "subagudo": 2, "cronico": 1,
            "exposicao_antigenica": 3,
        },
        "dica": "Micronódulos centrolobulares em vidro fosco difusos + mosaico/aprisionamento aéreo.",
    },
    {
        "nome": "Pneumonia em organização",
        "grupo": "Intersticial",
        "pesos": {
            "consolidacao": 3, "vidro_fosco": 1, "halo_invertido": 3,
            "opacidades_perilobulares": 3, "nodulos_multiplos": 1,
            "dist_periferica": 2, "dist_peribroncovascular": 2, "dist_inferior": 1,
            "faveolamento": -3, "cavitacao": -1,
            "agudo": 1, "subagudo": 3,
            "autoimune": 1, "drogas": 1, "febre": 1,
        },
        "dica": "Consolidações periféricas/peribroncovasculares, migratórias, com halo invertido e padrão perilobular.",
    },
    {
        "nome": "Pneumonia eosinofílica crônica",
        "grupo": "Intersticial",
        "pesos": {
            "consolidacao": 3, "vidro_fosco": 2, "opacidades_perilobulares": 1,
            "dist_superior": 2, "dist_periferica": 3,
            "cavitacao": -2, "faveolamento": -3,
            "agudo": -1, "subagudo": 2, "cronico": 2,
            "eosinofilia_asma": 3,
        },
        "dica": "Consolidações periféricas em lobos superiores (\"negativo do edema\"), asma e eosinofilia.",
    },
    {
        "nome": "Pneumonia eosinofílica aguda",
        "grupo": "Intersticial",
        "pesos": {
            "vidro_fosco": 3, "espessamento_septal_liso": 3, "consolidacao": 1,
            "pavimentacao": 1, "derrame_pleural": 2, "dist_difusa": 1,
            "cardiomegalia": -2,
            "agudo": 3, "cronico": -3,
            "tabagismo": 2, "hipoxemia_grave": 2, "febre": 1, "eosinofilia_asma": 1,
        },
        "dica": "Simula edema, mas sem cardiomegalia; associação com início recente de tabagismo/vape.",
    },
    {
        "nome": "Doença intersticial relacionada ao tabagismo (BR-DPI / PID descamativa)",
        "grupo": "Intersticial",
        "pesos": {
            "micronodulos_centrolobulares": 2, "vidro_fosco": 2, "espessamento_bronquico": 1,
            "enfisema": 2, "cistos": 1,
            "faveolamento": -2,
            "agudo": -2, "cronico": 2,
            "tabagismo": 3,
        },
        "dica": "BR-DPI: micronódulos centrolobulares em lobos superiores. PID descamativa: vidro fosco basal com pequenos cistos.",
    },
    {
        "nome": "Sarcoidose",
        "grupo": "Intersticial",
        "pesos": {
            "micronodulos_perilinfaticos": 3, "nodulos_multiplos": 1, "conglomerados": 1,
            "reticulacao": 1, "bronquiectasia_tracao": 1,
            "dist_superior": 2, "dist_peribroncovascular": 2,
            "linfonodomegalia": 3, "linfonodos_calcificados": 1,
            "cavitacao": -1, "arvore_brotamento": -1, "derrame_pleural": -2,
            "subagudo": 1, "cronico": 2,
            "idade_60": -1, "tabagismo": -1,
        },
        "dica": "Micronódulos perilinfáticos peribroncovasculares em lobos superiores + linfonodomegalia hilar simétrica.",
    },
    {
        "nome": "Silicose / pneumoconiose",
        "grupo": "Intersticial",
        "pesos": {
            "micronodulos_perilinfaticos": 2, "micronodulos_centrolobulares": 2,
            "conglomerados": 3, "nodulos_calcificados": 2, "enfisema": 1,
            "dist_superior": 2,
            "linfonodos_calcificados": 3, "linfonodomegalia": 1,
            "agudo": -3, "cronico": 3,
            "exposicao_silica": 3,
        },
        "dica": "Micronódulos posteriores em lobos superiores, conglomerados e linfonodos com calcificação em casca de ovo.",
    },
    {
        "nome": "Asbestose",
        "grupo": "Intersticial",
        "pesos": {
            "reticulacao": 2, "faveolamento": 1, "bronquiectasia_tracao": 1,
            "dist_inferior": 2, "dist_periferica": 2,
            "placas_pleurais": 3,
            "agudo": -3, "cronico": 3,
            "exposicao_asbesto": 3, "idade_60": 1,
        },
        "dica": "Fibrose basal subpleural (pode lembrar PIU) com placas pleurais e exposição a asbesto.",
    },
    {
        "nome": "Histiocitose de células de Langerhans",
        "grupo": "Intersticial",
        "pesos": {
            "cistos": 3, "micronodulos_centrolobulares": 2, "nodulos_multiplos": 1,
            "cavitacao": 1, "dist_superior": 3, "pneumotorax": 1,
            "cronico": 2,
            "tabagismo": 3, "idade_60": -1,
        },
        "dica": "Cistos bizarros e nódulos (às vezes cavitados) em lobos superiores, poupando seios costofrênicos. Tabagistas jovens.",
    },
    {
        "nome": "Linfangioleiomiomatose (LAM)",
        "grupo": "Intersticial",
        "pesos": {
            "cistos": 3, "dist_difusa": 2, "pneumotorax": 2, "derrame_pleural": 1,
            "nodulos_multiplos": -1, "micronodulos_centrolobulares": -1, "dist_superior": -1,
            "cronico": 3,
            "mulher_jovem": 3,
        },
        "dica": "Cistos redondos de paredes finas, difusos, em mulher; pneumotórax e derrame quiloso. Pensar em esclerose tuberosa.",
    },
    {
        "nome": "Pneumonia intersticial linfocítica (PIL)",
        "grupo": "Intersticial",
        "pesos": {
            "cistos": 3, "vidro_fosco": 2, "micronodulos_centrolobulares": 1,
            "espessamento_septal_liso": 1, "dist_inferior": 1, "linfonodomegalia": 1,
            "cronico": 2,
            "autoimune": 2, "imuno_hiv": 1,
        },
        "dica": "Poucos cistos perivasculares em bases + vidro fosco. Associada a Sjögren.",
    },
    {
        "nome": "Proteinose alveolar pulmonar",
        "grupo": "Intersticial",
        "pesos": {
            "pavimentacao": 3, "vidro_fosco": 2, "espessamento_septal_liso": 1, "dist_difusa": 1,
            "derrame_pleural": -2, "cardiomegalia": -2, "linfonodomegalia": -1,
            "agudo": -1, "subagudo": 2, "cronico": 2,
            "febre": -1, "exposicao_silica": 1,
        },
        "dica": "Pavimentação em mosaico geográfica, com sintomas desproporcionalmente leves.",
    },
    {
        "nome": "Pneumonite induzida por drogas",
        "grupo": "Intersticial",
        "pesos": {
            "vidro_fosco": 2, "consolidacao": 1, "reticulacao": 1, "halo_invertido": 1,
            "opacidades_perilobulares": 1, "micronodulos_centrolobulares": 1, "dist_difusa": 1,
            "agudo": 1, "subagudo": 2, "cronico": 1,
            "drogas": 3,
        },
        "dica": "Pode reproduzir PINE, POC, PH ou DAD. Amiodarona: consolidações hiperatenuantes e fígado denso.",
    },
    {
        "nome": "Dano alveolar difuso / SDRA",
        "grupo": "Intersticial",
        "pesos": {
            "consolidacao": 3, "vidro_fosco": 2, "pavimentacao": 1, "bronquiectasia_tracao": 1,
            "dist_difusa": 2, "derrame_pleural": 1,
            "agudo": 3, "cronico": -3,
            "hipoxemia_grave": 3, "febre": 1, "drogas": 1,
        },
        "dica": "Consolidações pendentes e vidro fosco difuso; bronquiectasias de tração na fase organizante.",
    },

    # ===================== VASCULARES / CARDIOGÊNICAS =====================
    {
        "nome": "Edema pulmonar cardiogênico",
        "grupo": "Vascular / cardiogênica",
        "pesos": {
            "espessamento_septal_liso": 3, "vidro_fosco": 2, "consolidacao": 1,
            "pavimentacao": 1, "espessamento_bronquico": 1,
            "dist_central": 2, "dist_inferior": 1,
            "derrame_pleural": 2, "cardiomegalia": 3, "linfonodomegalia": 1,
            "cavitacao": -3,
            "agudo": 3, "cronico": -1,
            "cardiopatia": 3,
        },
        "dica": "Septos lisos, vidro fosco peri-hilar/pendente, derrames bilaterais e cardiomegalia.",
    },
    {
        "nome": "Hemorragia alveolar difusa",
        "grupo": "Vascular / cardiogênica",
        "pesos": {
            "vidro_fosco": 3, "consolidacao": 2, "micronodulos_centrolobulares": 2,
            "pavimentacao": 1, "dist_poupa_subpleural": 1, "dist_difusa": 1,
            "derrame_pleural": -1, "cardiomegalia": -1,
            "agudo": 3, "cronico": -2,
            "hemoptise": 3, "vasculite_sinais": 2, "autoimune": 1,
        },
        "dica": "Vidro fosco difuso que evolui para pavimentação em dias. Hemoptise pode estar ausente.",
    },
    {
        "nome": "Granulomatose com poliangiite",
        "grupo": "Vascular / cardiogênica",
        "pesos": {
            "nodulos_multiplos": 3, "cavitacao": 3, "sinal_halo": 2, "consolidacao": 1,
            "vidro_fosco": 1, "halo_invertido": 1,
            "agudo": 1, "subagudo": 2, "cronico": 1,
            "vasculite_sinais": 3, "hemoptise": 1,
        },
        "dica": "Nódulos/massas cavitadas múltiplos, com halo (hemorragia). Investigar seios da face e rins.",
    },
    {
        "nome": "Infarto pulmonar (tromboembolismo)",
        "grupo": "Vascular / cardiogênica",
        "pesos": {
            "consolidacao": 2, "halo_invertido": 1, "dist_periferica": 2, "dist_inferior": 1,
            "derrame_pleural": 1,
            "agudo": 3, "cronico": -2,
            "hemoptise": 1,
        },
        "dica": "Consolidação periférica cuneiforme de base pleural. Confirmar com angio-TC.",
    },

    # ===================== NEOPLÁSICAS =====================
    {
        "nome": "Metástases hematogênicas",
        "grupo": "Neoplásica",
        "pesos": {
            "nodulos_multiplos": 3, "micronodulos_randomicos": 2, "cavitacao": 1,
            "sinal_halo": 1, "dist_inferior": 1, "dist_periferica": 1,
            "agudo": -1, "subagudo": 1, "cronico": 1,
            "neoplasia": 3, "febre": -1,
        },
        "dica": "Nódulos de tamanhos variados, periféricos e basais. Halo: melanoma, coriocarcinoma, angiossarcoma.",
    },
    {
        "nome": "Linfangite carcinomatosa",
        "grupo": "Neoplásica",
        "pesos": {
            "espessamento_septal_nodular": 3, "espessamento_septal_liso": 1,
            "micronodulos_perilinfaticos": 2, "dist_unilateral": 1, "dist_peribroncovascular": 1,
            "derrame_pleural": 2, "linfonodomegalia": 2,
            "faveolamento": -2,
            "subagudo": 2, "cronico": 1,
            "neoplasia": 3,
        },
        "dica": "Septos nodulares e espessamento peribroncovascular, sem distorção arquitetural; muitas vezes assimétrico.",
    },
    {
        "nome": "Neoplasia primária de pulmão (nódulo/massa)",
        "grupo": "Neoplásica",
        "pesos": {
            "nodulo_massa_solitaria": 3, "cavitacao": 1, "enfisema": 1,
            "linfonodomegalia": 1, "derrame_pleural": 1,
            "agudo": -1, "cronico": 2,
            "tabagismo": 2, "idade_60": 2, "hemoptise": 1, "exposicao_asbesto": 1,
        },
        "dica": "Nódulo espiculado ou massa em tabagista; cavitação de paredes espessas sugere carcinoma epidermoide.",
    },
    {
        "nome": "Adenocarcinoma de padrão pneumônico / lepídico",
        "grupo": "Neoplásica",
        "pesos": {
            "consolidacao": 2, "vidro_fosco": 2, "nodulo_massa_solitaria": 2,
            "nodulos_multiplos": 1, "pavimentacao": 1, "dist_unilateral": 1,
            "agudo": -2, "cronico": 3,
            "tabagismo": 1, "idade_60": 1, "febre": -1,
        },
        "dica": "Consolidação ou vidro fosco persistente que não resolve com tratamento: considerar adenocarcinoma mucinoso.",
    },
    {
        "nome": "Linfoma pulmonar",
        "grupo": "Neoplásica",
        "pesos": {
            "consolidacao": 2, "nodulos_multiplos": 2, "dist_peribroncovascular": 1,
            "linfonodomegalia": 2,
            "agudo": -1, "cronico": 2,
            "autoimune": 1, "imuno_hiv": 1,
        },
        "dica": "Consolidações ou nódulos peribroncovasculares com broncograma aéreo, de evolução lenta (MALT).",
    },

    # ===================== VIAS AÉREAS =====================
    {
        "nome": "DPOC / enfisema",
        "grupo": "Vias aéreas",
        "pesos": {
            "enfisema": 3, "espessamento_bronquico": 1, "dist_superior": 2,
            "cronico": 3,
            "tabagismo": 3, "idade_60": 1,
        },
        "dica": "Enfisema centrolobular em lobos superiores. Panlobular basal: pensar em deficiência de alfa-1 antitripsina.",
    },
    {
        "nome": "Bronquiolite infecciosa",
        "grupo": "Vias aéreas",
        "pesos": {
            "arvore_brotamento": 3, "micronodulos_centrolobulares": 2,
            "espessamento_bronquico": 2, "consolidacao": 1,
            "agudo": 3, "cronico": -2,
            "febre": 2,
        },
        "dica": "Árvore em brotamento e espessamento brônquico em quadro agudo (vírus, micoplasma, bactérias).",
    },
    {
        "nome": "Bronquiolite constritiva (obliterante)",
        "grupo": "Vias aéreas",
        "pesos": {
            "atenuacao_mosaico": 3, "aprisionamento_aereo": 3, "bronquiectasias": 2,
            "espessamento_bronquico": 1,
            "vidro_fosco": -1, "micronodulos_centrolobulares": -1,
            "cronico": 3,
            "imuno_neutropenia": 2, "autoimune": 1,
        },
        "dica": "Mosaico com vasos reduzidos nas áreas hipoatenuantes e aprisionamento na expiração (pós-TMO, AR, inalação).",
    },
    {
        "nome": "Bronquiectasias (pós-infecciosas, FC, discinesia ciliar)",
        "grupo": "Vias aéreas",
        "pesos": {
            "bronquiectasias": 3, "espessamento_bronquico": 2, "impactacao_mucoide": 2,
            "arvore_brotamento": 2, "atenuacao_mosaico": 1, "aprisionamento_aereo": 1,
            "cronico": 3,
            "infeccoes_repeticao": 3,
        },
        "dica": "Predomínio superior sugere fibrose cística; lobo médio/língula, discinesia ciliar ou micobactéria.",
    },
]


# ---------------------------------------------------------------------------
# 3) Referências usadas para montar a base
# ---------------------------------------------------------------------------

REFERENCIAS = [
    "Hansell DM et al. Fleischner Society: glossary of terms for thoracic imaging. Radiology 2008.",
    "Bankier AA et al. Fleischner Society: glossary of terms for thoracic imaging (atualização). Radiology 2024.",
    "Webb WR, Müller NL, Naidich DP. High-Resolution CT of the Lung. Wolters Kluwer.",
    "Raghu G et al. Idiopathic pulmonary fibrosis (an update) and progressive pulmonary fibrosis in adults. "
    "ATS/ERS/JRS/ALAT guideline. Am J Respir Crit Care Med 2022.",
    "Lynch DA et al. Diagnostic criteria for IPF: a Fleischner Society White Paper. Lancet Respir Med 2018.",
    "Raghu G et al. Diagnosis of hypersensitivity pneumonitis in adults. ATS/JRS/ALAT guideline. "
    "Am J Respir Crit Care Med 2020.",
    "Travis WD et al. ATS/ERS update of the international multidisciplinary classification of the "
    "idiopathic interstitial pneumonias. Am J Respir Crit Care Med 2013.",
    "Simpson S et al. RSNA expert consensus statement on reporting chest CT findings related to COVID-19. "
    "Radiology: Cardiothoracic Imaging 2020.",
    "Gupta N et al. Diffuse cystic lung disease (Parts I e II). Am J Respir Crit Care Med 2015.",
    "Silva CIS, Marchiori E, Souza Jr AS, Müller NL. Consenso brasileiro ilustrado sobre a terminologia "
    "dos descritores e padrões fundamentais da TC de tórax. J Bras Pneumol 2010.",
]
