import random
import gifts


class GiftDistributor():


	def __init__(self, gift_keys_cancelled):

		gift_keys_all = set(gifts.gifts.keys())
		self.gift_keys = gift_keys_all.difference(set(gift_keys_cancelled))
		if not self.gift_keys:
			# Tous les cadeaux ont été annulés. C'est bien dommage.
			# Du coup, on reprend la liste de cadeaux initiale.
			self.gift_keys = gifts.gifts.keys()
		self.gift_keys = list(self.gift_keys)
		random.shuffle(self.gift_keys)


	def iterate_on_gifts(self):

		while True:
			gift_key = self.gift_keys.pop(0)
			yield gift_key, gifts.gifts[gift_key]

