#! /usr/bin/python3

import re
import numpy as np

class Bookmaker:
	def __init__(self, init_prob, to_probs, label='Horse', against=True, st_budget=2520, tol=1):
		self.__tol = 10**tol
		odds = list()
		for p in init_prob:
			x,y = self._prob_to_odds(p)
			odds.append((x,y))
		self.__book = odds
		self.__money = [st_budget*p for p in init_prob]
		self.__money.append(st_budget)
		self.label = label if label else 'Horse'
		self.odds_against = against
		self.odds_to_prob = to_probs
		self.gamblers = dict()

	def _prob_to_odds(self,x):
		aux = x; i = 1
		while ((aux % 1. != 0.) and (aux < self.__tol)):
			aux *= 10
			i *= 10
		x = int(np.floor(aux))
		y = int(np.floor(i-aux))

		if (x > y):
			if (x % y == 0):
				return x // y, 1
		elif (y > x):
			if (y % x == 0):
				return 1, y // x

		return x, y

	def change_odds_display(self):
		self.odds_against = not self.odds_against

	def print_odds(self):
		print('---------------')
		if self.odds_against:
			print('Odds Against:')
		else:
			print('Odds For:')
		print('---------------')
		for i,(x,y) in enumerate(self.__book):
			if self.odds_against:
				odds_str = f'{y}:{x}'
			else:
				odds_str = f'{x}:{y}'
			if isinstance(self.label, str):
				print(f'#{i+1} {self.label}: {odds_str}')
			else:
				if (i <= len(self.label)):
					print(f'#{i+1} {self.label[i]}: {odds_str}')
				else:
					print(f'#{i+1} Unnamed Bet: {odds_str}')
		print('---------------')

	def print_probs(self):
		print('---------------')
		print('Probabilities')
		print('---------------')
		for i,(x,y) in enumerate(self.__book):
			p = self.odds_to_prob(x,y)
			if isinstance(self.label,list):
				print(f'#{i+1} {self.label[i]}: {p:.3f}')
			else:
				print(f'#{i+1} {self.label}: {p:.3f}')
		print('---------------')

	def get_probs(self):				#seria interessante fazer os apostadores calcularem
		probabilities = list()
		for i,(x,y) in enumerate(self.__book):
			probabilities.append(self.odds_to_prob(x,y))
		return probabilities

	def __update_odds(self):
		probs = list(map(lambda x: x/self.__money[-1], self.__money[:-1]))
		new_odds = list()
		for p in probs:
			x,y = self._prob_to_odds(p)
			new_odds.append((x,y))
		self.__book[:] = new_odds

	def place_bets(self, placed_bets):
		cum_bets = []
		for gambler,bets in placed_bets.items():
			if gambler in self.gamblers:
				self.gamblers[gambler] = list(map(lambda x,y: x+y,
					self.gamblers[gambler], bets))
			else:
				self.gamblers[gambler] = bets

			if len(cum_bets) == 0:
				cum_bets = bets
			else:
				cum_bets = list(map(lambda x,y: x+y, cum_bets, bets))

		for i,bet in enumerate(cum_bets):
			self.__money[i] += bet
			self.__money[-1] += bet
		self.__update_odds()

	def return_prize(self,winner):
		x,y = self.__book[winner]
		prize_money = dict()
		for gambler, money in self.gamblers.items():
			prize_money[gambler] = y/x*money[winner]
		return prize_money

	def add_new_bet(self, bet, label=None):
		if isinstance(self.label, list):
			if not label:
				print('Unnamed bet!!!')
				return
			self.label.append(label)
		self.__money.append(self.__money[-1] + bet)
		self.__money[-2] = bet
		self.__update_odds()
