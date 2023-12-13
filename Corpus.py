from Author import Author
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

	Getters | Setters :
		get_nom()      | set_nom(nom)
		get_id2aut()   | *
		get_id2loc()   | *
		get_ndoc()     | *
		get_naut()     | *
		get_allInOne() | *

	Method :
		addDocument(auteur, document) : Permet d'ajouter un document avec son auteur associer
		giveDate(self)                : Permet de recuper deux liste : une avec les ids des docs du corpus, et une avec leur date associé. (Utiliser dans la fonction Corpus.show)
		show(nbShow)                  : Permet d'afficher les nbShow premier document du corpus
		statsAuthor(authorName)       : Permet d'afficher les stats d'un auteur du corpus (nb de doc ...)
	"""

	def __init__(self, nom):
		self.set_nom(nom)
		self.__id2aut = {}
		self.__id2loc = {}
		self.__ndoc = 0
		self.__naut = 0
		self.__allInOne = ''


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


			

