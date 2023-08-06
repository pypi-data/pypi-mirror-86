from engpy.tools.math.core import log
from engpy.tools.math.trigs import trig
from engpy.errors.exceptions import UnacceptableToken
from engpy.misc.miscs import lexpr
from .gen import getter


def toClass(expr, hkeys=''):
    if 'log' in expr or 'ln' in expr:
        return log(expr, hkeys=hkeys)
    elif 'sin' in expr or 'sec' in expr or 'cos' in expr or 'cosec' in expr or 'tan' in expr or 'cot' in expr:
        return trig(expr, hkeys=hkeys)


def cross(cls, _cls):
    if getter(cls, 'name') == 'Expr':
        return cls
    elif getter(cls, 'name') == 'Fraction':
        return _cls({1: [{cls: 1}]})
    elif getter(cls, 'name') == 'Vector':
        return _cls(cls.vec)
    else:
        new = []
        for struct in cls.struct:
            for coeff, var in struct.expr.items():
                new.append(_cls({coeff: [{cls.recreate({1: var}): 1}]}))
        return sum(new)


def Mul(_list):
    if not isinstance(_list, (list, tuple)):
        raise UnacceptableToken(f'parameter must be a list object not {type(_list)}')
    mul_ = lexpr(1)
    for items in _list:
        mul_ *= items
    return mul_
