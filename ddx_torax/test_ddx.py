"""
Testes do diagnóstico diferencial.
Para rodar (a partir da raiz do repositório):  python -m unittest discover ddx_torax

Os casos clássicos abaixo servem de "gabarito": se uma mudança nos pesos
fizer um caso clássico sair do 1º lugar, o teste avisa.
"""

import unittest

from base_conhecimento import DOENCAS, TODOS_ITENS
from motor import avaliar, avisos

PESOS_VALIDOS = {-3, -2, -1, 1, 2, 3}


class TestBaseConhecimento(unittest.TestCase):

    def test_todos_os_itens_existem(self):
        for doenca in DOENCAS:
            for item in doenca["pesos"]:
                with self.subTest(doenca=doenca["nome"], item=item):
                    self.assertIn(item, TODOS_ITENS)

    def test_pesos_validos(self):
        for doenca in DOENCAS:
            for item, peso in doenca["pesos"].items():
                with self.subTest(doenca=doenca["nome"], item=item):
                    self.assertIn(peso, PESOS_VALIDOS)

    def test_nomes_unicos(self):
        nomes = [d["nome"] for d in DOENCAS]
        self.assertEqual(len(nomes), len(set(nomes)))


class TestRegras(unittest.TestCase):

    def test_sem_selecao_nao_retorna_nada(self):
        self.assertEqual(avaliar(set()), [])

    def test_so_clinica_nao_basta(self):
        # Sem nenhum padrão de imagem, nenhuma doença deve aparecer
        self.assertEqual(avaliar({"tabagismo", "cronico", "idade_60"}), [])

    def test_aviso_para_quadro_inespecifico(self):
        selecionados = {"vidro_fosco", "consolidacao", "agudo", "febre"}
        mensagens = avisos(selecionados, avaliar(selecionados))
        self.assertTrue(any("distribuição" in m for m in mensagens))
        self.assertTrue(any("pouco específico" in m for m in mensagens))

    def test_sem_avisos_para_caso_completo(self):
        selecionados = CASOS_CLASSICOS[0][1]
        self.assertEqual(avisos(selecionados, avaliar(selecionados)), [])


