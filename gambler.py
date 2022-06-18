#! /usr/bin/python3

import re

class Gambler:
	def __init__(self, resources, p_opinion=None, strategy='eg', bettin_profile='all_in', track_bets=False):
		self.resources=resources
		self._st_res=resources
		self.p_opinion=p_opinion
		self.strategy=strategy
		self.b_profile=bettin_profile
		self.track=track_bets
		self._bets = list()

	def get_st_resources(self):
		return self._st_res

	def get_bets(self):
		return self._bets

	def def_bet(self, money_dist, b_type='all_in', spread='top_1'):
		if self.resources == 0.:
			print('Go alway! You have no money left!')
			return

		if re.search('all', b_type):
			resources = self.resources
		elif re.search('quarter', b_type):
			resources = self.resources/4
		elif re.search('half', b_type):
			resources = self.resources/2
		else:
			try:
				aux = float(b_type)
			except:
				aux = 1.
			aux = aux if (aux <= 1. and aux > 0.) else 0.
			resources = self.resources*aux

		#if self.strategy == 'eg':
		expectations = self._eisenberg_gale(money_dist)

		#if re.search('top',self.b_profile):
		perc = None
		if re.search('top',spread):
			n = int(spread.split('_')[-1])
			expectations.sort(reverse=True)
			b_exp = expectations[:n]
		elif re.search('_',spread):
			perc = [int(x) for x in spread.split('_')]
			tot = sum(perc)
			perc = list(map(lambda x: x/perc, perc))
		else:
			b_exp = [max(expectations)]

		if perc:
			bets = [resources*p if e in b_exp else 0. for e,p in zip(expectations,perc)]
		else:
			bets = [resources if e in b_exp else 0. for e in expectations]
		n_bets = len(list(filter(lambda x: x > 0, bets)))
		if n_bets > 1:
			bets = [b/n_bets for b in bets]
		self.resources -= sum(bets)
		if self.resources < 0:
			self.resources = 0
		if self.track:
			while (len(self._bets) < len(bets)):
				self._bets.append(0.)
			self._bets = list(map(lambda x,y: x + y, self._bets, bets))
		return bets

	def _eisenberg_gale(self, money_dist):
		if self.p_opinion:
			while len(self.p_opinion) < len(money_dist):
				self.p_opinion.append(0.)
		else:
			probs = [1/len(money_dist) for _ in money_dist]
			return list(map(lambda P,pi: P/pi, probs, money_dist))

		return list(map(lambda P,pi: P/pi, self.p_opinion, money_dist))
