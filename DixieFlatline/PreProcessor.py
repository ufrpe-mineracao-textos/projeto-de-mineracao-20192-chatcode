import pandas as pd
import numpy as np
import tensorflow as tf
import re
import time

lines = open('cornell movie-dialogs corpus\movie_lines.txt', encoding='utf-8', errors='ignore').read().split('\n')
conv_lines = open('cornell movie-dialogs corpus\movie_conversations.txt', encoding='utf-8', errors='ignore').read().split('\n')

# creating a line dictionary, with index to each line
line_dict = {}
for line in lines:
    _line = line.split(' +++$+++ ')
    if len(_line) == 5:
        line_dict[_line[0]] = _line[4]
        
conversations = [ ]
for line in conv_lines[:-1]:
    _line = line.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","")
    conversations.append(_line.split(','))
    
print(conversations[:10])

conversations = conversations[473:865]

convs_text = []

for conv in conversations:
    text_lines = []
    for i in range(len(conv)):
        _line = line_dict[conv[i]]
        if _line != 'CONTINUED':
            text_lines.append(_line)       
    convs_text.append(text_lines)
    
print(convs_text[:10])

textFile = open("conversationsLines.txt", "w")

for conv in convs_text:
    for line in conv:
        textFile.write(line + "\n")

textFile.close()