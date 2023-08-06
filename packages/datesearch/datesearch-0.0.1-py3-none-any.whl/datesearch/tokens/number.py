from datesearch.tokens.abstract_token import AbstractToken


class Number(AbstractToken):
    @classmethod
    def its_me(cls, chunk):
        chunk = cls.clean_word(chunk)
        if chunk.isdigit() or cls.get_number_from_word(chunk) is not None:
            return True
        return False

    def source_parse(self):
        word = self.clean_word(self.source)
        if word.isdigit():
            return int(word)
        return self.get_number_from_word(word)

    @classmethod
    def clean_word(cls, source):
        return ''.join([x for x in source if x.isalnum()])

    @classmethod
    def get_number_from_word(cls, word):
        all_numbers = {'ones': {
            'ноль': 0,
            'один': 1,
            'два': 2,
            'три': 3,
            'четыре': 4,
            'пять': 5,
            'шесть': 6,
            'семь': 7,
            'восемь': 8,
            'девять': 9,
        }, 'tens': {
            'десять': 10,
            'двадцать': 20,
            'тридцать': 30,
            'сорок': 40,
            'пятьдесят': 50,
            'шестьдесят': 60,
            'семьдесят': 70,
            'восемьдесят': 80,
            'девяносто': 90,
        }, 'hundreds': {
            'сто': 100,
            'двести': 200,
            'триста': 300,
            'четыреста': 400,
            'пятьсот': 500,
            'шестьсот': 600,
            'семьсот': 700,
            'восемьсот': 800,
            'девятсот': 900,
            'сотня': 100,
        }, 'other': {
            'тысяча': 100,
            'миллион': 100,
            'триллион': 100,
            'миллиард': 100,
            'гугол': 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000,
            'шестьсот': 100,
            'семьсот': 100,
            'восемьсот': 100,
            'девятсот': 100,
            'первое': 1,
            'второе': 2,
            'третье': 3,
            'четвертое': 4,
            'пятое': 5,
            'шестое': 6,
            'седьмое': 7,
            'восьмое': 8,
            'девятое': 9,
            'десятое': 10,
        }}
        normal_form = cls.get_normal_form(word)
        for group in all_numbers:
            for name in all_numbers[group]:
                if name == normal_form:
                    return all_numbers[group][name]
        return None

    @classmethod
    def get_normal_form(cls, word):
        forms = cls.morph.parse(word)
        for form in forms:
            if form.tag.POS == 'NUMR':
                return form.normal_form
        return forms[0].normal_form

    def equal_content(self, letters):
        if not letters:
            return True
        letters = ''.join(letters)
        if letters and not letters.isdigit():
            raise ValueError(f'missing content of the token in the expression')
        number = int(letters)
        return number == self.content
