from dash import dcc, html
from class_PAP import ScrapingGeneral


class htmlEvent():

	def __init__(self):

		self.value = {
			'input1' : "",
			'input2' : 50,
			'input3' : 50,

			'radio1'  : "",
			'button1' : 0,
			'button2' : 0,
			'drop1'   : None,
		}

		self.current_html = 0
		self.div = self.html0()
		
		# Création d'un objets scrapingGeneral
		self.sg = ScrapingGeneral()



	def giveHiddens(self, *hiddens):

		hiddensDiv = []

		for hide in hiddens:
			if "button" not in hide:
				hiddensDiv.append(dcc.Input(id=hide, type="hidden", n_submit=1, value=self.value[hide]))
			else:
				hiddensDiv.append(html.Button(id=hide, type="hidden", n_clicks=0, style={"display": "none"}))

		return hiddensDiv



	def html0(self, numdiv=None):

		return [dcc.Markdown("""        ## Bienvenue sur la page du Projet Avancé Python (PAP)       """),
			dcc.Markdown("""        Choix de la query :        """),

			dcc.Input(id="input1", type="text", placeholder="Query..........", n_submit=1, value=self.value['input1']),

			dcc.Markdown("""        Tu veux :        """),
			dcc.RadioItems(['Charger', 'Make'], id="radio1", value=self.value['radio1']),

			html.Div([html.P("Nombre de document Arxiv voulu :"),
			dcc.Input(id="input2", type="number", placeholder="Nb Arxiv", n_submit=1, value=self.value['input2'], min=0, max=1000)],
			style = {'margin-left': '10px', 'display' : 'flex'}),

			html.Div([html.P("Nombre de document Reddit voulu :"),
			dcc.Input(id="input3", type="number", placeholder="Nb Reddit", n_submit=1, value=self.value['input3'], min=0, max=1000)],
			style = {'margin-left': '10px', 'display' : 'flex'}),

			html.Br(),

			html.Button('Lezgo', id='button1', n_clicks=self.value['button1'], style={'margin-top':'10px'})

			] + self.giveHiddens('drop1', 'button2')



	def html1(self):

		return [dcc.Markdown(f"""        ## Pour la query {self.value['input1']}       """),

			dcc.Markdown("""        Qu'est ce que tu veux voir :        """),
			dcc.Dropdown(['Show first document', 'Stats Authors', 'Concorde', 'Stats Mots', 'Search !'], value=self.value['drop1'], id='drop1'),

			html.Button('Retour', id='button2', n_clicks=self.value['button2']),
			html.Button('Valider !', id='button1', n_clicks=self.value['button1'])

			] + self.giveHiddens('input1', 'input2', 'input3', 'radio1')