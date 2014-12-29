#map keys
import random
from Tkinter import *
from time import sleep
from math import *

OWNER = 0
ARMY = 1
NEIGHBOURS = 2
CONTINENT = 3
CONQUERED = 4

def random_map(size = 10, continents = 0, min_neigh = 1, max_neigh = 6):
	#make random, planar map
	if continents == 0: continents = size / 3
	map = []
	continent = 0
	bonus = []
	change_continent_chance = continents * 1. / size
	continent_nodes = 0
	for n in range(size):
		if random.random() < change_continent_chance and continent_nodes > 0:
			continent += 1
			cont_bonus = int((random.random() + 0.5)**0.3 * continent_nodes)
			bonus.append(cont_bonus)
			continent_nodes = 0
		num_neighbours = min_neigh - 1 + int(random.random() * max_neigh)
		neigh = []
		if n > 0:
			neigh.append(n-1)
		elif n == size - 1:
			neigh.append(0)
		else:
			num_neighbours += 1
		for m in range(num_neighbours):
			new_neigh = int(random.random() * size)
			while new_neigh == n or new_neigh in neigh:
				new_neigh = int(random.random() * size)
			neigh.append(new_neigh)
		node = {OWNER: -1, ARMY: 0, NEIGHBOURS: neigh, CONTINENT: continent, CONQUERED: 0}
		map.append(node)
		continent_nodes += 1
	if len(bonus) < continent + 1:
		cont_bonus = int((random.random() + 0.5)**0.3 * continent_nodes)
		bonus.append(cont_bonus)
	return [map, bonus]
def make_simple_map():
	#make simple map of 13 nodes (0-12) in 4 continents (0-3), with bonus = [2,3,2,5]
	map = []
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [1,2], CONTINENT: 0, CONQUERED: 0};map.append(node)			#0
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [0,2,3,4], CONTINENT: 0, CONQUERED: 0};map.append(node)		#1
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [0,1,4,5], CONTINENT: 1, CONQUERED: 0};map.append(node)		#2
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [1,4,10], CONTINENT: 3, CONQUERED: 0};map.append(node)		#3
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [1,2,3,5], CONTINENT: 1, CONQUERED: 0};map.append(node)		#4
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [2,4,6], CONTINENT: 1, CONQUERED: 0};map.append(node)		#5
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [5,7], CONTINENT: 1, CONQUERED: 0};map.append(node)			#6
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [6,8], CONTINENT: 2, CONQUERED: 0};map.append(node)			#7
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [7,9], CONTINENT: 2, CONQUERED: 0};map.append(node)			#8
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [8,10,12], CONTINENT: 3, CONQUERED: 0};map.append(node)		#9
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [3,9,11,12], CONTINENT: 3, CONQUERED: 0};map.append(node)	#10
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [10,12], CONTINENT: 3, CONQUERED: 0};map.append(node)		#11
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [9,10,11], CONTINENT: 3, CONQUERED: 0};map.append(node)		#12
	bonus = [2,3,2,5]
	return [map, bonus]
