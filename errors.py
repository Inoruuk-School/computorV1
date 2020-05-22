WARNING = '\033[1;31m'
GOOD = '\033[1;32m'
END = '\033[0m'


class Error(Exception):
	"""Base class for exceptions in this module."""
	pass


class InputEqError(Error):
	"""
	Exception raised for errors in the input

	Attribute:
	expression : input expression in which the error occured
	errors: list of errors in the expression
	"""

	def __init__(self, expression: str, errors: list):
		self.expression = expression
		self.errors = errors

	def __str__(self):
		y = 0
		buff = ''
		for err in self.errors:
			x = self.expression.find(err)
			buff += GOOD + self.expression[y:x] + END + WARNING + err + END
			y = x + len(err)
		return 'Input error: ' + buff + self.expression[y:]


if __name__ == '__main__':
	try:
		raise InputEqError('a * X^2 + 5 * X^3 = 0', ['a', 'X^3'])
	except InputEqError as inp:
		print(inp)