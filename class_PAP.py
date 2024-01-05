import urllib, urllib.request
import datetime
import pickle
import praw
import os

import func_PAP
from Document import *
from Author import *
from Corpus import *



class ScrapingGeneral():
    
	"""
	Class scrapingGeneral, qui va servir à la gestion du scraping, et ceux avec plusieurs sources
	Pour plus d'information suplémentaire : 
	- Source pour le scraping Reddit : https://towardsdatascience.com/scraping-reddit-data-1c0af3040768
	- Source pour le scraping Arxiv : https://info.arxiv.org/help/api/index.html
	
	Param init :
		client_id [str]     : donner par default (voir source pour plus d'info)
		client_secret [str] : donner par default (voir source pour plus d'info)
		user_agent [str]    : donner par default (voir source pour plus d'info)
		url0_arxiv [str]    : donner par default, l'url `prefixe` par default pour la recherche arxiv
		datafolder [str]    : nom du dossier ou ce trouve les dossiers | 'data/'

	Attribut : 
		client_id [str]        : (voir source pour plus d'info)
		client_secret [str]    : (voir source pour plus d'info)
		user_agent [str]       : (voir source pour plus d'info)
		source [dict]          : dict contenant des sources pour certaine info (ex: source['reddit'])
		url0_arxiv [str]       : l'url `prefixe` par default pour la recherche arxiv
		datafolder [str]       : nom du dossier ou ce trouve les dossiers
		corpus [Corpus.Corpus] : corpus, contenant tout les documents, auteurs, ... (regarder sa doc pour plus d'info)

	Methode : 
		scrapReddit(query, nb_docs)          : Permet de scrap des articles de reddit et les returner
		scrapArxiv(query, nb_docs, nb_start) : Permet de scrap des articles de arxiv et les returner
		scrap(query, *args, **kwargs)        : Permet de scrap des articles de nature diverses et d'alimenter corpus
		save()                               : Permet de save le corpus sous un dataPAP, gerer avec Pickle
		charged()                            : Permet de charger des donnee deja faite, present dans la dossier datafolder
	"""

	def __init__(self,  
				client_id='gsfJcIOUGkM8YvJdWR_jWg',
				client_secret='bt1447AxbH2w3iEdLK5SyD8k_zM9Dg',
				user_agent='testscrapww',
				url0_arxiv='http://export.arxiv.org/api/query?',
				datafolder='data/'):

		self.client_id = client_id
		self.client_secret = client_secret
		self.user_agent = user_agent
		self.url0_arxiv = url0_arxiv
		self.datafolder = datafolder
		self.source = {'reddit' : 'https://towardsdatascience.com/scraping-reddit-data-1c0af3040768',
					   'arxiv'  : 'https://info.arxiv.org/help/api/index.html'}
		self.corpus = None



	def factoryDocument(self, doctype, **kwargs):

		if doctype == 'Reddit':
			return RedditDocument(**kwargs)

		elif doctype == 'Arxiv':
			return ArxivDocument(**kwargs)

		else:
			raise 'factoryError'


	def scrapArxiv(self, query, nb_docs, nb_start=0, limitCarac=20):
		"""
		Permet de scrap des articles de arxiv et les retourner

		Param :
			query [str]      : thème de la recherche
			nb_docs [int]    : nombre de documents arxiv voulus
			nb_start [int]   : on va scrap et prendre les texts a partir de nb_start article (0 par def)
			limitCarac [int] : limite de caractere du texte principal pour accepter un document
		"""

		url = self.url0_arxiv + 'search_query=all:{}&start={}&max_results={}'.format(query, nb_start, nb_docs)
		

		request = urllib.request.urlopen(url).read().decode('utf-8')
		dic = func_PAP.xmlto(request)


		if 'entry' in dic['feed'].keys():

			for i in range(min(nb_docs, len(dic['feed']['entry']))):
				if len(dic['feed']['entry'][i]['summary'].replace('\n', ' ')) > limitCarac:
					try:
						if type(dic['feed']['entry'][i]['author']) == dict:
							auteur = [dic['feed']['entry'][i]['author']['name']]
						elif type(dic['feed']['entry'][i]['author']) == list:
							auteur = []
							for auteur_i in dic['feed']['entry'][i]['author']:
								auteur.append(auteur_i['name'])
					except:
						print('WARNING : Problème de formatage dans les auteurs de source arxiv')
						auteur = ''
					titre = dic['feed']['entry'][i]['title']
					date0 = dic['feed']['entry'][i]['published'].replace('T', " ").replace('Z', "")
					date = datetime.datetime.strptime(date0, '%Y-%m-%d %H:%M:%S')
					url = dic['feed']['entry'][i]['link'][0]['@href']
					texte = dic['feed']['entry'][i]['summary'].replace('\n', ' ')
					category = dic['feed']['entry'][i]['arxiv:primary_category']['@term']

					docu = self.factoryDocument(doctype='Arxiv', texte=texte, titre=titre, date=date, auteur=auteur, url=url, category=category)
					self.corpus.addDocument(auteur, docu)

		else:
			print(f"WARNING : Aucun documents pour la query '{query}'")

		return None



	def scrapReddit(self, query, nb_docs=1, limitCarac=20):
		"""
		Permet de scrap des articles de reddit et les returner

		Param :
			query [str]      : theme de la recherche
			nb_docs [int]    : nombre de document reddit voulu
			limitCarac [int] : limite de caractere du texte principal pour accepter un document
		"""

		reddit = praw.Reddit(client_id='gsfJcIOUGkM8YvJdWR_jWg', client_secret=self.client_secret, user_agent=self.user_agent)
		posts = reddit.subreddit(query).hot(limit=nb_docs)

		for post in posts:
			if len(post.selftext.replace('\n', ' ')) > limitCarac:
				if post.author == None:
					auteur = ['Anonym']
				else:
					auteur = [post.author.name]
				date = datetime.datetime.utcfromtimestamp(post.created_utc)
				url = post.permalink
				titre = post.title
				texte = post.selftext.replace('\n', ' ')
				nb_comment = post.num_comments
				docu = self.factoryDocument(doctype='Reddit', texte=texte, titre=titre, date=date, auteur=auteur, url=url, nb_comment=nb_comment)
				self.corpus.addDocument(auteur, docu)

		return None


	def scrap(self, query, limitCarac=20, *args, **kwargs):
		"""
		Permet de scrap des articles de nature diverses et d'alimenter corpus

		Param :
			query [str]      : theme de la recherche
			limitCarac [int] : limite de caractere du texte principal pour accepter un document
			**kwargs         : donne le nombre de document pour chaque source
				(Ex : arxiv=10 pour 10 document arxiv)
		"""

		self.corpus = Corpus(query)

		kwReturns = {}

		for key in kwargs.keys():
			
			if key in ['arxiv', 'ar']:
				kwReturns['arxiv'] = self.scrapArxiv(query, nb_docs=int(kwargs[key]), limitCarac=limitCarac)
				print("INFO : Sucess to scrap arxiv document")

			elif key in ['reddit', 're']:
				kwReturns['reddit'] = self.scrapReddit(query, nb_docs=int(kwargs[key]), limitCarac=limitCarac)
				print("INFO : Sucess to scrap reddit document")

			else:
				print('WARNING : the source {} is not avaible'.format(key))



	def save(self):
		"""
		Permet de save le corpus sous un dataPAP, gerer avec Pickle
		"""

		name = f"{self.datafolder}{self.corpus.get_nom()}_corpus.dataPAP"
		print(f"INFO : Sucess to save corpus '{self.corpus.get_nom()}'")

		with open(name, 'wb') as f:
			pickle.dump(self.corpus, f)



	def charged(self, nom):
		"""
		Permet de charger des donnee deja faite, present dans la dossier datafolder
		
		Param : 
			nom [str] : nom du corpus voulu
		"""

		if f"{nom}_corpus.dataPAP" in os.listdir(self.datafolder):

			with open(f"{self.datafolder}{nom}_corpus.dataPAP", 'rb') as f:
				self.corpus = pickle.load(f)
				print(f"INFO : Sucess to charge corpus '{nom}'")
		else:
			print(f"WARNING : il n'y a pas de {self.datafolder}{nom}_corpus.dataPAP")
