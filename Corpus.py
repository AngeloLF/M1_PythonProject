from Author import Author
from scipy import sparse
import pandas as pd
import numpy as np
import re



class Corpus():
	"""
	Classe corpus, qui contient beacoup de meta-donnee

	Param init :
		nom [str] : Nom du corpus, d'usage on y mettra la query utiliser pour les documents dudit corpus

	Attribut :
		__nom [str]                 : nom du corpus
		__id2aut [dict]             : dictionnaire des auteurs  
		__id2loc [dict]             : dictionnaire des documents
		__ndoc [int]                : nombre de documents
		__naut [int]                : nombre d'auteurs
		__allInOne [str]            : string contenant TOUT le contenu des document du corpus
		__vocadf [pandas.DataFrame] : DataFrame contenant trois colonne : les mots associé avec leurs occurences dans le corpus (terFreq) et au nombre de doc ou ils sont present (docFreq)


	Getters | Setters :
		get_nom()      | set_nom(nom)
		get_id2aut()   | *
		get_id2loc()   | *
		get_ndoc()     | *
		get_naut()     | *
		get_allInOne() | *
		get_vocadf()   | *

	Method :
		addDocument(auteur, document) : Permet d'ajouter un document avec son auteur associer
		giveDate(self)                : Permet de recuper deux liste : une avec les ids des docs du corpus, et une avec leur date associé. (Utiliser dans la fonction Corpus.show)
		show(nbShow)                  : Permet d'afficher les nbShow premier document du corpus
		statsAuthor(authorName)       : Permet d'afficher les stats d'un auteur du corpus (nb de doc ...)
		search(motif)                 : Permet de chercher les endroits ou il y a la sequence `motif` dans le corpus
		concorde(motif, contexte)     : Renvoie un DataFrame contenant les passage ou l'on trouve un motif, avec son contexte associé
		stats(n)                      :	Permet d'afficher les stats du corpus : le nombre de mots différents, aussi que les n mots les plus récurrent
	"""

	def __init__(self, nom):
		self.set_nom(nom)
		self.__id2aut = {}
		self.__id2loc = {}
		self.__ndoc = 0
		self.__naut = 0
		self.__allInOne = ''
		self.__vocadf = pd.DataFrame.from_dict({'mot':[], 'term freq.':[], 'document freq.':[]})


	def __str__(self):
		return f"<Corpus {self.get_nom()} | Nb Document : {self.get_ndoc()} | Nb Auteur : {self.get_naut()}>"

	def __repr__(self):
		return f"<Corpus {self.get_nom()} | Nb Document : {self.get_ndoc()} | Nb Auteur : {self.get_naut()}>"

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



	def show(self, nbShow, reverse=False):
		"""
		Permet d'afficher les nbShow premier document du corpus (trier par date croissante)
		
		Param : 
			- nbShow [int]   : Nombre de document à afficher
			- reverse [bool] : True pour afficher trier par date decroissante
		"""
		print(f"---- Corpus {self.__nom} [{self.__ndoc} docs. | {self.__naut} auth.] :")
		print(f"- {nbShow} premier document, trier par date : \n")

		if reverse:
			funcm = max
		else:
			funcm = min

		xk, xd = self.giveDate()

		for i in range(nbShow):
			imin = xd.index(funcm(xd))
			self.__id2loc[xk[imin]].info()
			xk.pop(imin)
			xd.pop(imin)



	def giveDate(self):
		"""
		Permet de recuper deux liste : une avec les ids des docs du corpus, et une avec leur date associé.
		Utiliser dans la fonction Corpus.show

		Return :
			[list, list] : liste des id, liste des date
		"""
		xkeys = []
		xdate = []

		for key, val in self.__id2loc.items():
			xkeys.append(key)
			xdate.append(val.get_date())

		return xkeys, xdate



	def addDocument(self, auteur, document):
		"""
		Permet d'ajouter un document avec son auteur associer

		Param : 
			auteur [list] : liste des auteur(s) aillant participer au document
			document [Document.Document] : document a ajouter au corpus
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
		Permet d'afficher les stats d'un auteur du corpus (nb de doc ...)

		Param :
			authorName [str] : nom de l'auteur dont l'on veut les stats
		"""
		if authorName in self.__id2aut.keys():
			self.__id2aut[authorName].stats()
		else:
			print(f"WARNING : {authorName} inconnu")


	
	def search(self, motif):
		"""
		Permet de chercher les endroits ou il y a la sequence `motif` dans le corpus

		Param :
			motif [str] : motif que l'on veut chercher dans le corpus

		Return : 
			[list] : liste des index ou ce trouve le modif dans le texte
		"""
		indexSeq = []

		for match in list(re.finditer(motif, self.__allInOne)):
			indexSeq.append(match.start())

		return indexSeq



	def concorde(self, motif, contexte=10):
		"""
		Renvoie un DataFrame contenant les passage ou l'on trouve un motif, avec son contexte associé

		Param :
			motif [str]    : motif que l'on veut chercher dans le corpus
			contexte [int] : nombre de caractère que l'on souhaite pour le contexte

		Return :
			[pandas.DataFrame] : DataFrame contenant les contexte gauche et droite aussi que le motif
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
		Permet d'afficher les stats du corpus : le nombre de mots différents, aussi que les n mots les plus récurrent

		Param :
			n [int] : voir les n mots les plus récurrent
		"""
		print(f"\nSTATS sur le corpus {self.__nom} [{self.__ndoc} docs.]")
		print(f"\tNombre de mots differents : {len(list(self.__vocadf['mot']))}")
		print(f"\tLes {n} mots les plus fréquents : ")

		df_tri = self.__vocadf.sort_values(by='term freq.', ascending=False)

		if not display:
			print(df_tri[:n].to_string(index=False))
		else:
			return df_tri[:n]



	def createMatTF(self):

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

		return mat_TFxIDF



	def makeSearch(self, enters):

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
				print(f"INFO : il n'y a pas {mot}")

		mat_TFxIDF = self.createMatTF()

		vectProb = mat_TFxIDF.dot(vectEnter)

		iddoc = list(range(0, ndoc))

		RID, PROD = zip(*sorted(list(zip(iddoc, vectProb)), key=lambda x: x[1], reverse=True))

		dicRet = {'Titre':[], 'URL':[], 'Score':[]}

		nbResult = sum([x > 0 for x in PROD])

		print(f"\n{nbResult} Result(s) for '{enters}' : \n")

		for rid, prod in zip(RID, PROD):
			if prod > 0:
				s = f"id{rid}"
				print(f"| Titre : {self.__id2loc[s].get_titre()}")
				print(f"| URL   : {self.__id2loc[s].get_url()}")
				print(f"| Score : {np.round(prod, 3)}\n")