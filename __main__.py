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
#  X2-5X-10=0


def calcul_normal_pattern(pat):
	res = [0, 0, 0]  # res[0] = nombres sans X, res[1] = multiple de X, res[2] = multiple X^2
	for items in pat:
		if not items[0] or items[0] == '+':
			res[int(items[-1])] += float(items[1])
		else:
			res[int(items[-1])] -= float(items[1])
	return res


def calcul_simplified_pattern(pat):
	res = [0, 0, 0] #res[0] = nombres sans X, res[1] = multiple de X, res[2] = multiple X^2
	for items in pat: #item = [(total, signe, multiple, puissance si rien puissance = 1 sinon = 2)X^2 ou X^1 ou (total, signe, nombre)X^0]
		if items[0]:
			if not items[1] or items[1] == '+':
				res[int(items[3]) if items[3] else 1] += float(items[2]) if items[2] else 1
			else:
				res[int(items[3]) if items[3] else 1] -= float(items[2]) if items[2] else 1
		else:
			if not items[-2] or items[-2] == '+':
				res[0] += float(items[-1])
			else:
				res[0] -= float(items[-1])
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
		inp = input("equation du 2nd degre plz : ")
		pattern = re.findall('([+-=])?\s*([0-9.]+)\s*\*\s*[xX]\^(\d+)', inp)#first group : +-= or nothing, second group : number before *, third group :degree/power of X
		simplified_pattern = re.findall('((?P<sign>[+=-]?)\s*?(?P<multiplicateur>[0-9.]*|[0-9]*)\s*[xX](?P<puissance>[0-9]?))|((?P<sign2>[+=-]?)\s*?(?P<nombres>[0-9.]+))', inp)
		wrong_pattern = re.findall('([a-wyzA-WYZ]|[\d]*\.[\d]+\.[\d]+|X\^[0-9]\.[0-9]+|X\^[0-9]{2,}|X\^[3-9]|X\^-[0-9])', inp) #find letters, bad numbers(1.1.1...), bad powaaa X^3+ X^-1
		if not wrong_pattern and (pattern or simplified_pattern):
			break
		else:
			print("Mauvaise entrée, essayez avec la forme 1 + X^0 2 + X^1 3 + X^2 = 0 X^0 ...., sans lettres autres que xX ou nombres comme 9.9.9.9")
	if pattern:
		inc = calcul_normal_pattern(pattern)
	else:
		inc = calcul_simplified_pattern(simplified_pattern)
	print('La forme simplifié est : {}{}{} = 0'
		.format('{}X² '.format(inc[2]) if int(inc[2]) >= 0 else '- {}X² '.format(abs(inc[2])),
		'+ {}X '.format(inc[1]) if int(inc[1]) >= 0 else '- {}X '.format(abs(inc[1])),
		'+ {}'.format(inc[0]) if int(inc[0]) >= 0 else '- {}'.format(abs(inc[0]))))
	solution(inc[1] * inc[1] - (inc[0] * inc[2] * 4), inc)
	print('\u221A\u03051\u03056') #print une racine a supprimmer apres

#9.3X + 18.65 + 22.542X2 + 1.1X = -15465.165413X
#0.0012067496547532425 and 685.597471850292