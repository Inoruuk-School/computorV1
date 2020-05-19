import re

# Examples:
#  5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0
#  5 * X^0 + 4 * X^1 - 9.3 * X^2 = -1 * X^0
#  4 * X^0 + 4 * X^1 - 9.3 * X^2 = 0
#  5 * X^0 + 4 * X^1 = 4 * X^0
#  1 * X^0 + 4 * X^1 = 0
#  8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0
#  5 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 0
#  5 + 4 * X^0 + X^2= X^2
#  0*X^2-5*X^1-10*X^0=0
#  1X2-5X1-10=0
#  1X2-5X1-10= -5X2

base_pat = r'(?P<eq>=)?\s*?(?P<sign>[+\-])?\s*?(?P<mult>[0-9.]+)?\s*?\*?\s*?[xX]\^?(?P<pow>\d+)'
# eq: if '=' is found
# sign: +-= or nothing for first nb
# mult: multiplier before an X
# pow: degree/power of X


error_pat = r'([a-wyzA-WYZ]|[\d]*\.[\d]+\.[\d]+|[xX]\^?[0-9]\.[0-9]+|[xX]\^[0-9]{2,}|[xX]\^?-?[3-9]|[xX]\^-[0-9])'
# find letters, bad numbers(1.1.1...), bad powaaa X^3+ X^-1


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


def solution(expo: dict):
	a, b, c, disc = expo['a'], expo['b'], expo['c'], expo['b'] * expo['b'] - (expo['c'] * expo['a'] * 4)
	print('Le discriminant est :', disc)
	if disc < 0:
		print("Il n'existe pas de racines réelles, donc aucune solution")
	elif disc > 0:
		pos, neg = (-b + disc ** 0.5) / (2 * a), (-b - disc ** 0.5) / (2 * a)
		print("Il existe deux solutions: qui sont:\n"
			  "\t1: {}\n\t2: {}".format(pos, neg))
	else:
		print("Il existe une solution:\n\t{}".format(-b / (2 * a)))


if __name__ == '__main__':
	while 1:
		inp = input("Donnez moi une équation du second degré!\n")
		if inp == '-h':
			print('La forme de base est : 1 + X^0 2 + X^1 3 + X^2 = 0 X^0\n'
				  'Des X minuscules peuvent être utilisés : 1 + x^0 2 + x^1 3 + x^2 = 0 x^0\n'
				  'Le ^ peut être enlevé: 9X1 + 18x0 + 22x2 + 11x1 = -15465X0\n'
				  'Des nombres a virgules peuvent être utilisés : 9.3X + 18.65 + 22.542x2 + 1.1x = -15465.165413X')
		else:
			pattern = re.finditer(base_pat, inp)
			wrong_pattern = re.findall(error_pat, inp)
			if not wrong_pattern and pattern:
				break
			else:
				print("Votre équation n'a pas la forme correcte requise\n"
					  "-h pour avoir les possibilités de forme d'écriture de l'équation")
	sol = base_pattern_calcul(pattern)
	print('La forme simplifié est : {}{}{} = 0'
		.format('{}X² '.format(sol['a']) if int(sol['a']) >= 0 else '- {}X² '.format(abs(sol['a'])),
		'+ {}X '.format(sol['b']) if int(sol['b']) >= 0 else '- {}X '.format(abs(sol['b'])),
		'+ {}'.format(sol['c']) if int(sol['c']) >= 0 else '- {}'.format(abs(sol['c']))))
	solution(sol)

# 9.3X1 + 18.65X0 + 22.542X2 + 1.1X1 = -15465.165413X1
# -686.5201955022231 and -0.001205127712004599
# https://www.mathpapa.com/quadratic-formula/