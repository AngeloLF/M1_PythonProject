from dash import Dash, dcc, html, Input, Output, callback
import classDash_serv as DashHtml

callInput = [Input(component_id="input1", component_property="value"),     # vals[0]
	  		 Input(component_id="input2", component_property="value"),     # vals[1]
	  		 Input(component_id="input3", component_property="value"),     # vals[2]
	  		 Input(component_id="radio1", component_property="value"),     # vals[3]
	  		 Input(component_id="button1", component_property="n_clicks"), # vals[4]
	  		 Input(component_id="button2", component_property="n_clicks"), # vals[5]
	  		 Input(component_id="drop1", component_property="value")]      # vals[6]
callOutput = [Output(component_id="division", component_property="children")]

htmlClass = DashHtml.htmlEvent()

app = Dash(__name__)
app.layout = html.Div([dcc.Markdown(""" # Projet PAP """, style={'textAlign': 'center'}), 
	html.Div(htmlClass.div, id='division')],
	style={'background-color': '#f0f0dd', 'padding-top':'10px', 'padding-bottom':'20px'})


@callback(*callOutput, *callInput)
def chargedMake_Event(*vals):

	print(f"\nVALS : {vals}")



	### Page HTML 0

	if htmlClass.current_html == 0:	

		# Changement de query
		if vals[0] != htmlClass.value['input1']:
			htmlClass.value['input1'] = vals[0]
			htmlClass.div[2] = htmlClass.html0()[2]


		# Changement radio button
		if vals[3] == 'Charger' and htmlClass.value['radio1'] != 'Charger' :
			htmlClass.value['radio1'] = vals[3]
			htmlClass.div[4] = htmlClass.html0()[4]

		elif vals[3] == 'Make' and htmlClass.value['radio1'] != 'Make' :
			htmlClass.value['radio1'] = vals[3]
			htmlClass.div[4] = htmlClass.html0()[4]


		# Changement nombre de documents arxiv
		if vals[1] != htmlClass.value['input2'] :
			htmlClass.value['input2'] = vals[1]
			htmlClass.div[5] = htmlClass.html0()[5]

		# Changement nombre de document reddit
		if vals[2] != htmlClass.value['input3'] : 
			htmlClass.value['input3'] = vals[2]
			htmlClass.div[6] = htmlClass.html0()[6]

		# Bouton lezgo
		if vals[4] == 1:
			if vals[0] != '':
				print('LEZGO')
				htmlClass.div = htmlClass.html1()
				htmlClass.current_html = 1
			else:
				print('Il faut que il y ai une query !')
				if len(htmlClass.div) < 12:
					htmlClass.div.append(html.P("Il faut remplir la query !", style={'color':'#ee0000'})) 



	### Page HTML 1

	elif htmlClass.current_html == 1:

		if vals[6] != htmlClass.value['drop1']:

			htmlClass.value['drop1'] = vals[6]
			htmlClass.div[2] = dcc.Dropdown(['Show first document', 'Stats Authors', 'Concorde', 'Stats Mots', 'Search !'], value=htmlClass.value['drop1'], id='drop1')

		if vals[4] == 1:
			print('VALIDER !')

		if vals[5] == 1:
			print('Retour !')
			htmlClass.div = htmlClass.html0()
			htmlClass.current_html = 0



	return htmlClass.div




if __name__ == "__main__":
	app.run(debug=True)