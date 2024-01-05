import datetime
import re



class Document():
	"""
	Classe servant a contenir les métadonnée d'un document

	Param init :
		titre [str]              : titre du document (def '', pas conseillé)
		auteur [list]            : auteurs du document (def [])
		date [datetime.datetime] : date de publication (def: None)
		url [str]                : url source du document (def: '')
		texte [str]              : contenu textuel du document (def: '', pas conseillé)

	Attribut :
		__titre [str]              : titre du document
		__auteur [list]            : auteurs du document
		__date [datetime.datetime] : date de publication
		__url [str]                : url source du document
		__texte [str]              : contenu textuel du document
		__voca [dict]              : dictionnaire qui associe les mots du texte (qui sont les keys) avec les occurence dans le document (pour les values)
		__type [str]               : type, plus précise pour les classes filles
		__size [list]              : liste contenant 3 int [<nombre carac>, <nombre mots>, <nombre phrases>] dans le doc

	Getters | Setters :
		get_titre()  | set_titre(titre)
		get_auteur() | set_auteur(auteur)
		get_date()   | set_date(date)
		get_url()    | set_url(url)
		get_texte()  | set_texte(texte)
		get_size()   | *
		get_voca()   | set_statsMots()

	Methode
		info()              : Permet d'afficher des infos sur le document
		nettoyertexte(text) : Permet de nettoyer le texte du document
	"""

	def __init__(self, titre='', auteur=[], date=None, url='', texte=''):
		self.set_titre(titre)
		self.set_auteur(auteur)
		self.set_date(date)
		self.set_url(url)
		self.set_texte(texte)

		self.__type = "Document"
		self.__size = [len(texte), len(texte.split(" ")), len(texte.split("."))] #caractere, mots, phrase

	def __str__(self):
		return f"<Document | {self.get_titre()} | Auteur : {self.get_auteur()}>"

	def __repr__(self):
		return f"<Document | {self.get_titre()} | Auteur : {self.get_auteur()}>"

	# Les getters :
	def get_titre(self): 
		return self.__titre
	def get_auteur(self): 
		return self.__auteur
	def get_date(self): 
		return self.__date
	def get_url(self): 
		return self.__url
	def get_texte(self): 
		return self.__texte
	def get_voca(self):
		return self.__voca
	def get_size(self): 
		return self.__size
	# Les setters :
	def set_titre(self, enter):
		if type(enter) == str and len(enter) > 0: 
			self.__titre = enter
		else:
			raise "WARNING Document.set_titre : mauvais type"
	def set_auteur(self, enter):
		if type(enter) == list: 
			self.__auteur = enter
		else:
			raise "WARNING Document.set_auteur : mauvais type"
	def set_date(self, enter):
		if type(enter) == type(datetime.datetime.now()): 
			self.__date = enter
		else:
			raise "WARNING Document.set_date : mauvais type"
	def set_url(self, enter):
		if type(enter) == str and len(enter) > 0: 
			self.__url = enter
		else:
			raise "WARNING Document.set_url : mauvais type"
	def set_texte(self, enter):
		if type(enter) == str and len(enter) > 0:
			self.__texte = enter
			self.set_statsMots()
		else:
			raise "WARNING Document.set_texte : mauvais type"


	def set_statsMots(self):
		aio = self.nettoyerTexte(self.__texte).split(' ')
		mots, voca = list(set(aio)), {}
		if '' in mots : 
			mots.remove('')
		mots.sort()
		for m in mots : 
			voca[m] = aio.count(m)
		self.__voca = voca


	def nettoyerTexte(self, text):
		"""
		Permet de nettoyer le texte du document

		Param :
			text [str] : texte à nettoyer

		Return :
			[str] : texte nettoyer
		"""
		t = re.sub(r'[^\w\s]', '', text.lower().replace('.', ' ').replace('\n', ' '))
		t = re.sub(r'[\d]', '', t)
		return t


	def info(self):
		"""
		Permet d'afficher des infos sur le document
		"""
		print(f"Document :")
		print(f"\tTitre : {self.__titre}")
		print(f"\tAuteur : {self.__auteur}")
		print(f"\tDate : {self.__date}")
		print(f"\tSource url : {self.__url}")
		print(f"\tContenu : [{self.__size[0]} carac. | {self.__size[1]} word | {self.__size[2]} sent.]\n{self.__texte}\n")






