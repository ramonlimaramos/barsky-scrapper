from functools import reduce
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
    
    def __init__(self, text):
        self._text = text
        self._label = ''
        self._value = 0
        self._set_analyzer()

    def _set_analyzer(self):
        for k, v in KEYWORDS.items():
            self._calculate_score(k, v)
        self._set_label()
        
    
    def _calculate_score(self, x, y):
        text = self._text.lower()
        regex = r'\b{word}\b'.format(word=x)
        match = re.search(regex, text)
        
        if match:
            self._value = self._value + y


    def _set_label(self):
        pass

    @property
    def label(self):
        return self._label
    
    @property
    def value(self):
        return self._value