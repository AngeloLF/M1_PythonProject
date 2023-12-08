


class Author():
	"""
	Classe servant a contenir les meta donnee d'un auteur

	Param init :
		name [str] : nom de l'auteur

	Attribut :
		__name [str]        : nom de l'auteur
		__ndoc [int]        : nombre de document publiee
		__production [dict] : dict des document ecrit par l'auteur
		__size [list]       : liste contenant 3 int [<nombre carac>, <nombre mots>, <nombre phrase>] ecrit par l'auteur
	
	Getters | Setters :
		get_name()       | set_name(name)
		get_ndoc()       | *
		get_production() | *
		get_size()       | *

	Methode:
		add(document) : Permet d'ajouter un document dans la liste de l'auteur
		stats()       : Permet d'afficher des stats sur l'auteur (nb doc ...)
	"""

	def __init__(self, name):
		self.set_name(name)
		self.__production = {}
		self.__ndoc = 0
		self.__size = [0, 0, 0]
	
	def __str__(self):
		return f"<Author | {self.__name} | Nombre de document : {self.__ndoc}>" ### NOTE 0x413$Mod



	# Les getters :
	get_name = lambda self : self.__name
	get_ndoc = lambda self : self.__ndoc
	get_production = lambda self : self.__production
	get_size = lambda self : self.__size
	# Les setters :
	def set_name(self, enter):
		if type(enter) == str and len(enter) > 0: 
			self.__name = enter
		else:
			raise "WARNING Author.set_name : mauvais type"



	def add(self, document):
		"""
		Permet d'ajouter un document dans la liste de l'auteur

		Param :
			document [Document.Document] : Document à ajouter dans la liste des document
		"""
		if document.get_titre() not in self.__production.keys(): ### NOTE 0x413$Mod
			self.__ndoc += 1
			self.__size[0] += document.get_size()[0]
			self.__size[1] += document.get_size()[1]
			self.__size[2] += document.get_size()[2]
			self.__production[document.get_titre()] = document



	def stats(self):
		"""
		Permet d'afficher des stats sur l'auteur (nb doc ...)
		"""
		print(f"Pour l'auteur {self.__name} :")
		print(f"\t- Nombre de document(s) écrit : {self.__ndoc}")
		print(f"\t- Taille moy des document : {self.__size[1]/self.__ndoc:1f} mots")