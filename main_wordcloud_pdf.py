#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 11:37:26 2020

@author: jochemvankempen
"""

# based on tutorials
# https://www.datacamp.com/community/tutorials/wordcloud-python
# https://towardsdatascience.com/creating-word-clouds-with-python-f2077c8de5cc
# https://rustyonrampage.github.io/text-mining/2019/07/21/creating-wordcloud-using-python.html

import sys
sys.modules[__name__].__dict__.clear()

# Loading libraries
import numpy as np
import re # regular expression
from PIL import Image # [Python Imaging Library](https://pypi.org/project/PIL/)

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from io import StringIO

import unicodedata
from nltk.corpus import stopwords

from wordcloud import WordCloud, ImageColorGenerator

# import packages from pdfminer
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

### ---------------------------------------------------------------------- ###
### process pdf 

# import pdf as text
output_string = StringIO()
with open('data/thesis_JochemVanKempen.pdf', 'rb') as in_file:
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)

# print(output_string.getvalue())
new_string = str(output_string.getvalue())

### ---------------------------------------------------------------------- ###
### Clean up text

# Remove brackets 
re.sub('[\(\[].*?[\)\]]', ' ', new_string)

# Remove accented characters and normalise using the unicodedata library
unicodedata.normalize('NFKD', new_string).encode('ascii', 'ignore').decode('utf-8', 'ignore')

# Remove special characters and numbers 
pattern = r'[^a-zA-Z\s]' 
re.sub(pattern, ' ', new_string)

# make lower case
new_string.lower()

# Remove stop words
stopword_list = stopwords.words('english')    
stopword_list.extend(['et', 'al', 'doi', 
                      'figure', 'Figure', 'chapter',
                      'and','well','thus','first','also',
                      'nat','neurosci','JNEUROSCI','Sci','Science',
                      'one','two','although',
                      'Thiele','Aston','Jones','Cohen','Arnsten','Bellgrove','Connell',
                      'non','within',
                      'single','Additionally'])
print(stopword_list)

### ---------------------------------------------------------------------- ###
### import brain image
mask_brain = np.array(Image.open("Img/brain_blackw.png"))    
# mask_brain[mask_brain==0]=255

# image_colors = ImageColorGenerator(mask_brain) # if you want to plot the words in colour of the mask, use this line
plt.imshow(mask_brain)
plt.axis("off")
plt.show()

wc = WordCloud(stopwords = stopword_list, 
               background_color = "black",                         
               mask = mask_brain, 
               collocations = False,
               max_words=200, width = 1600, height = 900, 
               random_state=1).generate(new_string)

# print(*wc.words_, sep = "\n")

# truncate colormap
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=-1):
    if n == -1:
        n = cmap.N
        
    new_cmap = mcolors.LinearSegmentedColormap.from_list(
         'trunc({name},{a:.2f},{b:.2f})'.format(name=cmap.name, a=minval, b=maxval),
         cmap(np.linspace(minval, maxval, n)))
    
    return new_cmap

minColor = 0.5
maxColor = 1.00

cmap2use = "cool_r"
cmap2use = "bone"
cmap_t = truncate_colormap(plt.get_cmap(cmap2use), minColor, maxColor)



# to recolour the image
# wc = WordCloud(background_color="white", max_words=200, width=400, height=400, mask=mask_brain, random_state=1).generate(new_string)

# to recolour the image
# plt.imshow(wc, interpolation ='bilinear') # Using the color function here
# plt.imshow(wc.recolor(color_func=image_colors), interpolation ='bilinear') # Using the color function here
plt.imshow( wc.recolor(colormap = cmap_t, random_state = 1), alpha = 1 , interpolation='bilinear')
plt.axis("off")
# plt.savefig("thesis_wordmap.svg")


wc.to_file("thesis_wordmap_" + cmap2use +".png")
