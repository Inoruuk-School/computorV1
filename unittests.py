import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
	unittest.main()

def base_pattern_calcul(pat):
	"""
	This function is used to calculate the multiplier of each degree of power of X
	:param pat: iterator giving each time a sign, a multiplier and a degree
	:return:	A list containing the calculated multiplier for each degree, the first item being degree 0,
				second degree 1 and third degree 2
	"""
	res = [0, 0, 0]  # res[0] = mult X^0, res[1] = mult X^1, res[2] = mult X^2
	eq_sign = False
	for items in pat:
		if items.group('eq'):
			eq_sign = True
		if eq_sign is False:
			if items.group('sign') is None or items.group('sign') == '+':
				res[int(items.group('pow'))] += float(items.group('mult'))
			else:
				res[int(items.group('pow'))] -= float(items.group('mult'))
		else:
			if items.group('sign') == '+':
				res[int(items.group('pow'))] -= float(items.group('mult'))
			else:
				res[int(items.group('pow'))] += float(items.group('mult'))
	return {'a': res[2], 'b': res[1], 'c': res[0]}


def solution(sol: dict):
	a, b, c, disc = sol['a'], sol['b'], sol['c'], sol['b'] * sol['b'] - (sol['c'] * sol['a'] * 4)
	print('Le discriminant est :', disc)
	if disc == 0 and c != 0:
		print('Il existe une solution qui est : {}'.format((-(b/(2 * c)))))
	elif disc > 0 and c != 0:
		print('Il existe deux solutions qui sont : {} and {}'.format((-b - disc ** 0.5) / (2 * c), (-b + disc ** 0.5) / (2 * c)))
	elif c == 0 and b != 0:
		print('The solution is')
	elif b == 0:
		print('titi')
	else:
		print('Il n\'existe aucune solution a cette equation')