# (descrição, itens selecionados, doença esperada em 1º lugar)
CASOS_CLASSICOS = [
    ("PIU / FPI",
     {"faveolamento", "reticulacao", "bronquiectasia_tracao", "dist_inferior",
      "dist_periferica", "cronico", "idade_60", "tabagismo"},
     "Fibrose pulmonar idiopática (padrão PIU)"),
    ("PINE em colagenose",
     {"vidro_fosco", "reticulacao", "bronquiectasia_tracao", "dist_inferior",
      "dist_poupa_subpleural", "esofago_dilatado", "cronico", "autoimune"},
     "Pneumonia intersticial não específica (PINE)"),
    ("Pneumocistose em HIV",
     {"vidro_fosco", "cistos", "dist_central", "subagudo", "imuno_hiv"},
     "Pneumocistose (Pneumocystis jirovecii)"),
    ("Sarcoidose",
     {"micronodulos_perilinfaticos", "linfonodomegalia", "dist_superior",
      "dist_peribroncovascular", "cronico"},
     "Sarcoidose"),
    ("COVID-19",
     {"vidro_fosco", "halo_invertido", "dist_periferica", "dist_inferior", "agudo", "febre"},
     "COVID-19"),
    ("Tuberculose pós-primária",
     {"cavitacao", "arvore_brotamento", "consolidacao", "dist_superior", "subagudo", "contato_tb"},
     "Tuberculose pós-primária (ativa)"),
    ("Edema cardiogênico",
     {"espessamento_septal_liso", "vidro_fosco", "derrame_pleural", "cardiomegalia",
      "agudo", "cardiopatia"},
     "Edema pulmonar cardiogênico"),
    ("Histiocitose de Langerhans",
     {"cistos", "micronodulos_centrolobulares", "dist_superior", "cronico", "tabagismo"},
     "Histiocitose de células de Langerhans"),
    ("LAM",
     {"cistos", "dist_difusa", "pneumotorax", "cronico", "mulher_jovem"},
     "Linfangioleiomiomatose (LAM)"),
    ("PH não fibrótica",
     {"micronodulos_centrolobulares", "vidro_fosco", "atenuacao_mosaico",
      "aprisionamento_aereo", "subagudo", "exposicao_antigenica"},
     "Pneumonite de hipersensibilidade não fibrótica"),
    ("PH fibrótica",
     {"reticulacao", "bronquiectasia_tracao", "sinal_tres_densidades",
      "atenuacao_mosaico", "dist_superior", "cronico", "exposicao_antigenica"},
     "Pneumonite de hipersensibilidade fibrótica"),
    ("Aspergilose angioinvasiva",
     {"nodulos_multiplos", "sinal_halo", "agudo", "imuno_neutropenia", "febre"},
     "Aspergilose angioinvasiva"),
    ("Pneumonia em organização",
     {"consolidacao", "opacidades_perilobulares", "halo_invertido", "dist_periferica",
      "dist_peribroncovascular", "subagudo"},
     "Pneumonia em organização"),
    ("Silicose",
     {"conglomerados", "micronodulos_perilinfaticos", "linfonodos_calcificados",
      "dist_superior", "cronico", "exposicao_silica"},
     "Silicose / pneumoconiose"),
    ("Metástases",
     {"nodulos_multiplos", "dist_inferior", "cronico", "neoplasia"},
     "Metástases hematogênicas"),
    ("Bronquiectasias",
     {"bronquiectasias", "espessamento_bronquico", "impactacao_mucoide", "cronico",
      "infeccoes_repeticao"},
     "Bronquiectasias (pós-infecciosas, FC, discinesia ciliar)"),
    ("Hemorragia alveolar",
     {"vidro_fosco", "consolidacao", "agudo", "hemoptise", "vasculite_sinais"},
     "Hemorragia alveolar difusa"),
    ("Proteinose alveolar",
     {"pavimentacao", "vidro_fosco", "cronico"},
     "Proteinose alveolar pulmonar"),
    ("Êmbolos sépticos",
     {"nodulos_multiplos", "cavitacao", "dist_periferica", "agudo", "fonte_embolica", "febre"},
     "Êmbolos sépticos"),
    ("Pneumonia eosinofílica crônica",
     {"consolidacao", "dist_periferica", "dist_superior", "subagudo", "eosinofilia_asma"},
     "Pneumonia eosinofílica crônica"),
    ("Micobacteriose não tuberculosa",
     {"bronquiectasias", "arvore_brotamento", "dist_lobo_medio_lingula", "cronico", "idade_60"},
     "Micobacteriose não tuberculosa (nodular-bronquiectásica)"),
    ("Paracoccidioidomicose",
     {"halo_invertido", "cavitacao", "dist_central", "cronico", "trabalhador_rural"},
     "Paracoccidioidomicose"),
]


class TestCasosClassicos(unittest.TestCase):

    def test_primeiro_lugar_com_alta_probabilidade(self):
        for descricao, selecionados, esperado in CASOS_CLASSICOS:
            with self.subTest(caso=descricao):
                resultado = avaliar(selecionados)
                self.assertTrue(resultado, "nenhum diagnóstico retornado")
                primeiro = resultado[0]
                self.assertEqual(primeiro["doenca"]["nome"], esperado)
                self.assertEqual(primeiro["nivel"], "Alta")

    def test_asbestose_sem_exposicao_nao_e_alta(self):
        # Fibrose basal sem exposição nem placas: asbestose não deve ser "Alta"
        selecionados = CASOS_CLASSICOS[0][1]
        niveis = {r["doenca"]["nome"]: r["nivel"] for r in avaliar(selecionados)}
        self.assertNotEqual(niveis.get("Asbestose"), "Alta")


if __name__ == "__main__":
    unittest.main()
