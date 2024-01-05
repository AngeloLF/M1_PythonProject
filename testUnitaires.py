import unittest
import os
from class_PAP import ScrapingGeneral
import Document
import Corpus
import Author
import datetime

class TestStringMethods(unittest.TestCase):

	def test_ScrapingGeneral(self):
		# Tests sur l'instance ScrapingGenerale
		
		sg = ScrapingGeneral()
		# Test : Est-ce que la création de l'instance à fonctionner et est-ce que l'attribut corpus a bien été initialisée à None
		self.assertTrue(sg.corpus is None)

		sg.scrap('python', arxiv=20, reddit=20)
<<<<<<< HEAD
		# Test : Scrap d'arxiv et reddit : on regarde si le nombre de document du corpus n'est plus nul
=======
		# Test : Scrap d'arxiv et reddit : on regarde si le nombre de documents du corpus n'est plus nul
>>>>>>> 9f062247c65f30307ad1d8b9a083eb5eb229a67e
		self.assertTrue(sg.corpus.get_ndoc() > 0)

		# Si l'on a deja un corpus avec cette query de save, on la suprimme
		if f"{sg.corpus.get_nom()}_corpus.dataPAP" in os.listdir(sg.datafolder):
			os.remove(f"{sg.datafolder}{sg.corpus.get_nom()}_corpus.dataPAP")

		# Test du save du corpus :
		sg.save()
		self.assertIn(f"{sg.corpus.get_nom()}_corpus.dataPAP", os.listdir(sg.datafolder))

		sg2 = ScrapingGeneral()
		sg2.charged('python')
<<<<<<< HEAD
		# Test : On verifie que les données sont charger correctement
=======
		# Test : On verifie que les données sont chargées correctement
>>>>>>> 9f062247c65f30307ad1d8b9a083eb5eb229a67e
		self.assertTrue(sg2.corpus is not None)

		os.remove(f"{sg.datafolder}{sg.corpus.get_nom()}_corpus.dataPAP")



	def test_Corpus_and_Document(self):
		# Tests de la classe RedditDocument et Corpus

		fauxAuteur = ['Angelo', 'Clement']

		fauxDocu = Document.RedditDocument(titre='Faux Titre', 
			auteur=fauxAuteur, 
			date=datetime.datetime.now(), 
			url='Non.com', 
			texte='Le faux texte c\'est ici', 
			nb_comment=999)
  
		fauxCorp = Corpus.Corpus('FauxCorpus')
		fauxCorp.addDocument(fauxAuteur, fauxDocu)

		self.assertEqual(list(fauxCorp.get_id2aut().keys()), fauxAuteur)
  
		# Tests des méthodes dans Document
  
		self.assertEqual(fauxDocu.get_titre(), 'Faux Titre')
		self.assertEqual(fauxDocu.get_auteur(), fauxAuteur)

		self.assertIn('RedditDocument', fauxDocu.__str__())
		fauxDocu.info()
		fauxDocu.set_date(datetime.datetime.now())

		# Test de la classe ArxivDocument
		fauxDocu2 = Document.ArxivDocument(titre='Faux Titre2', 
			auteur=fauxAuteur, 
			date=datetime.datetime.now(), 
			url='Non.com', 
			texte='Le faux texte c\'est ici', 
			category='physics')
  
		self.assertEqual(fauxDocu2.get_titre(), 'Faux Titre2')
		self.assertEqual(fauxDocu2.get_category(), 'physics')


	def test_Corpus_statAuthor(self):
		# Tests de la classe Documents et Authors

		fauxAuteur = ['Angelo', 'Clement']

		fauxDocu = Document.RedditDocument(titre='Faux Titre', 
			auteur=fauxAuteur, 
			date=datetime.datetime.now(), 
			url='Non.com', 
			texte='Le faux texte c\'est ici', 
			nb_comment=999)

		# Test de Corpus et ses méthodes
		fauxCorp = Corpus.Corpus('FauxCorpus')
		fauxCorp.addDocument(fauxAuteur, fauxDocu)

		# Tests de la méthode statsAuthor si l'auteur existe
		fauxCorp.statAuthor('Angelo')

		# Tests de la méthode statsAuthor si l'auteur n'existe pas !
		fauxCorp.statAuthor('sdfjqsdoghdqspdjqdhdfhsdqdhs')

		# Test de la classe Author et ses méthodes
		fauxAuteur2 = Author.Author('clement')

		self.assertEqual(fauxAuteur2.get_name(), 'clement')
		fauxAuteur2.add(fauxDocu)
		fauxAuteur2.stats()

		fauxAuteur2.set_name('angelo')
		self.assertEqual(fauxAuteur2.get_name(), 'angelo')


	def test_auteur(self):
     
		auteur = Author.Author("angelo")
		self.assertEqual("angelo", auteur.get_name())


if __name__ == '__main__':
	unittest.main()