def make_world_map():
	#recreate risk world map
	map = []
	#NORTH AMERICA
	c = 0
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [1,2,37], CONTINENT: c, CONQUERED: 0};map.append(node)			#0
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [0,2,3], CONTINENT: c, CONQUERED: 0};map.append(node)			#1
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [0,1,3,4], CONTINENT: c, CONQUERED: 0};map.append(node)			#2
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [1,2,4,5,7], CONTINENT: c, CONQUERED: 0};map.append(node)			#3
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [2,3,5,6], CONTINENT: c, CONQUERED: 0};map.append(node)			#4
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [3,4,6,7], CONTINENT: c, CONQUERED: 0};map.append(node)			#5
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [4,5,9], CONTINENT: c, CONQUERED: 0};map.append(node)			#6
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [3,5,8], CONTINENT: c, CONQUERED: 0};map.append(node)			#7
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [7,19], CONTINENT: c, CONQUERED: 0};map.append(node)			#8
	#SOUTH AMERICA
	c += 1
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [6,10,11], CONTINENT: c, CONQUERED: 0};map.append(node)			#9
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [9,11,12], CONTINENT: c, CONQUERED: 0};map.append(node)			#10
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [9,10,12,13], CONTINENT: c, CONQUERED: 0};map.append(node)			#11
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [10,11], CONTINENT: c, CONQUERED: 0};map.append(node)			#12
	#AFRICA
	c += 1
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [11,14,15,16,21], CONTINENT: c, CONQUERED: 0};map.append(node)			#13
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [13,15,24,26], CONTINENT: c, CONQUERED: 0};map.append(node)			#14
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [13,14,16,17,18], CONTINENT: c, CONQUERED: 0};map.append(node)			#15
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [13,15,17], CONTINENT: c, CONQUERED: 0};map.append(node)			#16
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [15,16,18], CONTINENT: c, CONQUERED: 0};map.append(node)			#17
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [15,17], CONTINENT: c, CONQUERED: 0};map.append(node)			#18
	#EUROPE
	c += 1
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [8,20,23], CONTINENT: c, CONQUERED: 0};map.append(node)			#19
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [19,21,22], CONTINENT: c, CONQUERED: 0};map.append(node)			#20
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [20,22,24,13], CONTINENT: c, CONQUERED: 0};map.append(node)			#21
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [20,21,23,24,25], CONTINENT: c, CONQUERED: 0};map.append(node)			#22
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [19,22,25], CONTINENT: c, CONQUERED: 0};map.append(node)			#23
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [21,22,26,14], CONTINENT: c, CONQUERED: 0};map.append(node)			#24
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [22,23,26,27,28], CONTINENT: c, CONQUERED: 0};map.append(node)			#25
	#ASIA
	c += 1
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [14,24,25,28,29], CONTINENT: c, CONQUERED: 0};map.append(node)			#26
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [25,28,30,31], CONTINENT: c, CONQUERED: 0};map.append(node)			#27
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [25,26,27,29,31,32], CONTINENT: c, CONQUERED: 0};map.append(node)			#28
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [26,28,32,33], CONTINENT: c, CONQUERED: 0};map.append(node)			#29
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [27,31,34,35], CONTINENT: c, CONQUERED: 0};map.append(node)			#30
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [27,28,30,32,35,36], CONTINENT: c, CONQUERED: 0};map.append(node)			#31
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [28,29,31,33,36], CONTINENT: c, CONQUERED: 0};map.append(node)			#32
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [29,32,39], CONTINENT: c, CONQUERED: 0};map.append(node)			#33
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [30,35,37], CONTINENT: c, CONQUERED: 0};map.append(node)			#34
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [30,31,34,36,37], CONTINENT: c, CONQUERED: 0};map.append(node)			#35
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [31,32,35,37,38], CONTINENT: c, CONQUERED: 0};map.append(node)			#36
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [0,34,35,36,38], CONTINENT: c, CONQUERED: 0};map.append(node)			#37
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [36,37], CONTINENT: c, CONQUERED: 0};map.append(node)			#38
	#OCEANIA
	c += 1
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [33,40,41], CONTINENT: c, CONQUERED: 0};map.append(node)			#39
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [39,41,42], CONTINENT: c, CONQUERED: 0};map.append(node)			#40
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [39,40,42], CONTINENT: c, CONQUERED: 0};map.append(node)			#41
	node = {OWNER: -1, ARMY: 0, NEIGHBOURS: [40,41], CONTINENT: c, CONQUERED: 0};map.append(node)			#42
	bonus = [5,2,3,5,7,2]
	return [map, bonus]
