from datesearch.tokenizator import Tokenizator
from datesearch.tokens import Dilimiter, Period, Number, Other, Punctuation


class ExpressionItem:
    token_classes = {
        'd': Dilimiter,
        'e': Period,
        'n': Number,
        'P': Punctuation,
        'o': Other,
    }

    def __init__(self, letter, args):
        if letter is None:
            raise ValueError('expression is invalid')
        if letter not in self.token_classes:
            raise ValueError('invalid token code')
        self.letter = letter
        self.args = args

    def __repr__(self):
        return f'ExpressionItem("{self.letter}", {self.args})'

    def __eq__(self, other):
        expected_class = self.token_classes[self.letter]
        if type(other) is expected_class:
            if other.equal_content(self.args):
                return True
        return False



class Search:
    token_classes = {
        'd': Dilimiter,
        'e': Period,
        'n': Number,
        'P': Punctuation,
        'o': Other,
    }

    def __call__(self, text, expression):
        tokens = Tokenizator(text).tokens
        expression = self.parse_expression(expression)
        return self.prove(tokens, expression)


    def parse_expression(self, expression):
        flag = False
        args = []
        current_letter = None
        result = []
        for letter in expression:
            if letter == '[':
                if args:
                    raise ValueError('expression is invalid')
                args = []
                flag = True
            elif letter == ']':
                flag = False
                item = ExpressionItem(current_letter, args)
                result.append(item)
                current_letter = None
                args = []
            else:
                if flag:
                    args.append(letter)
                else:
                    args = []
                    if current_letter is not None:
                        item = ExpressionItem(current_letter, args)
                        result.append(item)
                    current_letter = letter
        if current_letter is not None:
            if args:
                raise ValueError('expression is invalid')
            item = ExpressionItem(current_letter, args)
            result.append(item)
        return result

    def prove(self, tokens, expression):
        current_item = 0
        result = []
        for token in tokens:
            item = expression[current_item]
            if item == token:
                current_item += 1
                result.append(token)
                if current_item == len(expression):
                    return result
            else:
                current_item = 0
                result = []
        return None


search = Search()
