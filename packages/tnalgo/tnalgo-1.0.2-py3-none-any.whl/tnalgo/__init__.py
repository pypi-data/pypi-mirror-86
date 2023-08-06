__version__ = "1.0.2"

def aléa(a, b):
    from random import randint
    return randint(a, b)


def arrondi(x):
    return round(x)


def racine(x):
    return x ** 0.5


def ent(x):
    return int(x)


def long(ch):
    return ch


def pos(ch1, ch2):
    return ch2.find(ch1)


def convch(x):
    return str(x)


def estnum(ch):
    return ch.isnumeric()


def valeur(ch):
    return int(ch)


def sous_chaine(ch, d, f):
    return ch[d:f]


def effacer(ch, d, f):
    if f > d:
        return ch[:d] + ch[f:]
    return ch


def majus(ch):
    return ch.upper()