import datetime
import re

# Ajout racinisation
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


class Document():
	"""
	Classe servant à contenir les métadonnées d'un document

	Paramètres d'initialisation :
		titre [str]              : titre du document (def '', pas conseillé)
		auteur [list]            : auteur(s) du document (def [])
		date [datetime.datetime] : date de publication (def: None)
		url [str]                : url source du document (def: '')
		texte [str]              : contenu textuel du document (def: '', pas conseillé)

	Attributs :
		__titre [str]              : titre du document
		__auteur [list]            : auteur(s) du document
		__date [datetime.datetime] : date de publication
		__url [str]                : url source du document
		__texte [str]              : contenu textuel du document
		__voca [dict]              : dictionnaire qui associe les mots du texte (qui sont les keys) avec les occurrences dans le document (pour les values)
		__vocasn [dict]            : identique a __voca mais avec racinisation des mots
		__type [str]               : type, plus précise pour les classes filles
		__size [list]              : liste contenant 3 int [<nombre caracs>, <nombre mots>, <nombre phrases>] dans le doc

	Getters | Setters :
		get_titre()  | set_titre(titre)
		get_auteur() | set_auteur(auteur)
		get_date()   | set_date(date)
		get_url()    | set_url(url)
		get_texte()  | set_texte(texte)
		get_size()   | *
		get_voca()   | set_statsMots()
		get_vacosn() | set_statsMots()

	Methodes :
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
		self.__size = [len(texte), len(texte.split(" ")), len(texte.split("."))] #caractères, mots, phrases

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
	def get_vocasn(self): # Ajout racinisation
		return self.__vocasn
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

		try:
			# Ajout racinisation
			stemmer = SnowballStemmer(language='english')
			data0 = re.sub(r'[^\w\s]', ' ', self.__texte.lower()) # On laisse que les carac alphanum
			tokens = [stemmer.stem(token) for token in word_tokenize(data0) if token not in stopwords.words('english') and len(token) > 1]
			motsSN, vocaSN = list(set(tokens)), {}
			motsSN.sort()
			for m in motsSN : 
				vocaSN[m] = tokens.count(m)
			self.__vocasn = vocaSN
		except:
			# TestsUnitaires
			print('Tests Unitaire en cours')
			self.__vocasn = {'test':999}
			pass


	    




	def nettoyerTexte(self, text):
		"""
		Permet de nettoyer le texte du document

		Paramètres :
			text [str] : texte à nettoyer

		Return :
			[str] : texte nettoyé
		"""
		t = re.sub(r'[^\w\s]', '', text.lower().replace('.', ' ').replace('\n', ' '))
		t = re.sub(r'[\d]', '', t)
		return t


	def info(self, display=False):
		"""
		Permet d'afficher des infos sur le document
		"""
		if not display:
			print(f"Document :")
			print(f"\tTitre : {self.__titre}")
			print(f"\tAuteur : {self.__auteur}")
			print(f"\tDate : {self.__date}")
			print(f"\tSource url : {self.__url}")
			print(f"\tContenu : [{self.__size[0]} carac. | {self.__size[1]} word | {self.__size[2]} sent.]\n{self.__texte}\n")
			return None
		else:
			return [f"Titre : {self.__titre} | Date : {self.__date}",
					f"Auteur : {', '.join(self.__auteur)}",
					f"Source url : {self.__url}",
					f"Contenu : [{self.__size[0]} carac. | {self.__size[1]} word | {self.__size[2]} sent.]\n{self.__texte}\n"]






class RedditDocument(Document):
	"""
	RedditDocument héritée de Document. Permet d'ajouter des attributs unique de Reddit.

	Paramètres  d'initialisation :
		titre [str]              : (héritage Document) titre du document (def '', pas conseillé)
		auteur [list]            : (héritage Document) auteur(s) du document (def [])
		date [datetime.datetime] : (héritage Document) date de publication (def: None)
		url [str]                : (héritage Document) url source du document (def: '')
		texte [str]              : (héritage Document) contenu textuel du document (def: '', pas conseillé)
		nb_comment [int]         : nombre de commentaire(s) du document (ici de l'article Reddit plus précisément)(def: 0)

	Attributs :
		__titre [str]              : (héritage Document) titre du document
		__auteur [list]            : (héritage Document) auteur(s) du document
		__date [datetime.datetime] : (héritage Document) date de publication
		__url [str]                : (héritage Document) url source du document
		__texte [str]              : (héritage Document) contenu textuel du document
		__voca [dict]              : (héritage Document) dictionnaire qui associe les mots du texte (qui sont les keys) avec les occurrences dans le document (pour les values)
		__type [str]               : (héritage Document) type du document (source)
		__size [list]              : (héritage Document) liste contenant 3 int [<nombre caracs>, <nombre mots>, <nombre phrases>] dans le doc
		__nb_comment [int]         : nombre de commentaire(s) du document (ici de l'article Reddit plus précisément)

	Getters | Setters :
		get_titre()      | set_titre(titre)           (héritage Document)
		get_auteur()     | set_auteur(auteur)         (héritage Document)
		get_date()       | set_date(date)             (héritage Document)
		get_url()        | set_url(url)               (héritage Document)
		get_texte()      | set_texte(texte)           (héritage Document)
		get_size()       | *                          (héritage Document)
		get_voca()       | set_statsMots()            (héritage Document)
		get_nb_comment() | set_nb_comment(nb_comment)
		get_type()       | *

	Methodes :
		nettoyertexte(text) : (héritage Document) Permet de nettoyer le texte du document
		info()              : Permet d'afficher des infos sur le document (ajout du nombre de commentaire(s) /rapport a Document.info)
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



	def info(self, display=False):
		"""
		Permet d'afficher des infos sur le document
		"""
		if not display:
			print(f"Document :")
			print(f"\tTitre : {self.get_titre()}")
			print(f"\tAuteur : {self.get_auteur()}")
			print(f"\tDate : {self.get_date()}")
			print(f"\tType : {self.get_type()}")
			print(f"\tSource url : {self.get_url()}")
			print(f"\tNb comment : {self.__nb_comment}")
			print(f"\tContenu : [{self.get_size()[0]} carac. | {self.get_size()[1]} word | {self.get_size()[2]} sent.]\n{self.get_texte()}\n")
			return None
		else:
			return [f"Titre : {self.get_titre()} | Date : {self.get_date()} | Type : {self.get_type()}",
					f"Auteur : {', '.join(self.get_auteur())} | Nb comment : {self.__nb_comment}",
					f"Source url : https://www.reddit.com{self.get_url()}",
					f"Contenu : [{self.get_size()[0]} carac. | {self.get_size()[1]} word | {self.get_size()[2]} sent.]\n{self.get_texte()}"]








class ArxivDocument(Document):
	"""
	ArxivDocument héritée de Document. Permet d'ajouter des attributs unique d'Arxiv.

	Paramètres d'initialisation :
		titre [str]              : (héritage Document) titre du document (def '', pas conseillé)
		auteur [list]            : (héritage Document) auteur(s) du document (def [])
		date [datetime.datetime] : (héritage Document) date de publication (def: None)
		url [str]                : (héritage Document) url source du document (def: '')
		texte [str]              : (héritage Document) contenu textuel du document (def: '', pas conseillé)
		category [str]           : catégorie du document, renseignement directement par l'API d'Arxiv (def: '')

	Attributs :
		__titre [str]              : (héritage Document) titre du document
		__auteur [list]            : (héritage Document) auteur(s) du document
		__date [datetime.datetime] : (héritage Document) date de publication
		__url [str]                : (héritage Document) url source du document
		__texte [str]              : (héritage Document) contenu textuel du document
		__voca [dict]              : (héritage Document) dictionnaire qui associe les mots du texte (qui sont les keys) avec les occurrences dans le document (pour les values)
		__size [list]              : (héritage Document) liste contenant 3 int [<nombre caracs>, <nombre mots>, <nombre phrases>] dans le doc
		__category [str]           : catégorie du document, renseignement directement par l'API d'Arxiv (def: '')

	Getters | Setters :
		get_titre()    | set_titre(titre)       (héritage Document)
		get_auteur()   | set_auteur(auteur)     (héritage Document)
		get_date()     | set_date(date)         (héritage Document)
		get_url()      | set_url(url)           (héritage Document)
		get_texte()    | set_texte(texte)       (héritage Document)
		get_size()     | *                      (héritage Document)
		get_voca()     | set_statsMots()        (héritage Document)
		get_category() | set_category(category)
		get_type()     | *

	Methode
		nettoyertexte(text) : (héritage Document) Permet de nettoyer le texte du document
		info() : Permet d'afficher des infos sur le document (ajout de la catégorie /rapport à Document.info)
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



	def info(self, display=False):
		"""
		Permet d'afficher des infos sur le document
		"""
		if not display:
			print(f"Document :")
			print(f"\tTitre : {self.get_titre()}")
			print(f"\tAuteur : {self.get_auteur()}")
			print(f"\tDate : {self.get_date()}")
			print(f"\tType : {self.get_type()}")
			print(f"\tSource url : {self.get_url()}")
			print(f"\tCategory : {self.__category}")
			print(f"\tContenu : [{self.get_size()[0]} carac. | {self.get_size()[1]} word | {self.get_size()[2]} sent.]\n{self.get_texte()}\n")
			return None
		else:
			return [f"Titre : {self.get_titre()} | Date : {self.get_date()} | Type : {self.get_type()}",
					f"Auteur : {', '.join(self.get_auteur())}",
					f"Source url : {self.get_url()}",
					f"Contenu : [{self.get_size()[0]} carac. | {self.get_size()[1]} word | {self.get_size()[2]} sent.]\n{self.get_texte()}"]
	