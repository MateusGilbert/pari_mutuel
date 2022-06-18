#! /usr/bin/python3

import numpy as np
from gambler import *
from bookmaker import *

if __name__ == '__main__':
	init_prob = [.5, .25, .1, .05, .1]
	#print(sum(init_prob))
	odds_to_prob = lambda x,y: x/(x + y)
	bookmaker = Bookmaker(init_prob, odds_to_prob)
	bookmaker.print_odds()

	budget = {'g1': 1000, 'g2': 2500, 'g3': 5000}
	g1 = Gambler(budget['g1'], p_opinion=[.1, .4, .4, .1, .0], bettin_profile='all_in_top_2', track_bets=True)
	g2 = Gambler(budget['g2'], p_opinion=[.3, .2, .175, .125, .2], track_bets=True)
	g3 = Gambler(budget['g3'], bettin_profile='all_in_top_3', track_bets=True)
	gamblers = {'g1':  g1, 'g2': g2, 'g3': g3}


	prob = bookmaker.get_probs()
	bets = dict()
	for label,gambler in gamblers.items():
		bets[label] = gambler.def_bet(prob, b_type='quarter', spread='top_2')
	bookmaker.place_bets(bets)
	bookmaker.print_odds()


	prob = bookmaker.get_probs()
	bets = dict()
	for label,gambler in gamblers.items():
		bets[label] = gambler.def_bet(prob, b_type='half', spread='top_3')
	bookmaker.place_bets(bets)
	bookmaker.print_odds()


	prob = bookmaker.get_probs()
	bets = dict()
	for label,gambler in gamblers.items():
		bets[label] = gambler.def_bet(prob)
	bookmaker.place_bets(bets)
	bookmaker.print_odds()

	winner = np.random.choice(np.arange(len(init_prob)), p=init_prob)
	results = bookmaker.return_prize(winner)
	print('------------')
	print('Results')
	print('------------')
	print(f'Winner: #{winner+1} Horse')
	for gambler, prize in results.items():
		print(f'gambler {gambler}: from ${gamblers[gambler].get_st_resources():.2f} to ${prize:.2f}')
		print(f'\tBetting history:')
		for i,bet in enumerate(gamblers[gambler].get_bets()):
			print(f'\t(#{i+1}) ${bet:.2f}')

#
#	bets_1 = [100., 200., 300., 300., 0., 100., 800., 200., 100.]
#	bookmaker.place_bets(bets_1)
#	print('\nAfter first round of bets')
#	bookmaker.print_odds()
#	bookmaker.print_probs()
#
##	bets_2 = [0., 400., 300., 200., 200., 0., 0., 0., 0.]
##	bookmaker.place_bets(bets_2)
#	print('\nAfter second round of bets')
##	bookmaker.print_odds()
##	bookmaker.print_probs()
#
#	bookmaker.add_new_bet(200., 'Away by 4 goals')
#	bookmaker.print_odds()
#	bookmaker.print_probs()
#
#	bets_3 = [0., 0., 300., 100., 100., 0., 0., 80., 20., 100.]
#	bookmaker.place_bets(bets_3)
#	print('\nAfter third round of bets')
#	bookmaker.print_odds()
#	bookmaker.print_probs()
