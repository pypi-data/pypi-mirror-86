from pdb import set_trace as st
from gensim.models import KeyedVectors
import numpy as np
import re
import numpy as np


def string_found(string1, string2):
   s = re.search(r"\b" + re.escape(string1) + r"\b", string2)
   if s:
       return s.start()
   return False

import math
def sigmoid_punishment(x):
  return 2 / (1 + math.exp(-x*5))


def print_info(ret):
    keys = ret[1].keys()
    for key in sorted(keys):
        print(key)
        print(ret[1][key])
        print('=' * 20)
    print('-'*30)
    
class Finder:
    def __init__(self, model_path, binary = True):
        self.model = KeyedVectors.load_word2vec_format(model_path, binary = binary)

    def __find_whole_word(self, substring, phrase):
        s = re.search(r"\b" + re.escape(substring) + r"\b", phrase)
        if s:
            return s.start()
        return False

    def __build(self, query):
        words_expanded = []
        for word in query.split(' '):
            if len(word) <= 2:
                continue
            words_bag = []

            counter = 0
            offset = 0
            similar_words = [word]
            while counter < 20:
                counter += 1
                similar_words_list = []
                try:
                    similar_words_list = self.model.most_similar(word, topn = counter + offset)
                except KeyError:
                    continue
                found_new = False
                for similar_word_and_dist in similar_words_list:
                    similar_word = similar_word_and_dist[0]

                    similar_word_already_superset_of_a_word = False
                    for similar_word_existing in similar_words:
                        if similar_word.find(similar_word_existing) > -1:
                            similar_word_already_superset_of_a_word = True
                            break
                        else:
                            pass  # print(similar_word_existing, similar_word)

                    if not similar_word_already_superset_of_a_word:
                        if similar_word not in similar_words:
                            find_new = True
                            similar_words.append(similar_word)

                if not found_new:
                    offset += 5

            for similar_word_and_vec in similar_words:
                words_bag.append(similar_word_and_vec)
            words_expanded.append(words_bag)
        return words_expanded

    def __get_best_match(self, sentences, words_expanded):
        max_score = 0.0
        max_score_line = None
        # print(words_expanded)

        matches = dict()

        for my_phrase in sentences:
            indices = []
            phrase = my_phrase.lower()
            score = 0.0
            words_matched = []
            for words_bag in words_expanded:
                for word in words_bag:
                    s= self.__find_whole_word(word, phrase)
                    if s:
                        indices.append(s)
                        score += 2*round(np.linalg.norm(self.model[word]), 2)
                        phrase = phrase.replace(word, '*%s*' % word)
                        words_matched.append(word)
                        break

                    if len(word) <= 3:
                        continue
                    s = phrase.find(word)
                    if s > -1:
                        indices.append(s)
                        score += round(np.linalg.norm(self.model[word]), 2)
                        words_matched.append(word)


                        phrase = phrase.replace(word, '*%s*' % word)
                        # print('possible line: ', line)
                        # print('word', word)
                        # print('')
                        break

            #if indices found are too far away then score should be punished

            indices = [index / len(phrase) for index in indices]

            #deberia dividir el score por un numero entre 1 y len(words_matched)
            var = np.var(indices)
            if var > 0:
                #st()
                score /= sigmoid_punishment(var)

            if score > max_score:
                if score in matches:
                    matches[score].append(phrase)
                else:
                    matches[score] = [phrase]


            if score > max_score:
                max_score = score
                max_score_phrase = phrase

        return max_score_phrase, matches


    def find(self, query, sentences, debug=False):
        words_expanded = self.__build(query)
        max_score_phrase = self.__get_best_match(sentences, words_expanded)
        return max_score_phrase