class RedditDocument(Document):
	"""
	RedditDocument heriter de Document. Permet d'ajouter des attributs unique de Reddit.

	Param init :
		titre [str]              : (heritage Document) titre du document (def '', pas conseiller)
		auteur [list]            : (heritage Document) auteurs du document (def [])
		date [datetime.datetime] : (heritage Document) date de publication (def: None)
		url [str]                : (heritage Document) url source du document (def: '')
		texte [str]              : (heritage Document) contenu textuel du document (def: '', pas conseiller)
		nb_comment [int]         : nombre de commentaire du document (ici de l'article Reddit plus precisement)(def: 0)

	Attribut :
		__titre [str]              : (heritage Document) titre du document
		__auteur [list]            : (heritage Document) auteurs du document
		__date [datetime.datetime] : (heritage Document) date de publication
		__url [str]                : (heritage Document) url source du document
		__texte [str]              : (heritage Document) contenu textuel du document
		__voca [dict]              : (heritage Document) dictionnaire qui associe les moyts du texte (qui sont les keys) avec les occurence dans le document (pour les values)
		__type [str]               : (heritage Document) type du document (source)
		__size [list]              : (heritage Document) liste contenant 3 int [<nombre carac>, <nombre mots>, <nombre phrase>] dans le doc
		__nb_comment [int]         : nombre de commentaire du document (ici de l'article Reddit plus precisement)

	Getters | Setters :
		get_titre()      | set_titre(titre)           (heritage Document)
		get_auteur()     | set_auteur(auteur)         (heritage Document)
		get_date()       | set_date(date)             (heritage Document)
		get_url()        | set_url(url)               (heritage Document)
		get_texte()      | set_texte(texte)           (heritage Document)
		get_size()       | *                          (heritage Document)
		get_voca()       | set_statsMots()            (heritage Document)
		get_nb_comment() | set_nb_comment(nb_comment)
		get_type()       | *

	Methode
		nettoyertexte(text) : (heritage Document) Permet de nettoyer le texte du document
		info()              : Permet d'afficher des infos sur le document (ajout du nombre de commentaire /rapport a Document.info)
	"""

	def __init__(self, titre='', auteur=[], date=None, url='', texte='', nb_comment=0):
		super(RedditDocument, self).__init__(titre, auteur, date, url, texte)
		self.__type = "RedditDocument"
		self.set_nb_comment(nb_comment)

	def __str__(self):
		return f"<RedditDocument | {self.get_titre()} | Auteur : {self.get_auteur()}>"

	def __repr__(self):
		return f"<RedditDocument | {self.get_titre()} | Auteur : {self.get_auteur()}>"

	# Les getters :
	get_nb_comment = lambda self : self.__nb_comment
	get_type = lambda self : self.__type
	# Les setters : 
	def set_nb_comment(self, enter):
		if type(enter) == int: 
			self.__nb_comment = enter
		else:
			raise "WARNING Document.set_nb_comment : mauvais type"



	def info(self):
		"""
		Permet d'afficher des infos sur le document
		"""
		print(f"Document :")
		print(f"\tTitre : {self.get_titre()}")
		print(f"\tAuteur : {self.get_auteur()}")
		print(f"\tDate : {self.get_date()}")
		print(f"\tType : {self.get_type()}")
		print(f"\tSource url : {self.get_url()}")
		print(f"\tNb comment : {self.__nb_comment}")
		print(f"\tContenu : [{self.get_size()[0]} carac. | {self.get_size()[1]} word | {self.get_size()[2]} sent.]\n{self.get_texte()}\n")






class ArxivDocument(Document):
	"""
	ArxivDocument heriter de Document. Permet d'ajouter des attributs unique d'Arxiv.

	Param init :
		titre [str]              : (heritage Document) titre du document (def '', pas conseiller)
		auteur [list]            : (heritage Document) auteurs du document (def [])
		date [datetime.datetime] : (heritage Document) date de publication (def: None)
		url [str]                : (heritage Document) url source du document (def: '')
		texte [str]              : (heritage Document) contenu textuel du document (def: '', pas conseiller)
		category [str]           : categorie du document, renseignement directement par l'API d'Arxiv (def: '')

	Attributs :
		__titre [str]              : (heritage Document) titre du document
		__auteur [list]            : (heritage Document) auteurs du document
		__date [datetime.datetime] : (heritage Document) date de publication
		__url [str]                : (heritage Document) url source du document
		__texte [str]              : (heritage Document) contenu textuel du document
		__voca [dict]              : (heritage Document) dictionnaire qui associe les moyts du texte (qui sont les keys) avec les occurence dans le document (pour les values)
		__size [list]              : (heritage Document) liste contenant 3 int [<nombre carac>, <nombre mots>, <nombre phrase>] dans le doc
		__category [str]           : categorie du document, renseignement directement par l'API d'Arxiv (def: '')

	Getters | Setters :
		get_titre()    | set_titre(titre)       (heritage Document)
		get_auteur()   | set_auteur(auteur)     (heritage Document)
		get_date()     | set_date(date)         (heritage Document)
		get_url()      | set_url(url)           (heritage Document)
		get_texte()    | set_texte(texte)       (heritage Document)
		get_size()     | *                      (heritage Document)
		get_voca()     | set_statsMots()        (heritage Document)
		get_category() | set_category(category)
		get_type()     | *

	Methode
		nettoyertexte(text) : (heritage Document) Permet de nettoyer le texte du document
		info() : Permet d'afficher des infos sur le document (ajout de la categorie /rapport a Document.info)
	"""

	def __init__(self, titre='', auteur=[], date='', url='', texte='', category=''):
		super(ArxivDocument, self).__init__(titre, auteur, date, url, texte)
		self.__type = "ArxivDocument"
		self.set_category(category)

	def __str__(self):
		return f"<ArxivDocument | {self.get_titre()} | Auteur : {self.get_auteur()}>"

	def __repr__(self):
		return f"<ArxivDocument | {self.get_titre()} | Auteur : {self.get_auteur()}>"

	# Les getters :
	get_category = lambda self : self.__category
	get_type = lambda self : self.__type
	# Les setters : 
	def set_category(self, enter):
		if type(enter) == str: 
			self.__category = enter
		else:
			raise "WARNING Document.set_category : mauvais type"



	def info(self):
		"""
		Permet d'afficher des infos sur le document
		"""
		print(f"Document :")
		print(f"\tTitre : {self.get_titre()}")
		print(f"\tAuteur : {self.get_auteur()}")
		print(f"\tDate : {self.get_date()}")
		print(f"\tType : {self.get_type()}")
		print(f"\tSource url : {self.get_url()}")
		print(f"\tCategory : {self.__category}")
		print(f"\tContenu : [{self.get_size()[0]} carac. | {self.get_size()[1]} word | {self.get_size()[2]} sent.]\n{self.get_texte()}\n")
		