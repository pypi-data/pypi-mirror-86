# generates .n and .s on 'get'

import math

class fv:
    def __init__(self, value):
        self.set(value)
        
    def set(self, value):
        t = type(value).__name__
        if isinstance(value, fv):
            self.t = value.t # type
            self.v = value.v # value
        elif t in ['int', 'float']:
            self.t = 'number'
            self.v = float(value)
        elif t == 'str':
            self.t = 'string'
            self.v = value
        elif t == 'list':
            self.t = 'list'
            self.v = value
        else:
            raise TypeError('fv accepts only ints, floats, strings and lists')
        

    # DECORATORS

    def fvparam(function):
        def wrapper(*args):
            return function(*map(fv, args))
        return wrapper

    def fvreturn(function):
        def wrapper(*args):
            return fv(function(*args))
        return wrapper

    def listonly(function):
        def wrapper(*args):
            self = args[0]
            if not self.is_list():
                raise TypeError('fv must be list')
            return function(*args)
        return wrapper


    # IS METHODS
        
    def is_number(self):
        return self.t == 'number'

    def is_number_form(self):
        if self.is_number(): return True
        try:
            float(self.s) # .s to include lists
            return True
        except ValueError:
            return False

    def is_integer_form(self):
        if not self.is_number_form():
            return False
        elif float(int(self.v)) == float(self.v):
            return True
        else:
            return False

    def is_string(self):
        return self.t == 'string'

    def is_list(self):
        return self.t == 'list'

    def is_infinite(self):
        return self.v in ['Infinity', '-Infinity']

    def __bool__(self): # not bulitin scratch
        if self.s == 'true':
            return True
        elif self.s == 'false':
            return False
        else:
            return bool(self.v)


    # CONVERSION METHODS

    def __str__(self):
        return str(self.v)

    def __len__(self):
        if self.is_list():
            return len(self.v)
        else:
            return len(self.s)

    @property
    def n(self):
        if self.is_integer_form():
            return int(self.v)
        elif self.is_number_form():
            return float(self.v)
        elif self.is_string() or self.is_list():
            return 0
        else:
            raise TypeError('invalid type when converting fv to number')

    @property
    def s(self):
        if self.is_string():
            return self.v
        elif self.is_number():
            return str(self.v)
        elif self.is_list():
            return self.v.join(' ')
        else:
            raise TypeError('invalid type when converting fv to string')


    # SIGN METHODS

    @fvparam
    @fvreturn
    def __neg__(self):
        if self.s == 'Infinity':
            return '-Infinity'
        elif self.s == '-Infinity':
            return 'Infinity'
        else:
            return -self.n

    @fvparam
    @fvreturn
    def __pos__(self):
        return self.n

    @fvparam
    @fvreturn
    def __abs__(self):
        if self < 0:
            return -self
        else:
            return self

    
    # MATH METHODS
    
    @fvparam
    @fvreturn
    def __add__(self, value):
        if sorted([self.s, value.s]) == ['-Infinity', 'Infinity']:
            return 'NaN'
        elif 'Infinity' in [self.s, value.s]:
            return 'Infinity'
        elif '-Infinity' in [self.s, value.s]:
            return '-Infinity'
        else:
            return self.n + value.n

    @fvparam
    @fvreturn
    def __sub__(self, value):
        return self + -value # uses __neg__
    
    @fvparam
    @fvreturn
    def __mul__(self, value):
        if 0 in [self.n, value.n] and (self.is_infinite() or value.is_infinite()):
            return 'NaN'
        elif sorted([self.s, value.s]) == ['-Infinity', 'Infinity']:
            return '-Infinity'
        elif [self.s, value.s] == ['-Infinity', '-Infinity']:
            return 'Infinity'
        elif 'Infinity' in [self.s, value.s]:
            return 'Infinity'
        elif '-Infinity' in [self.s, value.s]:
            return '-Infinity'
        else:
            return self.n * value.n

    @fvparam
    @fvreturn
    def __truediv__(self, value):
        if self.is_infinite() and value.is_infinite():
            return 'NaN'
        elif self.is_infinite() and value.n == 0:
            return self
        elif self.n == 0 and value.is_infinite():
            return 0
        elif self.is_infinite():
            return self
        elif value.is_infinite():
            return 0
        else:
            return self.n / value.n

    @fvparam
    @fvreturn
    def __floordiv__(self, value):
        return math.floor((self / value).n)

    @fvparam
    @fvreturn
    def __mod__(self, value):
        if self.is_infinite():
            return 'NaN'
        elif value.n == 0:
            return 'Nan'
        else:
            return self.n % value.n

    @fvparam
    @fvreturn # undefined in scratch
    def __pow__(self, value):
        return self.n ** value.n


    # iMATH METHODS

    @fvparam
    @fvreturn
    def __iadd__(self, value):
        self.set((self + value))
        return self
        
    @fvparam
    @fvreturn
    def __isub__(self, value):
        self.set((self - value))
        return self
        
    @fvparam
    @fvreturn
    def __imul__(self, value):
        self.set((self * value))
        return self
        
    @fvparam
    @fvreturn
    def __itruediv__(self, value):
        self.set((self / value))
        return self

    @fvparam
    @fvreturn
    def __ifloordiv__(self, value):
        self.set((self // value))
        return self

    @fvparam
    @fvreturn
    def __imod__(self, value):
        self.set((self * value))
        return self
        
    @fvparam
    @fvreturn
    def __ipow__(self, value):
        self.set((self ** value))
        return self


    # COMPARISON

    @fvparam
    def __lt__(self, value):
        if self == value:
            return False
        elif self.s == 'Infinity':
            return False
        elif self.s == '-Infinity':
            return True
        elif value.s == 'Infinity':
            return True
        elif value.s == '-Infinity':
            return False
        elif self.is_number_form() and value.is_string():
            return False
        elif self.is_string() and value.is_number_form():
            return True
        else:
            return self.v < value.v

    @fvparam
    def __gt__(self, value):
        if self == value:
            return False
        else:
            return not self < value

    @fvparam
    def __eq__(self, value):
        return self.s == value.s

    @fvparam
    def __le__(self, value):
        return (self == value) or (self < value)

    @fvparam
    def __ge__(self, value):
        return (self == value) or (self > value)


    # STRING AND INDEX METHODS

    @fvparam
    @fvreturn
    def join(self, value):
        return self.s + value.s

    @fvparam
    @fvreturn
    def __getitem__(self, index):
        print(index)
        if index not in range(len(self)):
            return ''
        elif self.is_list():
            return self.v[int(index.n)]
        else:
            return self.s[int(index.n)]

    @fvparam
    @listonly
    def __setitem__(self, index, value):
        if index in range(len(self)):
            self.v[int(index.n)] = value

    @fvparam
    @listonly
    def __delitem__(self, index):
        if index in range(len(self)):
            del self.v[int(index.n)]

    @fvparam
    @listonly
    def insert(self, index, value):
        if index in range(len(self)):
            self.v.insert(index, value)

    @fvparam
    @fvreturn
    @listonly
    def item_number_of(self, value):
        try:
            return self.v.index(value)
        except ValueError:
            return 0


        
a = fv(1)

print( a.is_integer_form())