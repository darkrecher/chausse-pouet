"""
Programme qui pose des questions (maths, etc.) pour s'entraîner.
Niveau CE1.

v1.1.0
"""

# TODO : limite à 80 chars.

import random
import config_generic
import config_question
import gifts
from game_saver import SavedInformations


VERSION = (1, 1, 0)

POINTS_FROM_NB_TRIES_MADE = {
	1: 5,
	2: 2,
	3: 1,
}

STEP_FOR_GIFT = 25

class FinishGameException(Exception): pass


def ask_question(question, answer, nb_tries_authorized=None):
	# TODO : Fonction pour déterminer si la réponse est correcte ou pas.
	# Plutôt qu'un test d'égalité de gros bourrin.

	answer = str(answer).strip().upper()
	answer_proposed = None
	nb_tries_made = 0

	while True:

		answer_proposed = input(' ' + question + ' : ')
		answer_proposed = answer_proposed.strip()

		if not answer_proposed:
			continue
		if answer_proposed.upper() in ('SALUT', 'AU REVOIR', 'S'):
			raise FinishGameException()
		if not answer_proposed.isdigit():
			print(" Pour quitter, écrit 'salut', ou juste la lettre 'S', puis appuie sur Entrée.")
			continue


		nb_tries_made += 1
		# Pas de conversion string -> int. On compare directement les chaînes. Osef.
		if answer_proposed == answer:
			print(' Bravo !')
			return True, nb_tries_made
		if nb_tries_authorized is not None and nb_tries_made >= nb_tries_authorized:
			print(' Tant pis. La bonne réponse était : ' + answer)
			return False, nb_tries_made
		print(' Mince alors. Mauvaise réponse')


def get_current_status(current_score, points_gained_last=None, end_game=False):
	if current_score == points_gained_last:
		return "Tu a gagné %s points." % points_gained_last
	elif end_game:
		return "Tu as terminé ta partie avec %s points." % current_score
	else:
		return "Tu a gagné %s points. Tu as maintenant %s points." % (points_gained_last, current_score)


def iterate_on_gift():
	the_gifts = list(gifts.gifts)
	random.shuffle(the_gifts)
	for gift in the_gifts:
		yield(gift)


def main():

	saved_informations = SavedInformations()

	# Suppression des doublons dans chaque catégorie de questions.
	qas_all = {
		qa_category: list(set(qas))
		for qa_category, qas in
		config_question.qas_all.items()
	}

	qa_categories_deck = []

	current_score = 0
	next_step_gift = STEP_FOR_GIFT
	gift_distributor = iterate_on_gift()

	print('')
	print('*' * 10)
	print("Coucou %s !" % config_generic.PLAYER_NAME)
	print("Bon courage pour ton entraînement.")
	print("Pour indiquer tes réponses, indique le bon nombre puis appuies sur la touche Entrée.")
	print('*' * 10)
	print('')

	while qas_all:

		# Suppression des catégories qui n'ont plus de question.
		# TODO : bon c'est moche. Ce serait mieux si le distributeur de question était une classe séparée,
		# avec un itérateur et tout.
		qa_categories = list(qas_all.keys())
		for qa_categ in qa_categories:
			if not qas_all[qa_categ]:
				del qas_all[qa_categ]

		# Pour initialiser le deck de catégorie, on prend chaque catégorie en double.
		# Ça permet d'avoir une répartition "équitable mais un peu random quand même", dans le choix des catégories.
		# TODO : rendre ça configurable.
		if not qa_categories_deck:
			qa_categories_deck.extend(qa_categories)
			qa_categories_deck.extend(qa_categories)
			random.shuffle(qa_categories_deck)

		qa_categ_selected = qa_categories_deck.pop(0)
		len_qas_selected = len(qas_all[qa_categ_selected])
		qa_index = random.randint(0, len_qas_selected-1)
		question, answer = qas_all[qa_categ_selected][qa_index]
		del qas_all[qa_categ_selected][qa_index]

		try:
			print('')
			correct, nb_tries_made = ask_question(question, answer, 3)
			print('')
			if correct:
				points_gained = POINTS_FROM_NB_TRIES_MADE.get(nb_tries_made, 0)
				current_score += points_gained
				print(get_current_status(current_score, points_gained))
				if current_score >= next_step_gift:
					next_step_gift += STEP_FOR_GIFT
					print("Tu mérites une petite récompense. Voici un joli dessin :")
					print('')
					# Ça va faire une exception s'il n'y a plus de récompenses.
					# Pour éviter ça, on va faire une sorte qu'il y ait toujours plus de récompenses possibles que de steps.
					print(next(gift_distributor))
					print('')
					input("Appuie sur Entrée pour continuer le jeu.")

			else:
				print("Passons à la question suivante.")

		# TODO : deux fois le même code. C'est dégueu. (break, ou un truc du genre).
		except FinishGameException:
			print('')
			print(get_current_status(current_score, end_game=True))
			saved_informations.save()
			print('Au revoir. À bientôt.')
			raise SystemExit()

	print("Tu as répondu à toutes les questions.")
	print(get_current_status(current_score, end_game=True))
	saved_informations.save()
	print("TODO : le truc avec le super-bonus")


if __name__ == '__main__':
	main()
