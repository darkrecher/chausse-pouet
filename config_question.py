"""
Configuration des questions
"""

from question_generator import (
	table_multiplication, table_addition, table_soustraction,
	double_de, moitie_de,
	qas_all)


table_multiplication(5)

table_multiplication(2)

double_de(3, 30)

moitie_de(1, 20)

table_soustraction(1, 20, 1, 20, generate_reverse=False)

table_addition(50, 100, 4, 10, generate_reverse=False)
