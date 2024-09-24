from functools import reduce
from typing import Callable, Tuple

# fuzzbuzz через мультиметод

def multimethod (
        dispatcher: Callable [[int], Tuple [bool, bool]], 
        ops: dict [(bool, bool), Callable [[int], str | int]]):
    
    def inner (n: int):
        key = dispatcher (n)
        if key not in ops:
            raise ValueError (f"добавьте условие {key} в {ops}")

        return ops [key] (n)
    
    return inner

_fuzzbuzz = multimethod (
    dispatcher= lambda n: (n % 3 == 0, n % 5 == 0),
    ops=
    {
        (True, True)    : lambda _: "fuzzbuzz",
        (True, False)   : lambda _: "fuzz",
        (False, True)   : lambda _: "buzz",
        (False, False)  : lambda n: n 

    }                       

)

fuzzbuzz = lambda n: reduce (lambda _, elem: print (elem, end= ','), map (_fuzzbuzz, range (1, n)), None)

# каррирование

from functools import partial
import inspect

def curry (f: Callable):
    sig = inspect.signature(f)

    if not all (
        param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD) 
            and param.default is param.empty
                for param in sig.parameters.values()
        
        ): raise ValueError ("только old plain функции, никаких *, ** или defaults")               


    _curry = lambda f, n: lambda a: f (a) if n == 1 else _curry (partial (f, a), n - 1)

    return _curry (f, len (sig.parameters))



@curry
def sum_ (a: int, b: int, c: int):
    return a + b + c

# пайпы

class Pipe:
    def __init__ (self, *fns: Callable):
        self.fns = list (fns)

    def __or__ (self, fn: Callable):
        self.fns.append (fn)

        return self

    def __call__ (self, *a, **kw):
        it = iter (self.fns)
        first_fn = next (it)

        return reduce (lambda acc, fn: fn (acc), it, first_fn (*a, **kw))

piped = Pipe


if __name__ == '__main__':
    fuzzbuzz (30)

    print ()

    print (sum_ (1) (2) (3))

    from operator import add, mul

    add = curry (add)
    mul = curry (mul)

    # ака lambda x: (x + 1) * 4
    pipe_1 = Pipe() | add(1) | mul(4)
    pipe_2 = piped (add(1), mul(4))

    print (pipe_1 (5))
    print (pipe_2 (5))
