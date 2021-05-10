import collections
import nltk
from typing import Callable
from pymorphy2 import MorphAnalyzer
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
import multiprocessing
import numpy as np
import os
import io
from razdel import sentenize, tokenize
from navec import Navec
from slovnet import Morph
import itertools


class PrepareText:
    def __init__(self, text: dict, model: Callable = MorphAnalyzer().parse):
        self.text = text
        self.lemmatizer = model
        self.word_dict = dict()
        self.space_chars: str = u'«»“”’*©…/_(),\\'
        self.tokens_part = dict()

    # def post_to_corpus_line(self, text_part: str):
    #     words = collections.Counter()
    #     # content_text = self._delete_space_charts(self.text[text_part])
    #     # tokens = nltk.tokenize.wordpunct_tokenize(content_text)
    #     chunk = []
    #     tokens = []
    #
    #     for sent in sentenize(self.text[text_part]):
    #         tokens = [_.text for _ in tokenize(sent.text)]
    #         chunk.append(tokens)
    #     # tokens = nltk.word_tokenize(content_text)
    #     navec = Navec.load('navec_news_v1_1B_250K_300d_100q.tar')
    #     morph = Morph.load('slovnet_morph_news_v1.tar', batch_size=4)
    #     morph.navec(navec)
    #
    #     markup = morph.map(chunk)
    #
    #     for sentence in markup:
    #         for token in sentence:
    #             tokens.append(f'{self._preprocess_token(token.text)}_{token.pos}')
    #     # for number, token in enumerate(tokens):
    #     #     if len(token) > 2:
    #     #         token = token.lower().replace(u'ё', u'е')
    #     #         word = self.lemmatizer(token)[0].normal_form
    #     #         tokens[number] = word
    #     #         if len(word) > 0:
    #     #             words[word] += 1
    #
    #     # self.word_dict.update({text_part: words})
    #     self.tokens_part.update({text_part: tokens})

    def post_to_corpus_line(self, text_part: str):
        new_tokens = []
        text = self.text[text_part].replace('\n', '.').replace('U.S.', 'US')
        chunk = []
        for sent in sentenize(text):
            tokens = [self._preprocess_token(_.text) for _ in tokenize(sent.text)]
            chunk.append(tokens)

        navec = Navec.load('navec_news_v1_1B_250K_300d_100q.tar')
        morph = Morph.load('slovnet_morph_news_v1.tar', batch_size=4)
        morph.navec(navec)

        markup = morph.map(chunk)
        for sentence in markup:
            for token in sentence.tokens:
                add = f'{token.text}_{token.pos}'
                new_tokens.append(add)

        self.tokens_part.update({text_part: new_tokens})

    def _delete_space_charts(self, content_text):
        # content_text = ''.join(text_parts)

        for c in self.space_chars:
            content_text = content_text.replace(c, ' ')

        return content_text

    def _preprocess_token(self, token):
        # if len(token) > 2:
        token = token.lower().replace(u'ё', u'е').strip()
        token = self.lemmatizer(token)[0].normal_form
        return token

    def prepare_text(self):
        for text_part in self.text.keys():
            self.post_to_corpus_line(text_part)

    def create_str_sentences(self, bag_of_words: list):
        end_sentences = [number for number, word in enumerate(bag_of_words) if word == '.']

        for x in end_sentences:
            bag_of_words[x] = '\n'

        sentence = ' '.join(bag_of_words)
        # sentence = sentence.replace('.', '\n')
        return sentence
    

class TextVectorize:
    def __init__(self, text, vector_model):
        self.text = text
        self.model = vector_model

    def vectorize(self):
        model = Word2Vec(sentences=common_texts, size=100, window=5, min_count=1, workers=multiprocessing.cpu_count())
        model.train([["hello", "world"]], total_examples=1, epochs=1)


class TextToWord2Vec:
    '''
    Wrapper for accessing Stanford Tree Bank Dataset
    https://nlp.stanford.edu/sentiment/treebank.html

    Parses dataset, gives each token and index and provides lookups
    from string token to index and back

    Allows to generate random context with sampling strategy described in
    word2vec paper:
    https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf
    '''

    def __init__(self):
        self.index_by_token = {}
        self.token_by_index = []

        self.sentences = []

        self.token_freq = {}

        self.token_reject_by_index = None

    def load_dataset(self, folder_text, text_type='folder'):

        filename = os.path.join(folder_text, "ready.txt")
        if text_type == "str":
            f = io.StringIO(folder_text)
        elif text_type == 'folder':
            f = open(filename, "r", encoding="utf-8")

        for l in f:
            splitted_line = l.strip(' ').split()
            words = [w.lower() for w in splitted_line[1:]]  # First one is a number

            self.sentences.append(words)
            for word in words:
                if word in self.token_freq:
                    self.token_freq[word] += 1
                else:
                    index = len(self.token_by_index)
                    self.token_freq[word] = 1
                    self.index_by_token[word] = index
                    self.token_by_index.append(word)
        f.close()
        self.compute_token_prob()

    def compute_token_prob(self):
        words_count = np.array([self.token_freq[token] for token in self.token_by_index])
        words_freq = words_count / np.sum(words_count)

        # Following sampling strategy from word2vec paper:
        # https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf
        self.token_reject_by_index = 1 - np.sqrt(1e-5 / words_freq)

    def check_reject(self, word):
        return np.random.rand() > self.token_reject_by_index[self.index_by_token[word]]

    def get_random_context(self, context_length=5):
        """
        Returns tuple of center word and list of context words
        """
        sentence_sampled = []
        while len(sentence_sampled) <= 2:
            sentence_index = np.random.randint(len(self.sentences))
            sentence = self.sentences[sentence_index]
            sentence_sampled = [word for word in sentence if self.check_reject(word)]

        center_word_index = np.random.randint(len(sentence_sampled))

        words_before = sentence_sampled[max(center_word_index - context_length // 2, 0):center_word_index]
        words_after = sentence_sampled[center_word_index + 1: center_word_index + 1 + context_length // 2]

        return sentence_sampled[center_word_index], words_before + words_after

    def num_tokens(self):
        return len(self.token_by_index)

