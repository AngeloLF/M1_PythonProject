import xmltodict
import praw



def xmlto(dataxml):
	"""
	Permet d'enlever l'entete des document xml, car le package xmltodict, dependant de la version, à des fois un problèmes avec celle ci
	Il retourne ensuite le fichier xml transformer en dictionnaire.

	Param :
		dataxml [str] : string contenant un fichier respectant le balisage xml

	Return :
		[dict] : transformation du xml sous forme de dict
	"""

	first = dataxml[dataxml.index('<'):dataxml.index('>')+1]
	if '<?xml' in first:
		# print(first)
		dataxml = dataxml[dataxml.index('>')+1:]
	return xmltodict.parse(dataxml)





def speedTestReddit():
	"""
	Fonction rapide pour tester la connexion et le scraping sur reddit
	-> Si erreur 401 et 404 ****
	"""

	reddit = praw.Reddit(client_id='gsfJcIOUGkM8YvJdWR_jWg', 
	client_secret='bt1447AxbH2w3iEdLK5SyD8k_zM9Dg', 
	user_agent='testscrapww')

	hot_posts = reddit.subreddit('MachineLearning').hot(limit=10)
	for post in hot_posts:
		print(post.title)





