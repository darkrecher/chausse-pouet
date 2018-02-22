import json


class SavedInformations():


	def __init__(self, filepath='savefile.txt', instant_load=True):
		self.filepath = filepath
		if instant_load:
			self.load()


	def load(self):

		try:
			with open(self.filepath, 'r', encoding='utf-8') as savefile:
				str_saved_infos = savefile.read()
		except:
			str_saved_infos = '{ "score": 0, "gifts": [] }'

		saved_infos = json.loads(str_saved_infos)
		self.score = saved_infos['score']
		# TODO : à renommer en "obtained_gifts", pour éviter de confusionner.
		self.gifts = saved_infos['gifts']


	def set_score(self, score):
		self.score = score


	def add_gift(self, gift_key):
		self.gifts.append(gift_key)


	def save(self):
		saved_infos = {
			'score': self.score,
			'gifts': self.gifts,
		}
		str_saved_infos = json.dumps(saved_infos)
		with open(self.filepath, 'w', encoding='utf-8') as savefile:
			savefile.write(str_saved_infos)

