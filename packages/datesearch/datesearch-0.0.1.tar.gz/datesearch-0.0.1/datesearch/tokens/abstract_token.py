import pymorphy2


class AbstractToken:
    morph = pymorphy2.MorphAnalyzer()

    def __init__(self, piece_of_string):
        self.source = piece_of_string
        self.content = self.source_parse()

    def __repr__(self):
        name = self.__class__.__name__
        content = f'"{self.content}"' if type(self.content) is str else f'{self.content}'
        base = f'{name}({content})'
        return base

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            if self.content == other.content:
                return True
        return False

    def its_me(self):
        raise NotImplementedError()

    def source_parse(self):
        raise NotImplementedError()

    def equal_content(self):
        raise NotImplementedError()
