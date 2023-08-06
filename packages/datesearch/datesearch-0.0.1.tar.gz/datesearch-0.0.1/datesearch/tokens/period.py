from datesearch.tokens.abstract_token import AbstractToken


class Period(AbstractToken):
    """
    's' - секунда
    'm' - минута
    'h' - час
    'd' - день
    'w' - неделя
    'M' - месяц
    'N' - именованный месяц
    'q' - квартал
    'Y' - год
    'C' - век, столетие
    """
    allowed_periods = {
        'секунда': 's',
        'минута': 'm',
        'час': 'h',
        'месяц': 'M',
        'год': 'Y',
        'столетие': 'C',
        'квартал': 'q',
        'неделя': 'w',
        'день': 'd',
        'век': 'C',
    }
    allowed_months = {
        'январь': 'N',
        'февраль': 'N',
        'март': 'N',
        'апрель': 'N',
        'май': 'N',
        'июнь': 'N',
        'июль': 'N',
        'август': 'N',
        'сентябрь': 'N',
        'октябрь': 'N',
        'ноябрь': 'N',
        'декабрь': 'N',
    }

    @classmethod
    def its_me(cls, chunk):
        normal_form = cls.morph.parse(cls.clean_word(chunk))[0].normal_form
        if normal_form in cls.allowed_periods or normal_form in cls.allowed_months:
            return True
        return False

    def source_parse(self):
        normal_form = self.morph.parse(self.clean_word(self.source))[0].normal_form
        if normal_form in self.allowed_periods:
            pers = self.allowed_periods
        elif normal_form in self.allowed_months:
            pers = self.allowed_months
        return pers[normal_form]

    @classmethod
    def clean_word(cls, source):
        return ''.join([x for x in source if x.isalnum()])

    def equal_content(self, letters):
        if not letters:
            return True
        return self.content in letters
