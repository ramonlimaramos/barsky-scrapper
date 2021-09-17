import re


__all__ = ['ScoreAnalyzer']


KEYWORDS = {
    'experience': 10,
    'cool': 20,
    'nice': 30,
    'helped': 40,
    'great': 40,
    'happy': 50,
    'awesome': 60,
    'amazing': 60,
    'recommend': 60,
    'best': 90,
    'exceptional': 100,
    'fantastic': 100,
    'superb': 100,
}


class ScoreAnalyzer:

    def __init__(self, text, ratings):
        self._text = text
        self._rating_sum = sum(
            [v for v in ratings.values() if isinstance(v, float)])
        self._label = None
        self._value = 0
        self._set_analyzer()
        self._value = self._value + self._rating_sum

    def _set_analyzer(self):
        for k, v in KEYWORDS.items():
            self._calculate_score(k, v)

    def _calculate_score(self, x, y):
        text = self._text.lower()
        regex = r'\b{word}\b'.format(word=x)
        match = re.search(regex, text)

        if match:
            self._value = self._value + y

    @property
    def label(self):
        labels = (
            ({'from': 0, 'to': 260}, 'Neutral'),
            ({'from': 261, 'to': 320}, 'Happy'),
            ({'from': 321, 'to': 370}, 'Excited'),
            ({'from': 371, 'to': 400}, 'Amazed'),
            ({'from': 401, 'to': 99999}, 'Suspicious'),
        )

        if self._value == 0:
            return ''

        for item in labels:
            if self._value >= item[0]['from'] and self._value <= item[0]['to']:
                self._label = item[1]

        return self._label

    @property
    def value(self):
        return self._value
