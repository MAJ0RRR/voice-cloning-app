from enum import Enum


class Gender(Enum):
    man = 1
    woman = 2


class Language(Enum):
    polish = 1
    english = 2


class Options(Enum):
    train_old = 1
    train_new = 2
    synthesize_speech = 3
    generate_samples = 4
    retrain = 5
