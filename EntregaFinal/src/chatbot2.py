#import necessary libraries
import random
import string  # to process standard python strings
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import nltk
from nltk.stem import WordNetLemmatizer
import os.path

nltk.download('popular', quiet=True) # for downloading packages
warnings.filterwarnings('ignore')
nlp = spacy.load('en')


class ChatterBot(object):
    # Keyword Matching
    GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
    GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]

    def __init__(self):
        self.sent_tokens = nltk.sent_tokenize('')
        self.word_tokens = nltk.word_tokenize('')
        self.train_bot()
        # Preprocessing
        self.lemmer = WordNetLemmatizer()

    def train_bot(self):
        # uncomment the following only the first time
        nltk.download('punkt')  # first-time use only
        nltk.download('wordnet')  # first-time use only

        path = 'dataset/'
        for f in os.listdir(path) :
            if os.path.isfile(os.path.join(path, f)):
                print(f.title())
                with open(path + f.title(), 'r', encoding='utf8', errors='ignore') as fin:
                    raw = fin.read().lower()

                # TOkenisation
                self.sent_tokens = self.sent_tokens + nltk.sent_tokenize(raw)  # converts to list of sentences
                self.word_tokens = self.word_tokens + nltk.word_tokenize(raw)  # converts to list of words

    def lem_tokens(self, tokens):
        return [self.lemmer.lemmatize(token) for token in tokens]

    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    remove_punct_dict[ord('¶')] = None

    def lem_normalize(self, text):
        return self.lem_tokens(nltk.word_tokenize(text.lower().translate(self.remove_punct_dict)))

    def greeting(self,sentence):
        """If user's input is a greeting, return a greeting response"""
        for word in sentence:
            if word.lower_ in self.GREETING_INPUTS:
                return random.choice(self.GREETING_RESPONSES)

    # Generating response
    def response(self, user_response):
        robo_response = ''
        self.sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=self.lem_normalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if (req_tfidf == 0):
            robo_response = robo_response + "I am sorry! I don't understand you"
            return robo_response
        else:
            robo_response = robo_response + self.sent_tokens[idx]
            return robo_response

    def check_is_phrase_only_greetings_thanks_or_bye(self,word, phrase, x):
        is_greeting = word.lower_ in self.GREETING_INPUTS
        is_thanks_1 = word.lower_ == 'thanks'
        if x+1 < len(phrase):
            is_thanks_2 = phrase[x + 1].lower_ == 'you' and word.lower_ == 'thank' or \
                          phrase[x].lower_ == 'you' and phrase[x-1].lower_ == 'thank'
        else:
            is_thanks_2 = phrase[x].lower_ == 'you' and phrase[x-1].lower_ == 'thank'
        is_bye = word.lower_ == 'bye'

        return is_greeting or is_bye or is_thanks_1 or is_thanks_2

    def chatter_response(self, user_response):
        user_response = user_response.lower()
        print(user_response)
        translator = str.maketrans('', '', string.punctuation)
        print(user_response.translate(translator))
        phrase = nlp(user_response.translate(translator))
        print([token.pos_ for token in phrase])
        bot_response = ''
        is_phrase_only_greetings_thanks_or_bye = all(self.check_is_phrase_only_greetings_thanks_or_bye(word, phrase, x)
                                                     for x, word in enumerate(phrase))

        if self.greeting(phrase):
            bot_response = bot_response + '\n' + self.greeting(phrase)

        if not is_phrase_only_greetings_thanks_or_bye:
            bot_response = bot_response + '\n' + self.response(user_response)
            self.sent_tokens.remove(user_response)

        if 'thanks' in [word.lower_ for word in phrase] or \
                True in [word.lower_ == 'thank' and phrase[x+1].lower_ == 'you' for x, word in enumerate(phrase)]:
            bot_response = bot_response + '\n' + "You are welcome.."
        if 'bye' in [word.lower_ for word in phrase]:
            bot_response = bot_response +'\n'+ "Bye! take care.."

        return bot_response