def redraw_simple(map):
	w.delete('b')
	COL = {-1: [0,255,0],
		   0 : [255,0,0],
		   1 : [0,0,255],
		   2 : [0,255,255],
		   3 : [255,0,255],
		   4 : [255,255,0],
		   5 : [255,255,255],}
	for n in range(len(map)):
		total_armies = 0
		for node in range(len(map)): 
			if map[node][ARMY] > total_armies: total_armies = map[node][ARMY]
		if total_armies == 0: total_armies += 1
		#if map[n][ARMY] == 0: armies = 1
		#else: armies = map[n][ARMY]
		#mul = log(armies, total_armies)
		mul = map[n][ARMY] * 1. / total_armies
		mul = 0.5 + mul * 0.5
		r = hex(int(COL[map[n][OWNER]][0] * mul))
		if len(r)<4: r = '0x'+'0'+r[2]
		g = hex(int(COL[map[n][OWNER]][1] * mul))
		if len(g)<4: g = '0x'+'0'+g[2]
		b = hex(int(COL[map[n][OWNER]][2] * mul))
		if len(b)<4: b = '0x'+'0'+b[2]
		col = '#'+r[2]+r[3]+g[2]+g[3]+b[2]+b[3]
		if   n == 0: x1 = 40; x2 = 60; y1 = 00; y2 = 20
		elif n == 1: x1 = 30; x2 = 50; y1 = 20; y2 = 40
		elif n == 2: x1 = 50; x2 = 70; y1 = 20; y2 = 40
		elif n == 3: x1 = 20; x2 = 40; y1 = 40; y2 = 60
		elif n == 4: x1 = 40; x2 = 60; y1 = 40; y2 = 50
		elif n == 5: x1 = 60; x2 = 80; y1 = 40; y2 = 50
		elif n == 6: x1 = 70; x2 = 90; y1 = 50; y2 = 70
		elif n == 7: x1 = 70; x2 = 90; y1 = 70; y2 = 90
		elif n == 8: x1 = 60; x2 = 70; y1 = 70; y2 = 90
		elif n == 9: x1 = 40; x2 = 60; y1 = 70; y2 = 90
		elif n ==10: x1 = 20; x2 = 40; y1 = 60; y2 = 80
		elif n ==11: x1 = 00; x2 = 20; y1 = 70; y2 = 90
		elif n ==12: x1 = 20; x2 = 40; y1 = 80; y2 =100
		w.create_rectangle(x1,y1,x2,y2,tags='b',fill=col,outline='#000000')
	w.update()
