import ipywidgets as widgets
from IPython.display import display, HTML

def UXCHOICE(sgi):
	def on_button0_clicked(b):
		with output0:
			if check.value == 'Charger les données':
				sgi.charged(query.value)
			else:
				sgi.scrap(query.value, arxiv=NBarxiv.value, reddit=NBreddit.value)
				sgi.save()
				sgi.charged(query.value)
			UXCHOICE_NEXT(sgi)

	button0 = widgets.Button(description="Lezgongue")
	output0 = widgets.Output()
	button0.on_click(on_button0_clicked)

	check = widgets.RadioButtons(options=['Charger les données', 'Faire la recherche, save et charger'], value='Charger les données', description='Option :', disabled=False)
	query = widgets.Text(value='astrophysics', placeholder='Type something', description='Query :', disabled=False)
	NBarxiv = widgets.IntSlider(value=10, min=0, max=500, step=1, description='D\'Arxiv :', disabled=False, continuous_update=False, orientation='horizontal', readout=True, readout_format='d')
	NBreddit = widgets.IntSlider(value=10, min=0, max=500, step=1, description='De Reddit :', disabled=False, continuous_update=False, orientation='horizontal', readout=True, readout_format='d')

	display(check)
	display(query)
	display(NBarxiv)
	display(NBreddit)
	display(button0, output0)



def UXCHOICE_NEXT(sgi):
	def on_button1_clicked(b):
		with output1:
			if drop.value == 'show':
				UXCHOICE_NEXT_show(sgi)
			elif drop.value == 'statsAuthor':
				UXCHOICE_NEXT_author(sgi)
			elif drop.value == 'concorde':
				UXCHOICE_NEXT_concorde(sgi)
			elif drop.value == 'stats':
				UXCHOICE_NEXT_stats(sgi)
			elif drop.value == 'Search !':
				UXCHOICE_NEXT_Search(sgi)

	button1 = widgets.Button(description="Lezgongue")
	output1 = widgets.Output()
	button1.on_click(on_button1_clicked)

	drop = widgets.Dropdown(options=['show', 'statsAuthor', 'concorde', 'stats', 'Search !'], value='Search !', description='Function :', disabled=False)

	display(drop)
	display(button1, output1)



def UXCHOICE_NEXT_show(sgi):
	def on_button1bis_clicked(b):
		with output1bis:
			sgi.corpus.show(WGshow.value)
			UXCHOICE_NEXT(sgi)

	button1bis = widgets.Button(description="Show !")
	output1bis = widgets.Output()
	button1bis.on_click(on_button1bis_clicked)

	WGshow = widgets.IntText(value=10, min=1, max=sgi.corpus.get_ndoc(), description='Nombre de document à show : ', disabled=False)

	display(WGshow)
	display(button1bis, output1bis)



def UXCHOICE_NEXT_author(sgi):
	def on_button1bis_clicked(b):
		with output1bis:
			sgi.corpus.statAuthor(WGauthor.value)
			UXCHOICE_NEXT(sgi)

	button1bis = widgets.Button(description="Les stats !")
	output1bis = widgets.Output()
	button1bis.on_click(on_button1bis_clicked)

	WGauthor = widgets.Text(value='', placeholder='Nom de l\'auteur', description='Nom de l\'auteur :', disabled=False)

	display(WGauthor)
	display(button1bis, output1bis)



def UXCHOICE_NEXT_concorde(sgi):
	def on_button1bis_clicked(b):
		with output1bis:
			df = sgi.corpus.concorde(WGmotif.value, WGconcorde.value).style.set_properties(subset=['contexte droit'], **{'text-align': 'left'})
			display(df)
			UXCHOICE_NEXT(sgi)

	button1bis = widgets.Button(description="Concorde !")
	output1bis = widgets.Output()
	button1bis.on_click(on_button1bis_clicked)

	WGconcorde = widgets.IntText(value=10, min=10, max=50, description='Nombre du contexte :', disabled=False)
	WGmotif    = widgets.Text(value='', placeholder='Motif', description='Motif :', disabled=False)

	display(WGconcorde)
	display(WGmotif)
	display(button1bis, output1bis)



def UXCHOICE_NEXT_stats(sgi):
	def on_button1bis_clicked(b):
		with output1bis:
			df = sgi.corpus.stats(WGstats.value, display=True).style
			display(df)
			UXCHOICE_NEXT(sgi)

	button1bis = widgets.Button(description="Les stats !")
	output1bis = widgets.Output()
	button1bis.on_click(on_button1bis_clicked)

	WGstats = widgets.IntText(value=5, min=5, max=50, description='Nombre de mots les plus freq. :', disabled=False)

	display(WGstats)
	display(button1bis, output1bis)



def UXCHOICE_NEXT_Search(sgi):
	def on_button1bis_clicked(b):
		with output1bis:
			df = sgi.corpus.makeSearch(WGSearch.value, display=True)
			display(df)
			UXCHOICE_NEXT(sgi)

	button1bis = widgets.Button(description="Search !")
	output1bis = widgets.Output()
	button1bis.on_click(on_button1bis_clicked)

	WGSearch = widgets.Text(value='', placeholder='...', description='Search !', disabled=False)

	display(WGSearch)
	display(button1bis, output1bis)