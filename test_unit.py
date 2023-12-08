from class_PAP import scrapingGeneral
from time import sleep

suc, rat = 0, 0


print("Test : creation scraption"); sleep(1)
try:
	sg = scrapingGeneral()
	print("OK\n")
	suc += 1
except:
	print("PROBLEMES\n")
	rat += 1
sleep(1)


print("Test : methode scrap"); sleep(1)
try:
	sg.scrap('astrophysics', arxiv=20, reddit=20)
	print("OK\n")
	suc += 1
except:
	print("PROBLEMES\n")
	rat += 1
sleep(1)


print("Test : methode save"); sleep(1)
try:
	sg.save()
	print("OK\n")
	suc += 1
except:
	print("PROBLEMES\n")
	rat += 1
sleep(1)


print("Test : methode charged"); sleep(1)
try:
	sg.charged('astrophysics')
	print("OK\n")
	suc += 1
except:
	print("PROBLEMES\n")
	rat += 1
sleep(1)


print("Test : affiche un element de corpus, dans id2loc (il faut au moins 11 element)"); sleep(1)
try:
	sg.corpus.get_id2loc()['id11'].info()
	print("OK\n")
	suc += 1
except:
	print("PROBLEMES\n")
	rat += 1
sleep(1)


print("Test : method show(nbShow=10) de corpus"); sleep(1)
try:
	sg.corpus.show(20)
	print("OK\n")
	suc += 1
except:
	print("PROBLEMES\n")
	rat += 1
sleep(1)


print("Test : attribut allInOne"); sleep(1)
try:
	print(sg.corpus.get_allInOne())
	print("OK\n")
	suc += 1
except:
	print("PROBLEMES\n")
	rat += 1
sleep(1)


print("Test : method statAuthor"); sleep(1)
try:
	sg.corpus.statAuthor('S. Mendoza')
	print("OK\n")
	suc += 1
except:
	print("PROBLEMES\n")
	rat += 1
sleep(1)


print(f"Test reussite : {suc/(suc+rat)*100:2f}% ({suc}/{suc+rat})")