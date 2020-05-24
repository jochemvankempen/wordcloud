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

# Start with loading all necessary libraries
import numpy as np
# import pandas as pd
import re
from PIL import Image

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from io import StringIO

import unicodedata
# import nltk
from nltk.corpus import stopwords

#from wordcloud import WordCloud, ImageColorGenerator
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

print(output_string.getvalue())

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
char_mask = np.array(Image.open("Img/brain_blackw.png"))    
# char_mask[char_mask==0]=255

# def transform_format(val):
#     if val == 0:
#         return 255
#     else:
#         return val

# transformed_char_mask = np.ndarray((char_mask.shape[0],char_mask.shape[1]), np.int32)

# for i in range(len(char_mask)):
#     transformed_char_mask[i] = list(map(transformed_char_mask, char_mask[i]))


def grey_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    return("hsl(230,100%%, %d%%)" % np.random.randint(49,51))

image_colors = ImageColorGenerator(char_mask)
plt.imshow(char_mask)
plt.axis("off")
plt.show()

wc = WordCloud(stopwords = stopword_list, 
               background_color = "black",                         
               mask=char_mask, 
               collocations=False,
               max_words=200, width = 1600, height = 900, 
               random_state=1).generate(new_string)

print(*wc.words_, sep = "\n")

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
inferno_t = truncate_colormap(plt.get_cmap(cmap2use), minColor, maxColor)



# to recolour the image
# wc = WordCloud(background_color="white", max_words=200, width=400, height=400, mask=char_mask, random_state=1).generate(new_string)

# to recolour the image
# plt.imshow(wc, interpolation ='bilinear') # Using the color function here
# plt.imshow(wc.recolor(color_func=image_colors), interpolation ='bilinear') # Using the color function here
plt.imshow( wc.recolor(colormap = inferno_t, random_state = 1), alpha = 1 , interpolation='bilinear')
plt.axis("off")
# plt.savefig("thesis_wordmap.svg")


wc.to_file("thesis_wordmap_" + cmap2use +".png")
