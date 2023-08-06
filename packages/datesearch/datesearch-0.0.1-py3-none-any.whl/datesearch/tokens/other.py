from datesearch.tokens.abstract_token import AbstractToken


class Other(AbstractToken):
    @staticmethod
    def its_me(chunk):
        return True

    def source_parse(self):
        return self.source

    def equal_content(self, letters):
        print(letters, self.content)
        if not letters:
            return True
        return self.content == ''.join(letters)
