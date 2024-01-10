from dash import Dash, dcc, html, Input, Output, callback, dash_table
import classDash_serv as DashHtml
import plotly.graph_objects as go
from color_console.coloramaALF import *

callInput = [Input(component_id="input1", component_property="value"),       # vals[0]
	  		 Input(component_id="input2", component_property="value"),       # vals[1]
	  		 Input(component_id="input3", component_property="value"),       # vals[2]
	  		 Input(component_id="input4", component_property="value"),       # vals[3]
	  		 Input(component_id="input5", component_property="value"),       # vals[4]
	  		 Input(component_id="button1", component_property="n_clicks"),   # vals[5]
	  		 Input(component_id="button2", component_property="n_clicks"),   # vals[6]
	  		 Input(component_id="button3", component_property="n_clicks"),   # vals[7]
	  		 Input(component_id="table1", component_property="active_cell"), # vals[8]
	  		 Input(component_id="interv", component_property="n_intervals")] # vals[9]
callOutput = [Output(component_id="division", component_property="children"), Output("graph1", "figure")]

htmlClass = DashHtml.htmlEvent()


app = Dash(__name__, external_stylesheets=["css/all.css"])
app.layout = html.Div([dcc.Markdown(""" # Projet PAP """, style={'textAlign': 'center'}), 
	html.Div(htmlClass.div, id='division')],
	style={'background-color': '#f0f0dd', 'padding-top':'10px', 'padding-bottom':'20px'})


