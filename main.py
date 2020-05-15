import re

# Examples:
#  5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0
#  4 * X^0 + 4 * X^1 - 9.3 * X^2 = 0
#  5 * X^0 + 4 * X^1 = 4 * X^0
#  1 * X^0 + 4 * X^1 = 0
#  8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0
#  5 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 0
#  5 + 4 * X^0 + X^2= X^2
#  0*X^2-5*X^1-10*X^0=0
#  1X2-5X1-10=0

normal_pat = r'(?P<sign>[+=\-])?\s*(?P<mult>[0-9.]+)\s*\*\s*[xX]\^(?P<pow>\d+)'
# sign: +-= or nothing for first nb
# mult: multiplier before an X
# pow: degree/power of X

# r'(?P<sign>[+=\-])?\s*?((((?P<mult>[0-9.]*|[0-9]*)\s*[xX](?P<pow>[0-9])?))|(?P<nbs>[0-9.]+))'
advanced_pat = r'(?P<sign>[+=\-])?\s*?((((?P<mult>\d*.?\d*)\s*[xX](?P<pow>[0-9])?))|(?P<nbs>[0-9.]+))'
# sign: +=- or nothing for first nb
# mult: multiplier before an X

error_pat = r'([a-wyzA-WYZ]|[\d]*\.[\d]+\.[\d]+|[xX]\^[0-9]\.[0-9]+|[xX]\^[0-9]{2,}|[xX]\^[3-9]|[xX]\^-[0-9])'
# find letters, bad numbers(1.1.1...), bad powaaa X^3+ X^-1


def calcul_normal_pattern(pat):
	"""
	This function is used to calculate the multiplier of each degree of power of X
	:param pat: iterator giving each time a sign, a multiplier and a degree
	:return:	A list containing the calculated multiplier for each degree, the first item being degree 0,
				second degree 1 and third degree 2
	"""
	res = [0, 0, 0]  # res[0] = mult X^0, res[1] = mult X^1, res[2] = mult X^2
	eq_sign = False
	for items in pat:
		if items.group('sign') == '=':
			eq_sign = True
		if eq_sign is False:
			if items.group('sign') is None or items.group('sign') == '+':
				res[int(items.group('pow'))] += float(items.group('mult'))
			else:
				res[int(items.group('pow'))] -= float(items.group('mult'))
		else:
			if items.group('sign') in '=+':
				res[int(items.group('pow'))] -= float(items.group('mult'))
			else:
				res[int(items.group('pow'))] += float(items.group('mult'))
	return res


def calcul_simplified_pattern(pat):
	res = [0, 0, 0] # res[0] = mult X^0, res[1] = mult X^1, res[2] = mult X^2
	eq_sign = False
	for items in pat:
		if items.group('sign') == '=':
			eq_sign = True
		if eq_sign is False:
			if items.group('nbs') is None and (items.group('sign') is None or items.group('sign') == '+'):
				res[int(items.group('pow'))] += float(items.group('mult'))
			elif items.group('nbs') and (items.group('sign') is None or items.group('sign') == '+'):
				res[0] += float(items.group('nbs'))
			elif items.group('nbs'):
				res[0] -= float(items.group('nbs'))
			else:
				res[int(items.group('pow'))] -= float(items.group('mult'))
		else:
			if items.group('sign') in '=+' and items.group('nbs') is None:
				res[int(items.group('pow'))] -= float(items.group('mult'))
			elif items.group('sign') in '=+' and items.group('nbs'):
				res[0] -= float(items.group('nbs'))
			elif items.group('nbs'):
				res[0] += float(items.group('nbs'))
			else:
				res[int(items.group('pow'))] += float(items.group('mult'))
	print(res)
	return res


def solution(disc, inc):
	print('Le discriminant est :', disc)
	if disc == 0 and inc[2] != 0:
		print('Il existe une solution qui est : {}'.format((-(inc[1]/(2 * inc[2])))))
	elif disc > 0 and inc[2] != 0:
		print('Il existe deux solutions qui sont : {} and {}'.format((-inc[1] - disc ** 0.5) / (2 * inc[2]), (-inc[1] + disc ** 0.5) / (2 * inc[2])))
	elif inc[2] == 0 and inc[1] != 0:
		print('The solution is')
	elif inc[1] == 0:
		print('titi')
	else:
		print('Il n\'existe aucune solution a cette equation')


if __name__ == '__main__':
	while 1:
		inp = input("Donnez moi une équation du second degré!\n")
		if inp == '-h':
			print('La forme de base est : 1 + X^0 2 + X^1 3 + X^2 = 0 X^0\n'
				  'Des X minuscules peuvent être utilisés : 1 + x^0 2 + x^1 3 + x^2 = 0 x^0\n'
				  'Le ^ peut être enlevé: 9X + 18 + 22x2 + 11x = -15465X\n'
				  'Des nombres a virgules peuvent être utilisés : 9.3X + 18.65 + 22.542x2 + 1.1x = -15465.165413X')
		else:
			# A AMELIORER
			pattern = re.findall(normal_pat, inp)
			simplified_pattern = re.findall(advanced_pat, inp)
			wrong_pattern = re.findall(error_pat, inp)
			if not wrong_pattern and (pattern or simplified_pattern):
				if pattern:
					pattern = re.finditer(normal_pat, inp)
				else:
					simplified_pattern = re.finditer(advanced_pat, inp)
					# for x in simplified_pattern:
					# 	print('sign: ', x.group('sign'), ' mult: ', x.group('mult'), ' pow: ', x.group('pow'), ' nb: ', x.group('nbs'))
				break
			else:
				print("Votre équation n'a pas la forme correcte requise\n"
					  "-h pour avoir les possibilités de forme d'écriture de l'équation")
	if pattern:
		inc = calcul_normal_pattern(pattern)
	else:
		inc = calcul_simplified_pattern(simplified_pattern)
	# print('La forme simplifié est : {}{}{} = 0'
	# 	.format('{}X² '.format(inc[2]) if int(inc[2]) >= 0 else '- {}X² '.format(abs(inc[2])),
	# 	'+ {}X '.format(inc[1]) if int(inc[1]) >= 0 else '- {}X '.format(abs(inc[1])),
	# 	'+ {}'.format(inc[0]) if int(inc[0]) >= 0 else '- {}'.format(abs(inc[0]))))
	# solution(inc[1] * inc[1] - (inc[0] * inc[2] * 4), inc)
	# print('\u221A\u03051\u03056') #print une racine a supprimmer apres

#9.3X + 18.65 + 22.542X2 + 1.1X = -15465.165413X
#0.0012067496547532425 and 685.597471850292