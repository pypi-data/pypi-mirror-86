import pymorphy2
from datesearch.tokens import Dilimiter, Period, Number, Other, Punctuation


class Tokenizator:
    def __init__(self, source_string):
        self.morph = pymorphy2.MorphAnalyzer()
        self.token_classes = [Dilimiter, Period, Number, Punctuation, Other]
        self.source = source_string
        self.splitted_source_tokens = self.source.replace('\n', ' ').lower().split()
        self.tokens = self.get_tokens()

    def get_tokens(self):
        tokens = []
        for element in self.splitted_source_tokens:
            token = self.get_token(element)
            tokens.append(token)
        return tokens

    def get_token(self, element):
        for Class in self.token_classes:
            if Class.its_me(element):
                return Class(element)