@callback(*callOutput, *callInput)
def chargedMake_Event(*vals):

	if vals[8] is None : callTable = None
	else : callTable = 'ROWX'

	print(f"\nCALLBACK : Inputs {vals[0:5]} | Buttons {vals[5:8]} | Table {callTable} | Interv {vals[9]}")

	### Page HTML 0

	if htmlClass.current_html == 0:	

		# Changement radio button
		if vals[3] == 'Charger un corpus existant' and htmlClass.value['input4'] != 'Charger un corpus existant' :
			htmlClass.value['input4'] = vals[3]
			htmlClass.div = htmlClass.html0()

		elif vals[3] == 'Créer un nouveau corpus' and htmlClass.value['input4'] != 'Créer un nouveau corpus' :
			htmlClass.value['input4'] = vals[3]
			htmlClass.div = htmlClass.html0()


		# Changement de query
		if vals[0] != htmlClass.value['input1']:
			htmlClass.value['input1'] = vals[0]
			htmlClass.div[4] = htmlClass.html0()[4]


		# Changement nombre de documents arxiv
		if vals[1] != htmlClass.value['input2'] :
			htmlClass.value['input2'] = vals[1]
			htmlClass.div[5] = htmlClass.html0()[5]


		# Changement nombre de document reddit
		if vals[2] != htmlClass.value['input3'] : 
			htmlClass.value['input3'] = vals[2]
			htmlClass.div[6] = htmlClass.html0()[6]


		# Selectionne un corpus sur le tableau
		if vals[8] != htmlClass.value['table1']:
			htmlClass.value['table1'] = vals[8]
			htmlClass.div[3] = htmlClass.html0()[3]
			htmlClass.div[5] = htmlClass.html0()[5]


		# Bouton Créer (un nouveau corpus)
		if vals[5] == 1:
			# Si le dernier n'es pas la fin de création d'un corpus
			if htmlClass.div[-1].children != "Corpus sauvegardé !":
				# Si la query n'est pas vide : 
				if vals[0] != '':

					print(f"{flblue}INFO : Création du corpus {htmlClass.value['input1']}...{rall}")

					# Si il y avait le msg de remplir la query, on l'enlève
					if htmlClass.div[-1].children == "Il faut remplir la query !":
						htmlClass.div.pop(-1)

					htmlClass.div[8] = html.Button(id='button1', type="hidden", n_clicks=0, style={"display": "none"})
					htmlClass.div[9] = dcc.Interval(id='interv', interval=400, n_intervals=100)

					htmlClass.div.append(html.P(f"Création du corpus {htmlClass.value['input1']}...", style={'color':'#dd0000'}))

				# Si la query est vide, on met un message : 
				else:
					print(f"{fyellow}LITTLE WARNING : Il faut remplir la query !{rall}")	
					if htmlClass.div[-1].children != "Il faut remplir la query !":
						htmlClass.div.append(html.P("Il faut remplir la query !", style={'color':'#ee0000'}))

			# Sinon : reset la page
			else:
				htmlClass.value['input1'] = ''
				htmlClass.div = htmlClass.html0()

		# Lorsque le bouton Créer est cliquer, il met notre n_interval a 100, et donc une seconde après a 101 et active ceci UNE FOIS
		if vals[9] == 101:

			print(f"{flblue}INFO : Begin scrap...{rall}")

			infoScraping = htmlClass.sg.scrap(htmlClass.value['input1'], arxiv=htmlClass.value['input2'], reddit=htmlClass.value['input3'])

			htmlClass.div.pop(-1)

			for key, val in infoScraping.items():
				nb, msg = val
				if msg is None:
					htmlClass.div.append(html.P(f"Nombre de document {key} récupéré(s) : {nb}", style={'color':'#00dd00'}))
				else:
					htmlClass.div.append(html.P(f"Pour {key} : {msg}", style={'color':'#dd0000'}))

			htmlClass.sg.save()
			htmlClass.div.append(html.P(f"Corpus sauvegardé !", style={'font-weight': 'bold', 'color':'#00dd00'}))

		# Garder un callback actif le temps du scraping (obligatoire pour le rafraichissement automatique de la page)
		if vals[9] > 101:
			print(f"{flblue}INFO : Scrap en cours...{rall}")
			if htmlClass.div[-1].children != "Corpus sauvegardé !":

				# Pour faire clignoter les '...' sur l'interface
				if htmlClass.value['input1'] in htmlClass.div[-1].children:
					child = htmlClass.div[-1].children.split(htmlClass.value['input1'])
					if len(child[1]) == 3:
						newchild = child[0] + htmlClass.value['input1'] + '.'
					else:
						newchild = child[0] + htmlClass.value['input1'] + child[1] + '.'
					htmlClass.div[-1] = html.P(newchild, style={'color':'#dd0000'})

				htmlClass.div[9] = dcc.Interval(id='interv', interval=400, n_intervals=vals[9])

			else:
				htmlClass.div[8] = html.Button('Fabriquer un autre corpus', id='button1', n_clicks=htmlClass.value['button1'], style={'margin-top':'10px'})
				htmlClass.div[9] = dcc.Interval(id='interv', interval=3600*1000, n_intervals=0)


		# Button charger corpus
		if vals[6] == 1:

			# Si on a selectionner un corpus
			if vals[8] is not None:
				print(f"{flblue}INFO : Go HMLT 1 ...{rall}")
				query = htmlClass.chargedCorpus()
				htmlClass.current_html = 1
				htmlClass.resetValue()
				htmlClass.value['input1'] = query
				htmlClass.div = htmlClass.html1()






	### Page HTML 1

	elif htmlClass.current_html == 1:

		if vals[1] != htmlClass.value['input2']:

			htmlClass.value['input2'] = vals[1]
			htmlClass.value['input3'] = ''

			print(f"{flblue}INFO : Go HMLT 2 [{htmlClass.value['input2']}] ...{rall}")
			htmlClass.current_html = 2
			htmlClass.div = htmlClass.html2()


		if vals[6] == 1:
			print(f"{flblue}INFO : Retour HMLT 0 ...{rall}")
			htmlClass.current_html = 0
			htmlClass.resetValue()
			htmlClass.div = htmlClass.html0()







	### Page HTML 2

	elif htmlClass.current_html == 2:

		# Si l'on a selectionné 'Faire la recherche'
		if htmlClass.value['input2'] == 'Faire une recherche':

			# Changement de terme de recherche
			if vals[2] != htmlClass.value['input3']:
				htmlClass.value['input3'] = vals[2]
				htmlClass.div[2] = htmlClass.html2()[2]

			# Si on clique sur Rechercher
			if vals[5] == 1:

				# Si la recherche n'est pas vide
				if htmlClass.value['input3'] != '':
					print(f"{flblue}INFO : makeSearch {htmlClass.value['input3']} ...{rall}")
					result = htmlClass.sg.corpus.makeSearch(htmlClass.value['input3'], display=True)

					listeDiv = [html.P(result[0], style={'font-weight':'bold', 'color':'#00dd00'})]

					for rppi in result[1:]:

						subDiv = [html.P(f"Titre : {rppi[0]}", style={'font-weight':'bold'}),
								  html.P(f"Type : {rppi[1]}"),
								  dcc.Link(f"{rppi[2]}", href=f"{rppi[2]}"),
								  html.P(f"Score : {rppi[3]}")]

						listeDiv.append(html.Div(subDiv, style={'background-color':'#F7F25F'}))

					htmlClass.div[5] = html.Div(listeDiv)


		elif htmlClass.value['input2'] == 'Statistiques':

			
			# Changement de stats
			if vals[2] != htmlClass.value['input3']:

				htmlClass.value['input3'] = vals[2]
				htmlClass.value['input4'] = None
				htmlClass.value['input5'] = None

				if htmlClass.value['input3'] == 'Show first document' : htmlClass.value['input5'] = []

				htmlClass.div = htmlClass.html2()

			# Si Concorde est selectionné
			elif htmlClass.value['input3'] == 'Concorde':

				# Si on modifie Motif
				if vals[3] != htmlClass.value['input4']:
					htmlClass.value['input4'] = vals[3]
					htmlClass.div[4] = htmlClass.html2()[4]

				# Si on modifie Taille
				if vals[4] != htmlClass.value['input5']:
					htmlClass.value['input5'] = vals[4]
					htmlClass.div[5] = htmlClass.html2()[5]

				# Si on clique sur Valider
				if vals[5] == 1:
					
					# On vérifie si le motif et la taille sont bien renseignés
					if htmlClass.value['input4'] not in [None, ''] and htmlClass.value['input5'] not in [None, '']:
						print(f"{flblue}INFO : concorde {htmlClass.value['input4']} for {htmlClass.value['input5']} of context ...{rall}")
						result = htmlClass.sg.corpus.concorde(htmlClass.value['input4'], contexte=int(htmlClass.value['input5']))
						htmlClass.div[8] = html.Div([dash_table.DataTable(result.to_dict('records'), [{"name": i, "id": i} for i in result.columns], 
							id='table1', active_cell=None,
							style_cell={'textAlign': 'center'},
        					style_data_conditional=[{'if': {'column_id': 'contexte droit'}, 'textAlign': 'left'}, 
        											{'if': {'column_id': 'contexte gauche'}, 'textAlign': 'right'}]
        					)])

			# Si Stats Mots est selectionné
			elif htmlClass.value['input3'] == 'Stats Mots':

				# Si on modifie nombre
				if vals[3] != htmlClass.value['input4']:
					htmlClass.value['input4'] = vals[3]
					htmlClass.div[4] = htmlClass.html2()[4]

				# Si on clique sur Valider
				if vals[5] == 1:
					
					# On vérifie si le nombre est bien renseigné
					if htmlClass.value['input4'] not in [None, '']:
						print(f"{flblue}INFO : stats mots ({htmlClass.value['input4']}) ...{rall}")
						result = htmlClass.sg.corpus.stats(int(htmlClass.value['input4']), display=True)
						htmlClass.div[7] = html.Div([dash_table.DataTable(result.to_dict('records'), [{"name": i, "id": i} for i in result.columns], 
							id='table1', active_cell=None)])

			# Si Stats Authors est selectionné
			elif htmlClass.value['input3'] == 'Stats Authors':

				# Si on modifie nom
				if vals[3] != htmlClass.value['input4']:
					htmlClass.value['input4'] = vals[3]
					htmlClass.div[4] = htmlClass.html2()[4]

				# Si on clique sur Valider
				if vals[5] == 1:
					
					# On vérifie si le nom est bien renseigné
					if htmlClass.value['input4'] not in [None, '']:
						print(f"{flblue}INFO : stats authors with ({htmlClass.value['input4']}) ...{rall}")
						result = htmlClass.sg.corpus.statAuthor(htmlClass.value['input4'])

						if result[1] == 0:

							listeDiv = [html.P(f"Aucun resultat pour {htmlClass.value['input4']}", style = {'font-weight':'bold', 'color' : '#ff0000'})]

							if len(result[0]) > 0:

								listeDiv.append(html.P(f"Vous voulez peut-être dire :", style = {'font-weight':'bold'}))

								for name in result[0]:
									listeDiv.append(html.P(f"- {name}"))

							htmlClass.div[5] = html.Div(listeDiv, style={'background-color':'#FF8D8D'})

						else:
							htmlClass.div[5] = html.Div([html.P(f"Pour l'auteur {result[0]} :", style={'font-weight':'bold'}),
								html.P(f" - Nombre de document(s) rédigé(s) : {int(result[1])}"),
								html.P(f" - Moyenne de mots/document(s) : {int(result[2])}")],
								style = {'color' : '#00dd00', 'background-color':'#81FF8D'})

			# Si Show first documents est selectionné
			elif htmlClass.value['input3'] == 'Show first document':

				# Si on modifie nombre
				if vals[3] != htmlClass.value['input4']:
					htmlClass.value['input4'] = vals[3]
					htmlClass.div[4] = htmlClass.html2()[4]

				if vals[4] != htmlClass.value['input5']:
					htmlClass.value['input5'] = vals[4]
					htmlClass.div[5] = htmlClass.html2()[5]

				# Si on clique sur Valider
				if vals[5] == 1:
					
					# On vérifie si le nombre est bien renseigné
					if htmlClass.value['input4'] not in [None, '']:
						print(f"{flblue}INFO : show with ({htmlClass.value['input4']}) ...{rall}")
						if len(htmlClass.value['input5']) == 1 : reverse = True
						else : reverse = False
						result = htmlClass.sg.corpus.show(int(htmlClass.value['input4']), display=True, reverse=reverse)

						if len(result) <= 2:
							htmlClass.div[8] = html.P(f"Aucun documents ...", style = {'font-weight':'bold', 'color' : '#ff0000'})
						else:

							listeDiv = [html.P(result[0], style = {'font-weight':'bold'}),
									    html.P(result[1], style = {'font-weight':'bold'})]

							for res in result[2:]:

								divi = []
								for pi in res:
									if 'Source url : ' not in pi:
										divi.append(html.P(pi))
									else:
										divi.append(dcc.Link(f"{pi}", href=f"{pi[13:]}"))
										
								listeDiv.append(html.Div(divi, style={'background-color':'#E4DD10'}))

							htmlClass.div[8] = html.Div(listeDiv)
						
		elif htmlClass.value['input2'] == 'Analyse':

			# Changement d'analyse
			if vals[2] != htmlClass.value['input3'] and vals[2] not in [20, 50]:

				htmlClass.value['input3'] = vals[2]
				htmlClass.div = htmlClass.html2()

				# On choisi notre histogramme du nombre de mots / doc
				if htmlClass.value['input3'] == 'Histogram sur le nombre de mots par source':

					dico = {}

					for docu in htmlClass.sg.corpus.get_id2loc().values():
						doctype = docu.get_type().split('Document')[0]

						if doctype not in dico.keys():
							dico[doctype] = []

						dico[doctype].append(docu.get_size()[1])

					minnb = min([min(dico[key]) for key in dico.keys()])
					maxnb = max([max(dico[key]) for key in dico.keys()])
					size  = (maxnb - minnb) / 30

					fig = go.Figure()

					for key, val in dico.items():
						fig.add_trace(go.Histogram(x=val, name=key, xbins=dict(start=0, end=329, size=size)))

					fig.update_layout(barmode='overlay')
					fig.update_traces(opacity=0.75)

					htmlClass.fig = fig
					htmlClass.div[3] = html.Div([dcc.Graph(id=f"graph1")])
					htmlClass.div[4] = html.Div([])

				# On choisi l'image de mots la
				elif htmlClass.value['input3'] == 'Image Mots mdr oskour':

					htmlClass.sg.corpus.makeWCgraph()
					
					chemin = app.get_asset_url(f"image/{htmlClass.sg.corpus.get_nom()}_wordcloud.png")

					htmlClass.div[3] = html.Div([dcc.Graph(id=f"graph1")], style={'display':'none'})
					htmlClass.div[4] = html.Div([html.Img(src=chemin, style={'max-width': '100%', 'height': 'auto'})])

				else:
					print(f"{fred} WARNING : Dans l'event Analyse, l'input radio <{htmlClass.value['input3']}> non reconnu{rall}")
					print(f"HTML VALUE : ")
					for key, val in htmlClass.value.items():
						print(f"{key:7} : {val}")



		if vals[6] == 1:
			print(f"{flblue}INFO : Retour HMLT 1 ...{rall}")
			htmlClass.current_html = 1
			htmlClass.value['input2'] = ''
			htmlClass.div = htmlClass.html1()


	else:

		print(f"{fred}WARNING : htmlClass.current_html number inconnu [{htmlClass.current_html}] ...{rall}")

	return htmlClass.div, htmlClass.fig




if __name__ == "__main__":
	app.run(debug=True)