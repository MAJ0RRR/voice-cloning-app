from enum import Enum


class Gender(Enum):
    man = 1
    woman = 2


class Language(Enum):
    polish = 1
    english = 2

class Options(Enum):
    train = 1
    synthesize_speech = 2
