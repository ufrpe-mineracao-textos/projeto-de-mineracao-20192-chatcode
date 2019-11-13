from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 16:27:28 2019

@author: c.rodrigues.da.silva
"""
class ChatterBot(object):
    
    def __init__(self):
        self.chatbot_corpus = chatbot_corpus = ChatBot(
            'Bob',
            preprocessors=[
                'chatterbot.preprocessors.clean_whitespace', # remove whitespaces consecutivos
                'chatterbot.preprocessors.convert_to_ascii'  # converte de unicode para ascii
            ],
            logic_adapters=[
                "chatterbot.logic.BestMatch"
            ]
        )
        self.trainer = ChatterBotCorpusTrainer(chatbot_corpus)
        self.trainer.train(
            'chatterbot.corpus.portuguese'
        )
    
    def chatter_response(self, user_input):
        chatter_response = self.chatbot_corpus.get_response(user_input)
        return chatter_response.text
