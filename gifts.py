"""
Source des pokémons en ASCII arts :
 - http://www.fiikus.net/?pokedex

Autres sources pour plus tard :
 - https://www.ascii-code.com/ascii-art/video-games/pokemon.php
 - http://ascii.co.uk/art/pokemon
 - http://textart.io/art/tag/pokemon/1 etc.
"""

import os
import os.path

PATH_FIIKUS_POKEMONS = 'pokepack'
FILEPATH_FIIKUS_POKEMON_NAMES = os.sep.join((PATH_FIIKUS_POKEMONS, 'pokedex.txt'))


def fiikus_read_pokemon_names(filepath=FILEPATH_FIIKUS_POKEMON_NAMES):

	dict_names = {}

	with open(filepath, 'r', encoding='utf-8') as file_pokemon_names:
		for line in file_pokemon_names.readlines():
			if line.startswith('#'):
				poke_index, space, poke_name = line.partition(' ')
				if not space:
					raise Exception("Fail. Espace manquant.")
				poke_index = poke_index.lstrip('#')
				dict_names[poke_index] = poke_name.strip()

	return dict_names


def fiikus_read_pokemon_asciis(path=PATH_FIIKUS_POKEMONS, pokemon_max=151):

	dict_asciis = {}

	for poke_index in range(pokemon_max):
		poke_index = str(poke_index).rjust(3, '0')
		filename_pokemon = poke_index + '.txt'
		filepath_pokemon = os.sep.join((path, filename_pokemon))
		if os.path.isfile(filepath_pokemon):
			with open(filepath_pokemon, 'r', encoding='utf-8') as file_pokemon:
				pokemon_ascii = file_pokemon.read()
				pokemon_ascii = pokemon_ascii.strip('\n')
				dict_asciis[poke_index] = pokemon_ascii

	return dict_asciis


def fiikus_merge_pokemon(dict_names, dict_asciis):

	poke_gifts = {}
	poke_valid_indexes = set(dict_names.keys()).intersection(dict_asciis.keys())

	for poke_index in poke_valid_indexes:
		poke_name = dict_names[poke_index]
		poke_ascii = dict_asciis[poke_index]
		poke_gift = "%s\n\nC'est le pokémon %s !!\n" % (poke_ascii, poke_name)
		poke_key = 'fiikus_%s' % poke_index
		poke_gifts[poke_key] = poke_gift

	return poke_gifts


dict_names = fiikus_read_pokemon_names()
dict_asciis = fiikus_read_pokemon_asciis()
gifts = fiikus_merge_pokemon(dict_names, dict_asciis)


if __name__ == '__main__':
	print(gifts)
