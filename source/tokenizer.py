import re
import string

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from spacy.lang.en import English


class Tokenizer(object):

    def __init__(self,
                 remove_stop_words=True,
                 lemmatize=False,
                 min_word_length=1,
                 strip_punctuation=True,
                 remove_numbers=True,
                 strip_html=True):
        self.remove_stop_words = remove_stop_words
        self.lemmatize = lemmatize
        self.min_word_length = min_word_length
        self.strip_punctuation = strip_punctuation
        self.remove_numbers = remove_numbers
        self.strip_html = strip_html

        self.html_regex = re.compile('<.*?>')

        # Punctuation: do not include characters .,!-?
        self.punct = string.punctuation.replace('.', '').replace(',', '').\
            replace('!', '').replace('-', '').replace('?', '')

        # Load Spacy English tokenizer
        # TODO: Classify language and use language-specific tokenizer
        self.parser = English()

    def _conditions(self, word):
        return (len(word.orth_.strip()) >= self.min_word_length) and \
               (not word.is_punct) and \
               (not (self.remove_stop_words and word.is_stop)) and \
               (not (self.remove_numbers and word.is_digit))

    def __call__(self, doc):

        if self.strip_html:
            # Remove all HTML tags
            doc = re.sub(self.html_regex, ' ', doc)

        if self.strip_punctuation:
            doc = doc.translate({ord(char): None for char in self.punct})

        tokens = [(word.lemma_.lower().strip() if self.lemmatize else
                   word.orth_.lower().strip())
                  for word in self.parser(doc) if self._conditions(word)]

        return tokens


def get_token_counts(column, ngrams=1):
    '''
    Get total token counts from a column of strings using the default
    tokenizer.

    :param column: Series of strings
    :return: df of token counts by product
    '''
    tokenizer = Tokenizer()

    cv = CountVectorizer(tokenizer=tokenizer,
                         ngram_range=(ngrams, ngrams))

    # fit vectorizer:
    cv.fit(column.astype(str))
    # transform to count matrix:
    count_vectors = cv.transform(column.astype(str))
    # get all token names:
    token_names = cv.get_feature_names()

    df_bow = pd.DataFrame(count_vectors.todense(),
                          index=column.index,
                          columns=token_names)

    return df_bow
