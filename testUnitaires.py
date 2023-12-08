import unittest
import os
from class_PAP import ScrapingGeneral

class TestStringMethods(unittest.TestCase):
	

	def test_ScrapingGeneral(self):
		# Tests sur l'instance ScrapingGenerale
		
		sg = ScrapingGeneral()
		# Test : Est-ce que la création de l'instance à fonctionner et est-ce que l'attribut corpus a bien été initialisée à None
		self.assertTrue(sg.corpus is None)

		sg.scrap('python', arxiv=20, reddit=20)
		# Test : Scrap d'arxiv et reddit : on regarde si le nombre de document du corpus n'est plus nul
		self.assertTrue(sg.corpus.get_ndoc() > 0)

		# Si l'on a deja un corpus avec cette query de save, on la suprimme
		if f"{sg.corpus.get_nom()}_corpus.dataPAP" in os.listdir(sg.datafolder):
			os.remove(f"{sg.datafolder}{sg.corpus.get_nom()}_corpus.dataPAP")

		# Test du save du corpus :
		sg.save()
		self.assertIn(f"{sg.corpus.get_nom()}_corpus.dataPAP", os.listdir(sg.datafolder))

		sg2 = ScrapingGeneral()
		sg2.charged('python')
		# Test : On verifie que les données sont charger correctement
		self.assertTrue(sg2.corpus is not None)

		os.remove(f"{sg.datafolder}{sg.corpus.get_nom()}_corpus.dataPAP")





	






if __name__ == '__main__':
	unittest.main()