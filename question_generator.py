"""
Fonctions générant des questions.

qas (questions_answers) : liste de tuple de deux éléments. La question, la réponse.
"""

# https://stackoverflow.com/questions/533905/get-the-cartesian-product-of-a-series-of-lists
import itertools

qas_all = []

# TODO : faudrait pouvoir définir des coefs pour chaque question.
# Pour gérer le fait de mettre autant de multiplication que d'addition,
# même si y'a plus de questions d'additions que de questions de multiplication.


def decorator_add_in_qas_all(func_generate_qas):

	def wrapper_add_in_qas_all(*args, **kwargs):
		qas = func_generate_qas(*args, **kwargs)
		qas_all.extend(qas)

	return wrapper_add_in_qas_all


@decorator_add_in_qas_all
def table_multiplication(nb, generate_reverse=True):

	table = [
		(str(operand) + ' x ' + str(nb), operand*nb)
		for operand in range(11)
	]

	if generate_reverse:
		table_reversed = [
			(str(nb) + ' x ' + str(operand), operand*nb)
			for operand in range(11)
		]
		questions_answers = table + table_reversed
	else:
		questions_answers = table

	return questions_answers


@decorator_add_in_qas_all
def table_addition(
	operand_1_min, operand_1_max, operand_2_min, operand_2_max,
	generate_reverse=True
):

	operand_1_max += 1
	operand_2_max += 1

	table = [
		(str(operand_1) + ' + ' + str(operand_2), operand_1 + operand_2)
		for operand_1, operand_2 in itertools.product(
			range(operand_1_min, operand_1_max),
			range(operand_2_min, operand_2_max))
	]

	if generate_reverse:
		table_reversed = [
			(str(operand_2) + ' + ' + str(operand_1), operand_1 + operand_2)
			for operand_1, operand_2 in itertools.product(
				range(operand_1_min, operand_1_max),
				range(operand_2_min, operand_2_max))
		]
		questions_answers = table + table_reversed
	else:
		questions_answers = table

	return questions_answers


@decorator_add_in_qas_all
def table_soustraction(
	operand_1_min, operand_1_max, operand_2_min, operand_2_max,
	generate_reverse=True, authorize_negative_results=False
):
	operand_1_max += 1
	operand_2_max += 1

	table = [
		(str(operand_1) + ' - ' + str(operand_2), operand_1 - operand_2)
		for operand_1, operand_2 in itertools.product(
			range(operand_1_min, operand_1_max),
			range(operand_2_min, operand_2_max))
		if authorize_negative_results or operand_1 >= operand_2
	]

	if generate_reverse:
		table_reversed = [
			(str(operand_2) + ' - ' + str(operand_1), operand_1 - operand_2)
			for operand_1, operand_2 in itertools.product(
				range(operand_1_min, operand_1_max),
				range(operand_2_min, operand_2_max))
			if authorize_negative_results or operand_2 >= operand_1
		]
		questions_answers = table + table_reversed
	else:
		questions_answers = table

	return questions_answers


@decorator_add_in_qas_all
def double_de(nb_min, nb_max):
	nb_max += 1
	return [
		('Le double de ' + str(value), value * 2)
		for value in range(nb_min, nb_max)
	]


@decorator_add_in_qas_all
def moitie_de(nb_min, nb_max):
	nb_max += 1
	return [
		('La moitié de ' + str(value), value // 2)
		for value in range(nb_min + nb_min%2, nb_max, 2)
	]