def redraw_world(map):
	w.delete('b')
	COL = {-1: [0,255,0],
		   0 : [255,0,0],
		   1 : [0,0,255],
		   2 : [0,255,255],
		   3 : [255,0,255],
		   4 : [255,255,0],
		   5 : [255,255,255],}
		   
	max_armies = 2
	for node in range(len(map)): 
		if map[node][ARMY] > max_armies: max_armies = map[node][ARMY]
	
	mul = log(5, max_armies)
	#mul = 5. / max_armies
	#mul = 0.5 + mul * 0.5
	if mul>1:mul=1
	r = g = '0x00'
	b = hex(int(255 * mul))
	if len(b)<4: b = '0x'+'0'+b[2]
	col = '#'+r[2]+r[3]+g[2]+g[3]+b[2]+b[3]
	w.create_rectangle(0,140,200,150,tags='b',fill=col,outline='#000000')
	mul = log(10, max_armies)
	#mul = 10. / max_armies
	#mul = 0.5 + mul * 0.5
	if mul>1:mul=1
	r = g = '0x00'
	b = hex(int(255 * mul))
	if len(b)<4: b = '0x'+'0'+b[2]
	col = '#'+r[2]+r[3]+g[2]+g[3]+b[2]+b[3]
	w.create_rectangle(0,150,200,160,tags='b',fill=col,outline='#000000')
	mul = log(25, max_armies)
	#mul = 25. / max_armies
	#mul = 0.5 + mul * 0.5
	if mul>1:mul=1
	r = g = '0x00'
	b = hex(int(255 * mul))
	if len(b)<4: b = '0x'+'0'+b[2]
	col = '#'+r[2]+r[3]+g[2]+g[3]+b[2]+b[3]
	w.create_rectangle(0,160,200,170,tags='b',fill=col,outline='#000000')
	mul = log(50, max_armies)
	#mul = 50. / max_armies
	#mul = 0.5 + mul * 0.5
	if mul>1:mul=1
	r = g = '0x00'
	b = hex(int(255 * mul))
	if len(b)<4: b = '0x'+'0'+b[2]
	col = '#'+r[2]+r[3]+g[2]+g[3]+b[2]+b[3]
	w.create_rectangle(0,170,200,180,tags='b',fill=col,outline='#000000')
	for n in range(len(map)):
		if map[n][ARMY] == 0: armies = 1
		else: armies = map[n][ARMY]
		mul = log(armies, max_armies)
		#mul = map[n][ARMY] * 1. / max_armies
		mul = 0.5 + mul * 0.5
		#print mul,armies,max_armies
		r = hex(int(COL[map[n][OWNER]][0] * mul))
		if len(r)<4: r = '0x'+'0'+r[2]
		g = hex(int(COL[map[n][OWNER]][1] * mul))
		if len(g)<4: g = '0x'+'0'+g[2]
		b = hex(int(COL[map[n][OWNER]][2] * mul))
		if len(b)<4: b = '0x'+'0'+b[2]
		col = '#'+r[2]+r[3]+g[2]+g[3]+b[2]+b[3]
		if   n == 0: x1 =  00; x2 =  20; y1 =  10; y2 =  30
		elif n == 1: x1 =  20; x2 =  40; y1 =  00; y2 =  20
		elif n == 2: x1 =  20; x2 =  40; y1 =  20; y2 =  40
		elif n == 3: x1 =  40; x2 =  60; y1 =  10; y2 =  30
		elif n == 4: x1 =  40; x2 =  50; y1 =  30; y2 =  50
		elif n == 5: x1 =  50; x2 =  70; y1 =  30; y2 =  50
		elif n == 6: x1 =  40; x2 =  60; y1 =  50; y2 =  70
		elif n == 7: x1 =  60; x2 =  70; y1 =  10; y2 =  30
		elif n == 8: x1 =  70; x2 =  90; y1 =  00; y2 =  10
		
		elif n == 9: x1 =  40; x2 =  60; y1 =  70; y2 =  90
		elif n ==10: x1 =  30; x2 =  50; y1 =  90; y2 = 110
		elif n ==11: x1 =  50; x2 =  70; y1 =  90; y2 = 110
		elif n ==12: x1 =  40; x2 =  60; y1 = 110; y2 = 130
		
		elif n ==13: x1 =  70; x2 = 100; y1 =  70; y2 =  90
		elif n ==14: x1 = 100; x2 = 120; y1 =  70; y2 =  80
		elif n ==15: x1 = 100; x2 = 120; y1 =  80; y2 = 100
		elif n ==16: x1 =  90; x2 = 100; y1 =  90; y2 = 110
		elif n ==17: x1 = 100; x2 = 120; y1 = 100; y2 = 120
		elif n ==18: x1 = 120; x2 = 130; y1 =  90; y2 = 110
		
		elif n ==19: x1 =  90; x2 = 110; y1 =  10; y2 =  20
		elif n ==20: x1 =  90; x2 = 100; y1 =  20; y2 =  40
		elif n ==21: x1 =  90; x2 = 100; y1 =  40; y2 =  70
		elif n ==22: x1 = 100; x2 = 120; y1 =  30; y2 =  50
		elif n ==23: x1 = 110; x2 = 130; y1 =  20; y2 =  30
		elif n ==24: x1 = 100; x2 = 120; y1 =  50; y2 =  70
		elif n ==25: x1 = 120; x2 = 140; y1 =  30; y2 =  50
		
		elif n ==26: x1 = 120; x2 = 140; y1 =  50; y2 =  70
		elif n ==27: x1 = 140; x2 = 150; y1 =  20; y2 =  40
		elif n ==28: x1 = 140; x2 = 150; y1 =  40; y2 =  60
		elif n ==29: x1 = 140; x2 = 150; y1 =  60; y2 =  80
		elif n ==30: x1 = 150; x2 = 170; y1 =  10; y2 =  30
		elif n ==31: x1 = 150; x2 = 170; y1 =  30; y2 =  50
		elif n ==32: x1 = 150; x2 = 170; y1 =  50; y2 =  70
		elif n ==33: x1 = 150; x2 = 160; y1 =  70; y2 =  90
		elif n ==34: x1 = 170; x2 = 190; y1 =  00; y2 =  20
		elif n ==35: x1 = 170; x2 = 190; y1 =  20; y2 =  30
		elif n ==36: x1 = 170; x2 = 190; y1 =  30; y2 =  60
		elif n ==37: x1 = 190; x2 = 200; y1 =  10; y2 =  40
		elif n ==38: x1 = 190; x2 = 200; y1 =  40; y2 =  60
		
		elif n ==39: x1 = 160; x2 = 180; y1 =  90; y2 = 110
		elif n ==40: x1 = 180; x2 = 200; y1 =  90; y2 = 110
		elif n ==41: x1 = 160; x2 = 180; y1 = 110; y2 = 130
		elif n ==42: x1 = 180; x2 = 200; y1 = 110; y2 = 130
		w.create_rectangle(x1,y1,x2,y2,tags='b',fill=col,outline='#000000')
	w.update()

