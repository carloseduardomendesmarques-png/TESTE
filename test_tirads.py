"""
Testes automáticos da calculadora.
Para rodar: python -m unittest
"""

import unittest

from tirads import calcular_pontos, classificar, recomendar


class TestPontuacao(unittest.TestCase):

    def test_nodulo_cistico_simples(self):
        # cístico (0) + anecoico (0) + largo (0) + liso (0) + nenhum foco (0)
        self.assertEqual(calcular_pontos(1, 1, 1, 1, [1]), 0)

    def test_espongiforme_ignora_outras_categorias(self):
        self.assertEqual(calcular_pontos(2, 4, 2, 4, [4]), 0)

    def test_nodulo_muito_suspeito(self):
        # sólido (2) + muito hipoecoico (3) + alto (3) + irregular (2) + puntiformes (3)
        self.assertEqual(calcular_pontos(4, 4, 2, 3, [4]), 13)

    def test_focos_ecogenicos_somam(self):
        # sólido (2) + iso (1) + largo (0) + liso (0) + macro (1) + periférica (2)
        self.assertEqual(calcular_pontos(4, 2, 1, 1, [2, 3]), 6)


class TestClassificacao(unittest.TestCase):

    def test_limites_de_cada_tr(self):
        esperado = {0: 1, 1: 1, 2: 2, 3: 3, 4: 4, 6: 4, 7: 5, 13: 5}
        for pontos, tr in esperado.items():
            with self.subTest(pontos=pontos):
                self.assertEqual(classificar(pontos), tr)


class TestRecomendacao(unittest.TestCase):

    def test_tr1_e_tr2_sem_paaf(self):
        self.assertIn("Sem indicação de PAAF", recomendar(1, 5.0))
        self.assertIn("Sem indicação de PAAF", recomendar(2, 5.0))

    def test_tr3(self):
        self.assertIn("PAAF indicada", recomendar(3, 2.5))
        self.assertIn("Seguimento", recomendar(3, 1.5))
        self.assertIn("Sem indicação", recomendar(3, 1.4))

    def test_tr4(self):
        self.assertIn("PAAF indicada", recomendar(4, 1.5))
        self.assertIn("Seguimento", recomendar(4, 1.0))
        self.assertIn("Sem indicação", recomendar(4, 0.9))

    def test_tr5(self):
        self.assertIn("PAAF indicada", recomendar(5, 1.0))
        self.assertIn("Seguimento", recomendar(5, 0.5))
        self.assertIn("Sem indicação", recomendar(5, 0.4))


if __name__ == "__main__":
    unittest.main()
