import numpy as np
from navec import Navec
import gensim
from scipy.spatial.distance import cosine
import pandas as pd


class PredictTopics:
    def __init__(self, docs: str, class_words: dict, topics: str, labels: list):
        self.docs = docs
        self.class_words = class_words
        self.topics = topics
        self.labels = labels

    def word_to_classes(self):
        for word, label in self.class_words.items():
            self.text = self.text.replace(word, label)
            self.docs = self.docs.replace(word, label)

    def close_doc_to_topic(self, doc, topic):
        return np.cos(doc, topic)

    def bag_of_classes(self, text):
        bag = {x: 0 for x in self.labels}
        return [bag.update({word_class: bag.get(word_class) + 1}) for word_class in text]

    def topics_to_bof(self):
        for topic in self.topics:
            self.bag_of_classes(topic)

    def doc_to_bof(self):
        for doc in self.docs:
            self.bag_of_classes(doc)


class ClosenessTermsDocs:
    def __init__(self, terms, docs):
        self.terms = terms
        self.docs = docs
        self.model = gensim.models.KeyedVectors.load_word2vec_format('model.bin', binary=True)

    def term_to_vec(self, termins):

        sentences = []
        sentence = []

        all_termins = list(termins.values())[0].copy()

        for x in all_termins:
            if x.split('_')[0] == '.':

                sentences.append(np.sum(sentence, axis=0))
                sentence = []

            else:
                if x in self.model:
                    sentence.append(self.model.word_vec(x))
        return sentences

    def doc_to_vec(self, docs):
        vec_docs = {}
        for key in docs.keys():
            all_vect = [self.model.word_vec(word) for word in docs[key] if word in self.model]
            vec_docs.update({key: np.sum(all_vect, axis=0) / len(all_vect)})
        return list(vec_docs.values())

    def closeness(self, vec1, vec2):

        cos = cosine(vec1, vec2)
        return cos

    def closeness_matrix(self, list_vec1, list_vec2):

        array = np.zeros((len(list_vec1), len(list_vec2)))
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):

                cos = self.closeness(list_vec1[i], list_vec2[j])
                if not np.isnan(cos):
                    #             cos_dist.update({i: cos})
                    array[i, j] = cos
                else:
                    array[i, j] = 2

        return array

    def write_array(self, array, index, columns, file):

        df = pd.DataFrame(data=array, columns=columns, index=index).sort_index().T.sort_index().T
        df.to_csv(file, index=False)
