from Author import Author
from scipy import sparse
import pandas as pd
import numpy as np
import re
from color_console.coloramaALF import *

# def singleton(cls):
# 	instance = [None]
# 	def wrapper(*args, **kwargs):
# 		if instance[0] is None:
# 			instance[0] = cls(*args, **kwargs)
# 		return instance[0]
# 	return wrapper

# @singleton
class Corpus():
	"""
	Classe Corpus, qui contient beaucoup de métadonnées

	Param init :
		nom [str] : Nom du corpus, d'usage on y mettra la query utilisée pour les documents du dit corpus

	Attributs :
		__nom [str]                 : nom du corpus
		__id2aut [dict]             : dictionnaire des auteurs  
		__id2loc [dict]             : dictionnaire des documents
		__ndoc [int]                : nombre de documents
		__naut [int]                : nombre d'auteurs
		__allInOne [str]            : string contenant TOUT le contenu des documents du corpus
		__vocadf [pandas.DataFrame] : DataFrame contenant trois colonnes : les mots associés avec leurs occurrences dans le corpus (terFreq) et au nombre de documents où ils sont present (docFreq)
		__mat_TFxIDF [scipy.sparse.lil_matrix] : matrice TFxIDF du corpus (None tant que la méthode createMatTF n'est pas executée)


	Getters | Setters :
		get_nom()      | set_nom(nom)
		get_id2aut()   | *
		get_id2loc()   | *
		get_ndoc()     | *
		get_naut()     | *
		get_allInOne() | *
		get_vocadf()   | *

	Methodes :
		addDocument(auteur, document) : Permet d'ajouter un document avec son auteur associé
		giveDate(self)                : Permet de recuperer deux listes : une avec les ids des docs du corpus, et une avec leur date associée. (Utiliser dans la fonction Corpus.show)
		show(nbShow)                  : Permet d'afficher les nbShow premier(s) document(s) du corpus
		statsAuthor(authorName)       : Permet d'afficher les stats d'un auteur du corpus (nb de docs...)
		search(motif)                 : Permet de chercher les endroits où il y a la sequence `motif` dans le corpus
		concorde(motif, contexte)     : Renvoie un DataFrame contenant les passages où l'on trouve un motif, avec son contexte associé
		stats(n)                      :	Permet d'afficher les stats du corpus : le nombre de mots différents, aussi que les n mots les plus récurrents
		createMatTF()                 : Methode permettant de créer la matrice TFxIDF comme décrite dans la page : https://fr.wikipedia.org/wiki/TF-IDF
		makeSearch(enters)            : Methode qui cherche, et affiche, les documents les plus interressants par rapport a l'entrée enters
	"""

	def __init__(self, nom):
		self.set_nom(nom)
		self.__id2aut = {}
		self.__id2loc = {}
		self.__ndoc = 0
		self.__naut = 0
		self.__allInOne = ''
		self.__vocadf = pd.DataFrame.from_dict({'mot':[], 'term freq.':[], 'document freq.':[]})
		self.__mat_TFxIDF = None

	def __str__(self):
		return f"<Corpus {self.get_nom()} | Nb Document(s) : {self.get_ndoc()} | Nb Auteur(s) : {self.get_naut()}>"

	def __repr__(self):
		return f"<Corpus {self.get_nom()} | Nb Document(s) : {self.get_ndoc()} | Nb Auteur(s) : {self.get_naut()}>"

	# Les getters :
	get_nom = lambda self : self.__nom
	get_id2aut = lambda self : self.__id2aut
	get_id2loc = lambda self : self.__id2loc
	get_ndoc = lambda self : self.__ndoc
	get_naut = lambda self : self.__naut
	get_allInOne = lambda self : self.__allInOne
	get_vocadf = lambda self : self.__vocadf
	# Les setters :
	def set_nom(self, enter):
		if type(enter) == str and len(enter) > 0: 
			self.__nom = enter
		else:
			raise "WARNING Corpus.set_nom : mauvais type"



	def show(self, nbShow, reverse=False, display=False):
		"""
		Permet d'afficher les nbShow premiers documents du corpus (trié par date croissante)
		
		Param : 
			- nbShow [int]   : Nombre de document(s) à afficher
			- reverse [bool] : True pour trier par date décroissante

		Return :
			- returnStr [list] : liste avec les infos de show
		"""
		returnStr = []

		if not display:
			print(f"---- Corpus {self.__nom} [{self.__ndoc} docs. | {self.__naut} auth.] :")
			print(f"- {nbShow} premier(s) document(s), trier par date :")
		
		returnStr = [f" Corpus {self.__nom} [{self.__ndoc} docs. | {self.__naut} auth.] :",
					 f"- {nbShow} premier(s) document(s), trier par date :"]

		if reverse:
			funcm = max
		else:
			funcm = min

		xk, xd = self.giveDate()

		for i in range(nbShow):
			imin = xd.index(funcm(xd))
			returnStr.append(self.__id2loc[xk[imin]].info(display=display))
			xk.pop(imin)
			xd.pop(imin)

		if display : return returnStr



	def giveDate(self):
		"""
		Permet de recuperer deux listes : une avec les ids des docs du corpus, et une avec leur date associée.
		Utiliser dans la fonction Corpus.show

		Return :
			- xkeys, xdate [list, list] : liste des ids, liste des dates
		"""
		xkeys = []
		xdate = []

		for key, val in self.__id2loc.items():
			xkeys.append(key)
			xdate.append(val.get_date())

		return xkeys, xdate



	def addDocument(self, auteur, document):
		"""
		Permet d'ajouter un document avec son auteur associé

		Paramètres : 
			- auteur [list] : liste des auteur(s) aillant participé(s) au document
			- document [Document.Document] : document à ajouter au corpus
		"""
		self.__id2loc[f"id{len(self.__id2loc.keys())}"] = document
		self.__ndoc += 1
		self.__allInOne += document.get_texte()

		for mot, recu in document.get_voca().items():

			if mot not in list(self.__vocadf['mot']):
				new = {'mot':[mot], 'term freq.':[recu], 'document freq.':[1]}
				self.__vocadf = pd.merge(self.__vocadf, pd.DataFrame.from_dict(new), how='outer')

			else:
				self.__vocadf.loc[self.__vocadf['mot'] == mot, 'term freq.'] += recu
				self.__vocadf.loc[self.__vocadf['mot'] == mot, 'document freq.'] += 1


		for auteur_i in auteur:
			if auteur_i in self.__id2aut.keys():
				self.__id2aut[auteur_i].add(document)
			else:
				self.__id2aut[auteur_i] = Author(auteur_i)
				self.__id2aut[auteur_i].add(document)
				self.__naut += 1



	def statAuthor(self, authorName):
		"""	
		Permet d'afficher les stats d'un auteur du corpus (nb de docs...)

		Paramètres :
			- authorName [str] : nom de l'auteur pour obtenir ses stats

		Return :
			- name [str]      : nom de l'auteur
			- ndoc [int]      : nombre de documents écrits par l'auteur
			- sizedoc [float] : taille moyenne (en mots) des documents de l'auteur
		"""
		if authorName in self.__id2aut.keys():
			return self.__id2aut[authorName].stats()
		else:
			print(f"{fyellow}INFO : {authorName} inconnu{rall}")
			return authorName, 0, 0


	
	def search(self, motif):
		"""
		Permet de chercher les endroits ou il y a la séquence `motif` dans le corpus

		Paramètres :
			- motif [str] : motif que l'on veut chercher dans le corpus

		Return : 
			- indexSeq [list] : liste des indexes où se trouve le modif dans le texte
		"""
		indexSeq = []

		for match in list(re.finditer(motif, self.__allInOne)):
			indexSeq.append(match.start())

		return indexSeq



	def concorde(self, motif, contexte=10):
		"""
		Renvoie un DataFrame contenant les passages où l'on trouve un motif, avec son contexte associé

		Paramètres :
			- motif [str]    : motif que l'on veut chercher dans le corpus
			- contexte [int] : nombre de caractère(s) que l'on souhaite pour le contexte

		Return :
			- df [pandas.DataFrame] : DataFrame contenant les contextes à gauche et à droite ainsi que le motif
		"""
		dico = {'contexte gauche':[], 'motif':[], 'contexte droit':[]}
		k = len(motif)

		for ind in self.search(motif):
			dico['contexte gauche'].append('...' + self.__allInOne[ind-contexte:ind])
			dico['motif'].append(motif)
			dico['contexte droit'].append(self.__allInOne[ind+k:ind+k+contexte] + '...')

		df = pd.DataFrame.from_dict(dico)

		return df



	def stats(self, n, display=False):
		"""
		Permet d'afficher les stats du corpus : le nombre de mots différents, aussi que les n mots les plus récurrents

		Paramètres :
			- n [int] : voir les n mots les plus récurrents

		Return :
			- df [pandas.DataFrame] : df contenant les résultats si display est True
		"""
		if not display:
			print(f"\nSTATS sur le corpus {self.__nom} [{self.__ndoc} docs.]")
			print(f"\tNombre de mots differents : {len(list(self.__vocadf['mot']))}")
			print(f"\tLes {n} mots les plus fréquents : ")

		df_tri = self.__vocadf.sort_values(by='term freq.', ascending=False)

		if not display:
			print(df_tri[:n].to_string(index=False))
		else:
			return df_tri[:n]



	def createMatTF(self):
		"""
		Methode permettant de créer la matrice TFxIDF comme décrite dans la page : https://fr.wikipedia.org/wiki/TF-IDF

		Return:
			- mat_TFxIDF [scipy.sparse.lil_matrix] : Matrice TFxIDF calculée
		"""

		ndoc = self.__ndoc
		nmot = len(self.__vocadf['mot'])

		mots = list(self.__vocadf['mot'])
		mots.sort()

		mat_TFxIDF = sparse.lil_matrix((ndoc, nmot)).astype(float)
		
		for iddoc, val in self.__id2loc.items():
			nbmot = len(val.get_voca().keys())

			for mot, TF in val.get_voca().items():
				p = self.__vocadf.loc[self.__vocadf['mot'] == mot, 'document freq.'].values[0]
				mat_TFxIDF[int(iddoc[2:]), mots.index(mot)] = TF/nbmot * np.log(ndoc/p)

		self.__mat_TFxIDF = mat_TFxIDF

		return mat_TFxIDF



	def makeSearch(self, enters, display=False):
		"""
		Methode qui cherche, et affiche, les documents les plus interressants par rapport a l'entrée `enters`

		Paramètres :
			- enters [str] : mots pour la recherche de documents

		Return :
			- returnPP [list] : list contenant les résultats si display est True
		"""

		ndoc = self.__ndoc
		nmot = len(self.__vocadf['mot'])
		mots = list(self.__vocadf['mot'])
		mots.sort()

		enter = enters.lower().split(" ")
		vectEnter = np.zeros(nmot).astype(int)

		nbmot = len(enter)

		for mot in enter:
			if mot in mots:
				vectEnter[mots.index(mot)] = 1
			else:
				print(f"{fyellow}INFO : il n'y a pas {mot} rechercher dans le corpus{rall}")

		if self.__mat_TFxIDF is None:
			self.createMatTF()
			print(f"{fgreen}INFO : création Matrice TFxIDF{rall}")

		vectProb = self.__mat_TFxIDF.dot(vectEnter)

		iddoc = list(range(0, ndoc))

		RID, PROD = zip(*sorted(list(zip(iddoc, vectProb)), key=lambda x: x[1], reverse=True))

		dicRet = {'Titre':[], 'URL':[], 'Score':[]}

		nbResult = sum([x > 0 for x in PROD])

		if not display:

			print(f"\n{nbResult} Result(s) for '{enters}' : \n")

			for rid, prod in zip(RID, PROD):
				if prod > 0:
					s = f"id{rid}"
					print(f"| Titre : {self.__id2loc[s].get_titre()}")
					print(f"| URL   : {self.__id2loc[s].get_url()}")
					print(f"| Score : {np.round(prod, 3)}\n")

		else:

			returnPP = [f"{nbResult} Result(s) for '{enters}' :"]

			for rid, prod in zip(RID, PROD):
				if prod > 0:
					s = f"id{rid}"

					if self.__id2loc[s].get_type() == "RedditDocument":
						offset = 'https://www.reddit.com'
					else:
						offset = ''

					returnPP.append([self.__id2loc[s].get_titre(), 
									 self.__id2loc[s].get_type(), 
									 offset + self.__id2loc[s].get_url(), 
									 np.round(prod, 3)])

			return returnPP


