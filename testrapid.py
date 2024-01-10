from ScrapingGeneral import ScrapingGeneral
import os
from color_console.coloramaALF import *


sg = ScrapingGeneral()
kwkw = sg.scrap('astrophysics', arxiv=5, reddit=5, wiki=5)




print(kwkw)