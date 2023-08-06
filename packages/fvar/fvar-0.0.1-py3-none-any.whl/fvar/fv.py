# pre-computes .n and .s values at assignment

import math

def is_number_like(value):
	if isinstance(value, int) or isinstance(value, float):
		return True
	elif isinstance(value, str) and value.lower() in ('inf', '-inf', 'infinity', '-infinity', 'nan') and value not in ('Infinity', '-Infinity', 'NaN'):
		return False
	else:
		try:
			float(value)
			return True
		except:
			return False

def is_integer_like(value):
	if not is_number_like(value) or math.isinf(float(value)) or math.isnan(float(value)):
		return False
	elif float(int(value)) == float(value):
		return True
	else:
		return False

def all_single_items(value):
	return all(len(str(item)) == 1 for item in value)

def to_number(value):
	if is_number_like(value):
		if is_integer_like(value):
			return int(value)
		else:
			return float(value)
	elif isinstance(value, list) and all_single_items(value):
		return to_number(''.join(map(str, value)))
	else:
		return 0

def to_string(value):
	if isinstance(value, list):
		if all_single_items(value):
			return ''.join(map(str, value))
		else:
			return ' '.join(map(str, value))
	elif is_number_like(value):
		n = to_number(value)
		if math.isinf(n):
			return 'Infinity' if n > 0 else '-Infinity'
		elif math.isnan(n):
			return 'NaN'
		else:
			return str(n)
	else:
		return str(value)


class fv:
	def __init__(self, value):
		self.set(value)
		
	def set(self, value):
		if isinstance(value, fv):
			self.t = value.t # type
			self.n = value.n # number
			self.s = value.s # string
			self.l = value.l # list
		else:
			if isinstance(value, int) or \
				isinstance(value, float) or \
				value in ('-Infinity', 'Infinity', 'NaN'):	self.t = 'number'
			elif isinstance(value, str):					self.t = 'string'
			elif isinstance(value, list):					self.t = 'list'
			else:											raise TypeError('fv accepts only numbers, strings and lists')
			self.n = to_number(value)
			self.s = to_string(value)
			self.l = [*map(fv, value)] if self.is_list() else []
		

	# DECORATORS

	def arg(function):
		def wrapper(*args):
			return function(*map(fv, args))
		return wrapper

	def ret(function):
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

	def is_string(self):
		return self.t == 'string'

	def is_list(self):
		return self.t == 'list'

	def is_infinite(self):
		return math.isinf(self.n)

	def is_nan(self):
		return math.isnan(self.n)

	# def __bool__(self): # not bulitin scratch
	# 	if self.s == 'true':
	# 		return True
	# 	elif self.s == 'false':
	# 		return False
	# 	else:
	# 		return bool(self.v)


	# CONVERSION METHODS

	def __str__(self):
		return self.s

	def __repr__(self):
		if self.is_string() or self.is_infinite() or self.is_nan():
			return f'fv(\'{self.s}\')'
		elif self.is_list():
			return f'fv({self.l})'
		else:
			return f'fv({self.s})'

	def __len__(self):
		if self.is_list():
			return len(self.l)
		else:
			return len(self.s)

	@arg
	def __contains__(self, value):
		if self.is_list():
			return value in self.l
		else:
			return value.s in self.s

	def __floor__(self):
		if self.is_infinite() or self.is_nan():
			return self.n
		else:
			return float(math.floor(self.n))

	def __round__(self, precision=0):
		if self.is_infinite() or self.is_nan():
			return self.n
		else:
			return round(self.n, precision)

	def __ceil__(self):
		if self.is_infinite() or self.is_nan():
			return self.n
		else:
			return float(math.ceil(self.n))

	def __trunc__(self):
		if self.is_infinite() or self.is_nan():
			return self.n
		else:
			return float(math.trunc(self.n))

	def __int__(self):
		if self.is_infinite() or self.is_nan():
			return 0
		else:
			return int(self.n)

	def __float__(self):
		return float(self.n)


	# SIGN METHODS

	@arg
	@ret
	def __neg__(self): # consider keeping type
		return -self.n

	@arg
	@ret
	def __pos__(self):
		return self.n

	@arg
	@ret
	def __abs__(self):
		if self < 0:
			return -self
		else:
			return self

	
	# MATH METHODS
	
	@arg
	@ret
	def __add__(self, value):
		return self.n + value.n

	@arg
	@ret
	def __sub__(self, value):
		return self + -value # uses __neg__
	
	@arg
	@ret
	def __mul__(self, value):
		return self.n * value.n

	@arg
	@ret
	def __truediv__(self, value):
		if value == 0:
			if self.is_infinite():
				return self
			elif self == 0:
				return 'NaN'
			else:
				return 'Infinity'
		else:
			return self.n / value.n
			

	@arg
	@ret
	def __floordiv__(self, value):
		return math.floor(self / value)

	@arg
	@ret
	def __mod__(self, value):
		if value.n == 0:
			return 'NaN'
		elif value.is_infinite() and value < 0:
			return self
		else:
			return self.n % value.n

	@arg
	@ret # undefined in scratch
	def __pow__(self, value):
		return self.n ** value.n


	# iMATH METHODS

	@arg
	@ret
	def __iadd__(self, value):
		self.set((self + value))
		return self
		
	@arg
	@ret
	def __isub__(self, value):
		self.set((self - value))
		return self
		
	@arg
	@ret
	def __imul__(self, value):
		self.set((self * value))
		return self
		
	@arg
	@ret
	def __itruediv__(self, value):
		self.set((self / value))
		return self

	@arg
	@ret
	def __ifloordiv__(self, value):
		self.set((self // value))
		return self

	@arg
	@ret
	def __imod__(self, value):
		self.set((self * value))
		return self
		
	@arg
	@ret
	def __ipow__(self, value):
		self.set((self ** value))
		return self


	# COMPARISON

	@arg
	def __lt__(self, value):
		if is_number_like(self.s) and is_number_like(value.s):
			return self.n < value.n
		else:
			return self.s < value.s

	@arg
	def __gt__(self, value):
		if self == value:
			return False
		else:
			return not self < value

	@arg
	def __eq__(self, value):
		if self.is_list():
			if len(self) == len(value):
				for i in range(len(self)):
					if self[i] != value[i]:
						return False
				return True
			else:
				return False
		else:
			return self.s == value.s

	@arg
	def __le__(self, value):
		return (self == value) or (self < value)

	@arg
	def __ge__(self, value):
		return (self == value) or (self > value)


	# STRING METHODS

	@arg
	@ret
	def join(self, value):
		return self.s + value.s


	# LIST AND INDEX METHODS

	@arg
	@ret
	def __getitem__(self, index):
		if index not in range(len(self)):
			return ''
		elif self.is_list():
			return self.l[int(index.n)]
		else:
			return self.s[int(index.n)]

	@arg
	@listonly
	def __setitem__(self, index, value):
		if index in range(len(self)):
			self.l[int(index.n)] = value

	@arg
	@listonly
	def __delitem__(self, index):
		if index in range(len(self)):
			del self.l[int(index.n)]

	@arg
	@listonly
	def insert(self, index, value):
		if index in range(len(self)):
			self.l.insert(int(index.n), value)
		return self

	@arg
	@listonly
	def add(self, value):
		self.l.append(value)
		return self

	@arg
	@ret
	@listonly
	def item_number(self, value):
		try:
			return self.l.index(value)
		except ValueError:
			return 0

