from dash import dcc, html, dash_table
from class_PAP import ScrapingGeneral
import os
from color_console.coloramaALF import *
import pandas as pd
import plotly.express as px

class htmlEvent():
	"""
	Class htmlEvent, qui a deux objectif : 
	- Donner les composants html pour notre interface Dash
	- Gérer un objet ScrapingGeneral via un attribut (sg)

	Attributs : 
		current_html [int]     : (a faire ...)
		div [list]             : (a faire ...)
		fig [***]              : (a faire ...)
		sg [ScrapingGeneral]   : (a faire ...)

	Méthodes : 
		resetValue
		giveCorpusName
		giveHiddens
		findCorpus
		chargedCorpus
		html0
		html1
		html2
	"""

	def __init__(self):

		self.resetValue()

		self.current_html = 0
		self.div = self.html0()

		df = pd.DataFrame.from_dict({'Aled':['Oskour'], 'mots':[0]})
		self.fig = px.histogram(df, x="mots")
		
		# Création d'un objets scrapingGeneral
		self.sg = ScrapingGeneral()


	def resetValue(self):
		self.value = {
			'input1' : '',
			'input2' : 50,
			'input3' : 50, # Ne pas changer 
			'input4'  : '',
			'input5'  : None,

			'button1' : 0,
			'button2' : 0,
			'button3' : 0,

			'table1' : None
		}


	def giveCorpusName(self, folder='data', fileinfo='info_corpus.txt'):

		if self.value['table1'] is None:
			
			return html.P(f"Choisir un corpus", style={'color':'#dd0000'})

		else:
			row = self.value['table1']['row']
			with open(f"./{folder}/update_{fileinfo}", 'r') as f:
				name = f.read().split('\n')[row+1].split('-')[0]
			
			return html.P(f"Charger {name}", style={'font-weight': 'bold', 'color':'#00dd00'})


	def giveHiddens(self, *hiddens):

		hiddensDiv = []

		hiddensDiv.append(dcc.Interval(id='interv', interval=3600*1000, n_intervals=0))

		for hide in hiddens:
			if "input" in hide:
				n = hide.split('input')[1]
				for ni in n:
					if type(self.value[f"input{ni}"]) == list : gvalue = None
					else : gvalue = self.value[f"input{ni}"]
					hiddensDiv.append(dcc.Input(id=f"input{ni}", type="hidden", n_submit=1, value=gvalue))

			elif "button" in hide:
				n = hide.split('button')[1]
				for ni in n:
					hiddensDiv.append(html.Button(id=f"button{ni}", type="hidden", n_clicks=0, style={"display": "none"}))
				
			elif "table" in hide:
				n = hide.split('table')[1]
				for ni in n:
					hiddensDiv.append(html.Div([dash_table.DataTable([{'None':'None'}], [{"name": i, "id": i} for i in ['None']], id=f"table{ni}", active_cell=None)],
						style={'display':'none'}))

			elif "graph" in hide:
				n = hide.split('graph')[1]
				for ni in n:
					hiddensDiv.append(html.Div([dcc.Graph(id=f"graph{ni}")], style={'display':'none'}))

			else:
				hiddensDiv.append(html.P(f"Demande de cacher {hide} [inconnu]", style={'color':'#dd0000'}))

		return hiddensDiv


	def findCorpus(self, folder='data', fileinfo='info_corpus.txt'):

		data = []

		with open(f"./{folder}/{fileinfo}", 'r') as f:
			lines = f.read().split('\n')

			col = lines[0].split('-')
			corpusAll = lines[1:]
			updateinfo = [lines[0]]

		for corpus in corpusAll:

			d = {}

			vals = corpus.split('-')

			if f"{vals[0]}_corpus.dataPAP" in os.listdir(f"./{folder}/"):

				updateinfo.append(corpus)
				vals[0] = vals[0][0].upper() + vals[0][1:]

				for key, val in zip(col, vals):
					d[key] = val

				data.append(d)

			else:
				pass
				# print(f"UPDATE : Le corpus {vals[0]} present dans {fileinfo} n'existe pas dans le dossier {folder}")

		with open(f"./{folder}/update_{fileinfo}", 'w') as f:
			f.write('\n'.join(updateinfo))
			f.close()

		return data, col


	def chargedCorpus(self, folder='data', fileinfo='info_corpus.txt'):

		row = self.value['table1']['row']
		with open(f"./{folder}/update_{fileinfo}", 'r') as f:
			name = f.read().split('\n')[row+1].split('-')[0]
		
		self.sg.charged(name)

		return name





	def html0(self):

		if self.value['input4'] == '':

			return [dcc.Markdown("""        ## Bienvenue sur la page du Projet Avancé Python (PAP)       """),

				dcc.Markdown("""        Tu veux :        """),
				dcc.RadioItems(['Charger un corpus existant', 'Créer un nouveau corpus'], id="input4", value=self.value['input4']),

				] + self.giveHiddens('input1235', 'button123', 'table1', 'graph1')

		elif self.value['input4'] == 'Créer un nouveau corpus':

			return [dcc.Markdown("""        ## Bienvenue sur la page du Projet Avancé Python (PAP)       """),

				dcc.Markdown("""        Tu veux :        """),
				dcc.RadioItems(['Charger un corpus existant', 'Créer un nouveau corpus'], id="input4", value=self.value['input4']),

				dcc.Markdown("""        Choix de la query :        """),
				dcc.Input(id="input1", type="text", placeholder="Query...", n_submit=1, value=self.value['input1']),

				html.Div([html.P("Nombre de document Arxiv voulu :"),
				dcc.Input(id="input2", type="number", placeholder="Nb Arxiv", n_submit=1, value=self.value['input2'], min=0, max=1000)],
				style = {'margin-left': '10px', 'display' : 'flex'}),

				html.Div([html.P("Nombre de document Reddit voulu :"),
				dcc.Input(id="input3", type="number", placeholder="Nb Reddit", n_submit=1, value=self.value['input3'], min=0, max=1000)],
				style = {'margin-left': '10px', 'display' : 'flex'}),

				html.Br(),

				html.Button('Créer !', id='button1', n_clicks=self.value['button1'], style={'margin-top':'10px'})

				] + self.giveHiddens('input5', 'button23', 'table1', 'graph1')

		else:
			corpus_dispo, col = self.findCorpus()

			return [dcc.Markdown("""        ## Bienvenue sur la page du Projet Avancé Python (PAP)       """),

				dcc.Markdown("""        Tu veux :        """),
				dcc.RadioItems(['Charger un corpus existant', 'Créer un nouveau corpus'], id="input4", value=self.value['input4']),

				html.Div([html.P("Liste des corpus existant : "),
				dash_table.DataTable(corpus_dispo, [{"name": i, "id": i} for i in col], id='table1', active_cell=self.value['table1'])]),

				html.Br(),

				html.Button(self.giveCorpusName(), id='button2', n_clicks=self.value['button2'], style={'margin-top':'10px'})

				] + self.giveHiddens('input1235', 'button13', 'graph1')





	def html1(self):

		return [dcc.Markdown(f"""        ## Pour la query {self.value['input1']}       """),

			dcc.Markdown("""        Qu'est ce que tu veux faire :        """),
			dcc.RadioItems(['Faire une recherche', 'Statistiques', 'Analyse'], id="input2", value=self.value['input2']),	

			html.Button('Retour', id='button2', n_clicks=self.value['button2'])

			] + self.giveHiddens('input1345', 'button13', 'table1', 'graph1')





	def html2(self):

		## Event Faire une recherche

		if self.value['input2'] == 'Faire une recherche':
			
			return [dcc.Markdown(f"""        ## Pour la query {self.value['input1']}       """),

				dcc.Markdown("""        Choix de recherche :        """),
				dcc.Input(id="input3", type="text", placeholder="Recherche...", n_submit=1, value=self.value['input3']),

				html.Button('Retour', id='button2', n_clicks=self.value['button2']),
				html.Button('Rechercher', id='button1', n_clicks=self.value['button1']),

				html.Div([html.P('none')], style={'display':'none'})

				] + self.giveHiddens('input1245', 'button3', 'table1', 'graph1')



		## Event Statistiques

		elif self.value['input2'] == 'Statistiques':

			offset = [dcc.Markdown(f"""        ## Pour la query {self.value['input1']}       """),
					  dcc.Markdown("""        Statistiques :        """),
					  dcc.Dropdown(['Show first document', 'Stats Authors', 'Concorde', 'Stats Mots'], value=self.value['input3'], id='input3')]


			# Si on a rien selectionner
			if self.value['input3'] in ['', None]:

				suite = [html.Button('Retour', id='button2', n_clicks=self.value['button2'])] + self.giveHiddens('input1245', 'button13', 'table1', 'graph1')


			# Si on selectionne Concorde
			elif self.value['input3'] == 'Concorde':

				suite = [dcc.Markdown("""        Choix du motif :        """),

						html.Div([html.P("Motif :"),
							dcc.Input(id="input4", type="text", placeholder="Motif...", n_submit=1, value=self.value['input4'])],
							style = {'margin-left': '10px', 'display' : 'flex'}),

						html.Div([html.P("Taille :"),
							dcc.Input(id="input5", type="number", placeholder="Taille...", n_submit=1, value=self.value['input5'], min=5, max=50)],
							style = {'margin-left': '10px', 'display' : 'flex'}),

						html.Div([dash_table.DataTable([{'None':'None'}], [{"name": i, "id": i} for i in ['None']], id='table1', active_cell=None)],
							style={'display':'none'}),

						html.Button('Retour', id='button2', n_clicks=self.value['button2']),
						html.Button('Valider', id='button1', n_clicks=self.value['button1'])

						] + self.giveHiddens('input12', 'button3', 'graph1')


			# Si on selectionne Stats Mots
			elif self.value['input3'] == 'Stats Mots':

				suite = [dcc.Markdown("""        Nombre de mots :        """),

						html.Div([html.P("Nombre :"),
							dcc.Input(id="input4", type="number", placeholder="Nombre...", n_submit=1, value=self.value['input4'], min=5, max=100)],
							style = {'margin-left': '10px', 'display' : 'flex'}),

						html.Div([dash_table.DataTable([{'None':'None'}], [{"name": i, "id": i} for i in ['None']], id='table1', active_cell=None)],
							style={'display':'none'}),

						html.Button('Retour', id='button2', n_clicks=self.value['button2']),
						html.Button('Valider', id='button1', n_clicks=self.value['button1'])

						] + self.giveHiddens('input125', 'button3', 'graph1')


			# Si on selectionne Stats Authors
			elif self.value['input3'] == 'Stats Authors':

				suite = [dcc.Markdown("""        Statistiques sur un autheur :        """),

						html.Div([html.P("Nom :"),
							dcc.Input(id="input4", type="text", placeholder="Nom...", n_submit=1, value=self.value['input4'])],
							style = {'margin-left': '10px', 'display' : 'flex'}),

						html.P(f"Nom :", style = {'display' : 'none'}),

						html.Button('Retour', id='button2', n_clicks=self.value['button2']),
						html.Button('Valider', id='button1', n_clicks=self.value['button1'])

						] + self.giveHiddens('input125', 'button3', 'table1', 'graph1')


			# Si on selectionne Show first documents
			elif self.value['input3'] == 'Show first document':

				suite = [dcc.Markdown("""        Premier documents :        """),

						html.Div([html.P("Nombre de docs :"),
							dcc.Input(id="input4", type="number", placeholder="Nombre...", n_submit=1, value=self.value['input4'], min=5, max=50)],
							style = {'margin-left': '10px', 'display' : 'flex'}),

						dcc.Checklist(['Date dans l\'ordre décroissant'], id='input5', value=self.value['input5']),

						html.P(f"Nom :", style = {'display' : 'none'}),

						html.Button('Retour', id='button2', n_clicks=self.value['button2']),
						html.Button('Valider', id='button1', n_clicks=self.value['button1'])

						] + self.giveHiddens('input12', 'button3', 'table1', 'graph1')

			# return la Div de statistiques
			return offset + suite


		## Event Analyse

		elif self.value['input2'] == 'Analyse':

			return [dcc.Markdown(f"""        ## Pour la query {self.value['input1']}       """),

				dcc.Markdown("""        Analyse Disponible :        """),

				dcc.RadioItems(['Histogram sur le nombre de mots par source', 'Image Mots mdr oskour'], id="input3", value=self.value['input3']),

				html.Div([dcc.Graph(id=f"graph1")], style={'display':'none'}),
				html.Div([]),

				html.Br(),

				html.Button('Retour', id='button2', n_clicks=self.value['button2'])

				] + self.giveHiddens('input1245', 'button13', 'table1')

		else:

			return [dcc.Markdown(f"""        ## Pour la query {self.value['input1']}       """),

				dcc.Markdown("""        Page Inconnu :        """),

				html.Button('Retour', id='button2', n_clicks=self.value['button2'])

				] + self.giveHiddens('input12345', 'button13', 'table1', 'graph1')