def get_player_nodes(map):
	#return dictionary of number of nodes owned by each player
	player_nodes = {}
	for node in map:
		if node[OWNER] not in player_nodes:
			player_nodes[node[OWNER]] = 0
		player_nodes[node[OWNER]] += 1
	return player_nodes

def place(bot, map, player):
	#run AI to decide where to place, and then place
	target = bot.place(map)
	if not isinstance(target, int):
		return
	target %= len(map)
	target_node = map[target]
	if target_node[OWNER] == player:
		target_node[ARMY] += 1
	map[target] = target_node
	return map	
def move(map, origin, target, armies):
	#enact move command given
	origin_node = map[origin]
	target_node = map[target]
	origin_node[ARMY] -= armies
	if origin_node[OWNER] == target_node[OWNER]:
		target_node[ARMY] += armies
	else:
		armies = battle(armies, target_node[ARMY])
		if armies < 0:
			#attacker wins
			target_node[ARMY] = -armies
			target_node[OWNER] = origin_node[OWNER]
			target_node[CONQUERED] = 1
		else:
			target_node[ARMY] = armies
	map[origin] = origin_node
	map[target] = target_node
	return map
def battle(attack, defend):
	#+ve if def win (survivors)
	#-ve if atk win (survivors now in def territory)
	attack *= .9
	attack *= (random.random() + 0.5) ** 0.1
	defend *= (random.random() + 0.5) ** 0.1
	return int(defend - attack)

"""
GAME DESCRIPTION:
1 Map generated with continents
2 Given random countries at start
3 Place armies on these countries
4 If a player owns a full continent, place armies for continents bonus
5 Each player decide to attack or place, then do so
6 Return to 4
"""
		#Initialise
		###############################################################



