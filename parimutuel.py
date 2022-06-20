#! /usr/bin/python3

import numpy as np
import pandas as pd
from gambler import *
from bookmaker import *

#if __name__ == '__main__':
real_prob = [.3, .2, .03, .2, .27]
init_prob = [.25, .2, .05, .2, .3]
#	print(sum(init_prob))
#	print(sum(real_prob))
odds_to_prob = lambda x,y: x/(x + y)
bookmaker = Bookmaker(init_prob, odds_to_prob)
bookmaker.print_odds()


gamblers_list = {
	'g1': {'budget': 10000, 'opinion':[.3, .2, .1, .2, .2], 'bet_str': [('0.1', 'top_3'), ('quarter', '2_1'), ('quarter', '3_1'), ('half', '4_1'), ('all_in', 'top_1')], 'op': None},#con good guess
	'g2': {'budget': 10000, 'opinion':init_prob, 'bet_str': [('half', 'top_3'), ('quarter', 'top_2'), ('quarter', 'top_1'), ('all_in', '2_1_1'), ('all_in', 'top_1')], 'op': 'cow'},#con go w/ init guess
	'g3': {'budget': 25000, 'opinion':[.2, .2, .4, .1, .1], 'bet_str': [('0.05', 'top_3'), ('0.1', 'top_3'), ('half', '3_1'), ('half', '4_1'), ('all_in', 'top_2')], 'op': 'gr'},#bad guess, con beg 
	'g4': {'budget': 7500, 'opinion': [.3, .2, .1, .17, .23], 'bet_str': [('quarter', '3_3_1'), ('half', '3_2_1'), ('half', '3_2_1'), ('all_in', 'top_1'), ('all_in', 'top_2')], 'op': None},#low budget
	'g5': {'budget': 50000, 'opinion':[.1, .3, .2, .3, .1], 'bet_str': [('0.125', 'top_3'), ('quarter', '3_2_1'), ('half', 'top_1'), ('half', 'top_2'), ('all_in', 'top_2')], 'op': 'gr'},#high budget b/ guess
	'g6': {'budget': 25000, 'opinion':[.2, .2, .2, .2, .2], 'bet_str': [('0.125', 'top_2'), ('half', '3_2_1'), ('half', 'top_2'), ('all_in', '4_1'), ('all_in', 'top_2')], 'op': 'nc'},#no clue, aggressive
}

res = {'gambler': list(), 'st_mon': list(), 'prize': list(), 'net_gain': list(), 'winner': list()}
for _ in range(20):
	gamblers = dict()
	for gambler, params in gamblers_list.items():
		if not params['op']:
			params['op'] == 'eg'
		aux = Gambler(params['budget'], p_opinion=params['opinion'], track_bets=True, strategy=params['op'])
		gamblers[gambler] = aux

	for i in range(5):
		print(f'>>>> {i+1} Round <<<<')
		prob = bookmaker.get_probs()
		bets = dict()
		for label,gambler in gamblers.items():
			b_type, spread = gamblers_list[label]['bet_str'][i]
			bets[label] = gambler.def_bet(prob, b_type=b_type, spread=spread)
		bookmaker.place_bets(bets)
		bookmaker.print_odds()

	winner = np.random.choice(np.arange(len(real_prob)), p=real_prob)
	results = bookmaker.return_prize(winner)
	print('------------')
	print('Results')
	print('------------')
	print(f'Winner: #{winner+1} Horse')
	for gambler, prize in results.items():
		st_resources = gamblers[gambler].get_st_resources()
		print(f'gambler {gambler}: from ${st_resources:.2f} to ${prize:.2f}')
		print(f'\tNet Gain: ${prize - st_resources:.2f}')
		print(f'\tBetting history:')
		for i,bet in enumerate(gamblers[gambler].get_bets()):
			print(f'\t(#{i+1}) ${bet:.2f}')
		res['gambler'].append(gambler)
		res['st_mon'].append(st_resources)
		res['prize'].append(prize)
		res['net_gain'].append(prize-st_resources)
		res['winner'].append(winner)

df = pd.DataFrame(res)
df.to_csv('res_g.csv')
