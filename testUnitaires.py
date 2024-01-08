import unittest
import os
from class_PAP import ScrapingGeneral
import Document
import Corpus
import Author
import datetime
import pandas

class TestStringMethods(unittest.TestCase):

	def test_ScrapingGeneral(self):
		# Tests sur l'instance ScrapingGenerale
		
		sg = ScrapingGeneral()
		# Test : Est-ce que la création de l'instance a fonctionné et est-ce que l'attribut corpus a bien été initialisée à None
		self.assertTrue(sg.corpus is None)

		sg.scrap('python', arxiv=20, reddit=20)

		# Test : Scrap d'arxiv et reddit : on regarde si le nombre de documents du corpus n'est plus nul

		self.assertTrue(sg.corpus.get_ndoc() > 0)

		# Si l'on a déjà un corpus avec cette query de save, on la supprime
		if f"{sg.corpus.get_nom()}_corpus.dataPAP" in os.listdir(sg.datafolder):
			os.remove(f"{sg.datafolder}{sg.corpus.get_nom()}_corpus.dataPAP")

		# Test du save du corpus :
		sg.save()
		self.assertIn(f"{sg.corpus.get_nom()}_corpus.dataPAP", os.listdir(sg.datafolder))

		sg2 = ScrapingGeneral()
		sg2.charged('python')
  
		# Test : On verifie que les données sont chargées correctement
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
		# Tests de la classe Document et Author

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

	def test_corpus_method(self):
		# Tests des méthodes de Corpus ajoutées à la version 2 du projet
  
		# Création de documents et d'auteurs fictifs
		fauxAuteur2 = [['Angelo', 'Clement'], ['Angelo'], ['Celian']]

		fauxDocu3 = Document.RedditDocument(titre='Intelligence artifielle par gpt 1', 
			auteur=fauxAuteur2[2], 
			date=datetime.datetime.now(), 
			url='Non.com', 
			texte="L'intelligence artificielle (IA) a émergé comme une force transformative, redéfinissant la manière dont nous interagissons avec la technologie et percevons le monde qui nous entoure. Dotée de capacités d'apprentissage et d'analyse exceptionnelles, l'IA permet des avancées spectaculaires dans des domaines tels que la médecine, la finance, et la recherche scientifique. Cependant, son ascension rapide soulève également des questions éthiques et sociétales cruciales, notamment sur la confidentialité des données, la prise de décision automatisée et les implications sur l'emploi. En naviguant dans cette ère d'intelligence artificielle, la société est confrontée au défi de trouver un équilibre entre l'exploitation de son potentiel et la mise en place de garde-fous pour préserver nos valeurs fondamentales", 
			nb_comment=999)
  
		fauxDocu4 = Document.ArxivDocument(titre='Intelligence artifielle par gpt 2', 
			auteur=fauxAuteur2[1], 
			date=datetime.datetime.now(), 
			url='Non.com', 
   			texte="Dans le sillage de l'IA, émerge un paysage technologique en constante évolution qui façonne notre quotidien de manière insoupçonnée. Des assistants virtuels aux algorithmes de recommandation personnalisée, l'IA a infiltré notre vie quotidienne, simplifiant des tâches jadis complexes et augmentant notre productivité. Cependant, en parallèle, elle suscite des débats sur les implications à long terme de son développement. Les chercheurs, les décideurs et la société dans son ensemble se trouvent à la croisée des chemins, devant concilier l'innovation technologique avec la préservation de l'éthique et des droits humains. Ainsi, la trajectoire de l'intelligence artificielle devient un véritable enjeu sociétal, appelant à une réflexion approfondie sur la manière dont nous souhaitons façonner notre avenir avec cette puissante force technologique",
			category='IA')

		corpus = Corpus.Corpus("test corpus")
		corpus.addDocument(document=fauxDocu3, auteur=fauxAuteur2[2])
		corpus.addDocument(document=fauxDocu4, auteur=fauxAuteur2[1])
  
		# Méthode search
		print(corpus.search(motif='société'))
		self.assertEqual(3, len(corpus.search('technologique'))) # il y a bien 3 fois le mot technologie dans l'ensemble du corpus

		# Méthode concorde
		print(corpus.concorde(motif='société', contexte=20))
		self.assertTrue(isinstance(corpus.concorde(motif='société', contexte=20), pandas.DataFrame)) # le retour est bien un dataframe

		# Méthode stats
		print(type(corpus.stats(n=20, display=True))) # test de l'affichage de la méthode stats
		self.assertEqual(corpus.stats(n=20, display=True).shape, (20, 3)) # on teste que le dataframe retourner à la bonne dimension
  
		# Méthode createMatTF
		print(corpus.createMatTF()) # affichage de la matrice TFxIDF
		self.assertEqual(corpus.createMatTF().shape, (2, 146))
  
		# Méthode makesearch()
		corpus.makeSearch(enters='évolution', display=True) # affichage
  
		# Testons les plusieurs cas pour la méthode makesearch()
		self.assertEqual(corpus.makeSearch(enters='évolution', display=True).shape, (1, 3)) # On s'attend à avoir un résultat car "évolution" est présent dans un texte
		self.assertEqual(corpus.makeSearch(enters='intelligence', display=True).shape, (0, 3)) # présent dans les 2 documents donc pas de résultats
		self.assertEqual(corpus.makeSearch(enters='angelo', display=True).shape, (0, 3)) # présent dans aucun des documents donc pas de résultats

		

if __name__ == '__main__':
	unittest.main()