w=Canvas(width=200,height=200,background='#0000ff')
w.pack()
class RISKGAME():
	def __init__(self, map, bonus, num_players):
		self.map = map
		self.bonus = bonus
		self.num_players = num_players
		self.winners = []
		self.turn_list = []
		for player in range(num_players):
			self.winners.append(0)
		self.num_nodes = len(map)
	def play(self):
		no_conquer_turns = 0
		turn = 0
		#clear owned and army in each node
		for node in range(len(map)):
			map[node][OWNER] = -1
			map[node][ARMY] = 0
		#assign player starting nodes
		player_nodes = get_player_nodes(self.map)
		while -1 in player_nodes:
			for player in range(self.num_players):
				target = int(random.random() * self.num_nodes)
				target_node = self.map[target]
				while target_node[OWNER] == player: 
					target = int(random.random() * self.num_nodes)
					target_node = self.map[target]
				target_node[OWNER] = player
				self.map[target] = target_node
			player_nodes = get_player_nodes(self.map)

		#initialise bots
		bots = [BOT7(), BOT7(), BOT6(), BOT6(), BOT6(), BOT6()]
		for player in range(self.num_players):
			bots[player].setup(self.map, self.bonus, player)
			#Place initial armies
			###############################################################

		player_nodes = get_player_nodes(self.map)
		for player in range(self.num_players):
			if player in player_nodes:
				armies_to_place = player_nodes[player] / 3 + 3
				bot = bots[player]
				for n in range(armies_to_place):
					self.map = place(bot, self.map, player)

		while len(player_nodes) > 1:
			if no_conquer_turns > turn / 1.5 + 5: print no_conquer_turns,turn;return 0
			no_conquer_turns += 1; turn += 1
			#print turn
			#sleep(0.05)
			redraw_world(self.map)
			#Continent place
			###############################################################
			for node in range(len(self.map)):
				self.map[node][CONQUERED] = 0
			owned = []
			for continent in range(len(self.bonus)):
				owned.append(1)
				prev_owner = -1
				for target in range(len(self.map)):
					node_info = self.map[target]
					if node_info[CONTINENT] == continent:
						new_owner = node_info[OWNER]
						if prev_owner == -1:
							prev_owner = new_owner
						if new_owner != prev_owner:
							owned[continent] = -1
							break
						prev_owner = new_owner
				if owned[continent] == 1: owned[continent] = prev_owner
			#Move or place
			###############################################################
			player_nodes = get_player_nodes(self.map)
			for player in range(self.num_players):
				if player in player_nodes:
					bot = bots[player]
					for continent in range(len(self.bonus)):
						if owned[continent] == player:
							armies_to_place = self.bonus[continent]
							for n in range(armies_to_place):
								self.map = place(bot, self.map, player)

					#move_or_place = bot.move_or_place(self.map)
					move_or_place = 'place'
				
					if move_or_place == 'place':
						armies_to_place = player_nodes[player] / 3
						if armies_to_place < 3: armies_to_place = 3
						for n in range(armies_to_place):
							self.map = place(bot, self.map, player)

					move_or_place = 'move'
					if move_or_place == 'move':
						nodes = range(len(self.map))
						random.shuffle(nodes)
						for origin in nodes:
							origin_node = self.map[origin]
							if origin_node[OWNER] == player and origin_node[ARMY] > 0 and origin_node[CONQUERED] == 0:
								move_info = bot.move(self.map, origin)
								if isinstance(move_info, list) and len(move_info) == 2:
									target, armies = move_info
									if not (isinstance(target, int) or isinstance(armies, int)):
										break
									target %= self.num_nodes
									target_node = self.map[target]
									if target in origin_node[NEIGHBOURS]:
										armies %= origin_node[ARMY]
										old_owner = map[target][OWNER]
										self.map = move(self.map, origin, target, armies)
										if map[target][OWNER] != old_owner: no_conquer_turns = 0
										player_nodes = get_player_nodes(self.map)

		self.turn_list.append(turn)
		winner = player_nodes.keys()[0]
		self.winners[winner]+=1
		total_games = sum(self.winners)
		winner_percentages = []
		player = 0
		for player in range(self.num_players):
			winner_percentages.append(int(round(self.winners[player] / (1. * total_games) * 100)))
			player += 1
		print 'GAME',total_games,'(',turn,'TURNS )'
		print 'WIN PERCENTAGES:',winner_percentages
		print 'TURN INFO: MAX:',max(self.turn_list),'MEAN:',sum(self.turn_list)/len(self.turn_list),'MIN:',min(self.turn_list)

try: 
	from RiskAI import RNDBOT, BOT0, BOT1, BOT2, BOT3, BOT4, BOT5, BOT6, BOT7
	map, bonus = make_world_map()
	game = RISKGAME(map, bonus, 6)
	while 1: game.play()
except Exception, err:
	print 'ERROR: %s\n' % str(err)
	sleep(50)