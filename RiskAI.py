OWNER = 0
ARMY = 1
NEIGHBOURS = 2
CONTINENT = 3
CONQUERED = 4

import random

class BOT0():
	def get_my_nodes(self, map):
		#return list of all my nodes
		my_nodes = []
		for node in range(len(map)):
			if map[node][OWNER] == self.player:
				my_nodes.append(node)
		return my_nodes
	def get_my_armies(self, map):
		#return number my armies
		my_armies = 0
		my_nodes = self.get_my_nodes(map)
		for node in my_nodes:
			my_armies += map[node][ARMY]
		return my_armies
	def get_enemy_armies(self, map):
		#return number enemy armies
		enemy_armies = 0
		for node in range(len(map)):
			if map[node][OWNER] != self.player:
				enemy_armies += map[node][ARMY]
		return enemy_armies
	def get_my_borders(self, map):
		#return list of my nodes neighbouring enemy nodes
		my_borders = []
		my_nodes = self.get_my_nodes(map)
		for node in my_nodes:
			neighbours = map[node][NEIGHBOURS]
			for neigh in neighbours:
				if map[neigh][OWNER] != self.player:
					my_borders.append(node)
					break
		return my_borders
	def get_continent_nodes(self, map, continent):
		#return list of nodes in continent
		continent_nodes = []
		for node in range(len(map)):
			if map[node][CONTINENT] == continent:
				continent_nodes.append(node)
		return continent_nodes
	def get_owned(self, map, node_list):
		#return nodes in list I own
		owned = []
		for node in node_list:
			if map[node][OWNER] == self.player:
				owned.append(node)
		return owned
	def get_armies(self, map, node_list):
		#return armies in node list
		armies = 0
		for node in node_list:
			armies += map[node][ARMY]
		return armies
	#REQUIRED PROCS
	def setup(self, map, bonus, player):
		self.bonus = bonus
		self.player = player
		#setup local variables
	def move_or_place(self, map):
		#return 'move' or 'place'
		if random.random()<.5: return 'place'
		else: return 'move'
	def move(self, map, origin):
		#return something invalid to cancel, or [target, armies]
		origin_node = map[origin]
		neighbours = origin_node[NEIGHBOURS]
		move = 0
		best_targ = [-1, 999999]
		for target in neighbours:
			target_node = map[target]
			if target_node[OWNER] != self.player and target_node[ARMY] < best_targ[1]:
				best_targ = [target, target_node[ARMY]]
		if origin_node[ARMY] * 0.8 > best_targ[1]:
			move = 1
		if best_targ == -1:
			random.shuffle(neighbours)
			return [neighbours[0], origin_node[ARMY]-1]
		if move == 0:
			return 0
		return [best_targ[0], origin_node[ARMY]-1]
	def place(self, map):
		#return target
		my_borders = self.get_my_borders(map)
		#Place army in border with worst ratio my_armies : enemy_armies if ratio < 0.5
		worst_ratio = [99999,0]
		for node in my_borders:
			most_neigh_armies = 0
			for neigh in map[node][NEIGHBOURS]:
				if map[neigh][OWNER] != self.player and map[neigh][ARMY] > most_neigh_armies:
					ratio = map[node][ARMY] * 1. / map[neigh][ARMY]
					if ratio < worst_ratio[0]: worst_ratio = [ratio, node]
		if worst_ratio[0] < 0.5: return worst_ratio[1]

		#Place army in continent I don't own and have highest fraction armies in
		best_cont = [0,0]
		for continent in range(len(self.bonus)):
			cont_nodes = self.get_continent_nodes(map, continent)
			cont_my_nodes = self.get_owned(map, cont_nodes)
			
			cont_armies = self.get_armies(map, cont_nodes)
			cont_my_armies = self.get_armies(map, cont_my_nodes)
			
			if cont_armies > 0: fraction_armies = cont_my_armies / cont_armies
			else: fraction_armies = 0.9999999999999
			
			if 1 > fraction_armies > best_cont[1]:
				best_cont = [continent, fraction_armies]
		#target = first node in best continent to be a border
		cont_nodes = self.get_continent_nodes(map, best_cont[0])
		target = -1
		for node in cont_nodes:
			if node in my_borders:
				target = node
				break
		if target == -1:
			random.shuffle(my_borders)
			target = my_borders[0]
		return target

class BOT1():
	#return list of all my nodes
	def get_my_nodes(self, map):
		my_nodes = []
		for node in range(len(map)):
			if map[node][OWNER] == self.player:
				my_nodes.append(node)
		return my_nodes
	#return number my armies
	def get_my_armies(self, map):
		my_armies = 0
		my_nodes = self.get_my_nodes(map)
		for node in my_nodes:
			my_armies += map[node][ARMY]
		return my_armies
	#return number enemy armies
	def get_enemy_armies(self, map):
		enemy_armies = 0
		for node in range(len(map)):
			if map[node][OWNER] != self.player:
				enemy_armies += map[node][ARMY]
		return enemy_armies
	#return list of my nodes neighbouring enemy nodes
	def get_my_borders(self, map):
		my_borders = []
		my_nodes = self.get_my_nodes(map)
		for node in my_nodes:
			neighbours = map[node][NEIGHBOURS]
			for neigh in neighbours:
				if map[neigh][OWNER] != self.player:
					my_borders.append(node)
					break
		return my_borders
	#return list of nodes in continent
	def get_continent_nodes(self, map, continent):
		continent_nodes = []
		for node in range(len(map)):
			if map[node][CONTINENT] == continent:
				continent_nodes.append(node)
		return continent_nodes
	#return nodes in list I own
	def get_owned(self, map, node_list):
		owned = []
		for node in node_list:
			if map[node][OWNER] == self.player:
				owned.append(node)
		return owned
	#return armies in node list
	def get_armies(self, map, node_list):
		armies = 0
		for node in node_list:
			armies += map[node][ARMY]
		return armies
	#REQUIRED PROCS
	def setup(self, map, bonus, player):
		#setup local variables
		self.bonus = bonus
		self.player = player
	def move_or_place(self, map):
		#return 'move' or 'place'
		if random.random()<.5: return 'place'
		else: return 'move'
	def move(self, map, origin):
		#return something invalid to cancel, or [target, armies]
		origin_node = map[origin]
		neighbours = origin_node[NEIGHBOURS]
		move = 0
		best_targ = [-1, 0]
		#select enemy neighbour with least armies
		for target in neighbours:
			target_node = map[target]
			if target_node[OWNER] != self.player and target_node[ARMY] > best_targ[1]:
				best_targ = [target, target_node[ARMY]]
		if origin_node[ARMY] * 0.8 < best_targ[1]:
			return 0
		return [best_targ[0], origin_node[ARMY]-1]
	def place(self, map):
		#return target
		my_borders = self.get_my_borders(map)
		#Place army in border with worst ratio my_armies : enemy_armies if ratio < 0.5
		worst_ratio = [99999,0]
		for node in my_borders:
			most_neigh_armies = 0
			for neigh in map[node][NEIGHBOURS]:
				if map[neigh][OWNER] != self.player and map[neigh][ARMY] > most_neigh_armies:
					ratio = map[node][ARMY] * 1. / map[neigh][ARMY]
					if ratio < worst_ratio[0]: worst_ratio = [ratio, node]
		if worst_ratio[0] < 0.5: return worst_ratio[1]

		#Place army in continent I don't own and lowest (cont_armies - 1.5 * my_armies)
		best_cont = [0,-999999]
		for continent in range(len(self.bonus)):
			cont_nodes = self.get_continent_nodes(map, continent)
			cont_my_nodes = self.get_owned(map, cont_nodes)
			
			cont_armies = self.get_armies(map, cont_nodes)
			cont_my_armies = self.get_armies(map, cont_my_nodes)
			
			if cont_armies > 0: advantage = cont_armies - 1.5 * cont_my_armies
			else: advantage = len(cont_nodes)
			
			if advantage < best_cont[1] and cont_armies < cont_my_armies < 0:
				best_cont = [continent, advantage]
		#target = first node in best continent to be a border
		cont_nodes = self.get_continent_nodes(map, best_cont[0])
		target = -1
		for node in cont_nodes:
			if node in my_borders:
				target = node
				break
		if target == -1:
			random.shuffle(my_borders)
			target = my_borders[0]
		return target

class BOT2():
	#return list of all my nodes
	def get_my_nodes(self, map):
		my_nodes = []
		for node in range(len(map)):
			if map[node][OWNER] == self.player:
				my_nodes.append(node)
		return my_nodes
	#return number my armies
	def get_my_armies(self, map):
		my_armies = 0
		my_nodes = self.get_my_nodes(map)
		for node in my_nodes:
			my_armies += map[node][ARMY]
		return my_armies
	#return number enemy armies
	def get_enemy_armies(self, map):
		enemy_armies = 0
		for node in range(len(map)):
			if map[node][OWNER] != self.player:
				enemy_armies += map[node][ARMY]
		return enemy_armies
	#return list of my nodes neighbouring enemy nodes
	def get_my_borders(self, map):
		my_borders = []
		my_nodes = self.get_my_nodes(map)
		for node in my_nodes:
			neighbours = map[node][NEIGHBOURS]
			for neigh in neighbours:
				if map[neigh][OWNER] != self.player:
					my_borders.append(node)
					break
		return my_borders
	#return list of nodes in continent
	def get_continent_nodes(self, map, continent):
		continent_nodes = []
		for node in range(len(map)):
			if map[node][CONTINENT] == continent:
				continent_nodes.append(node)
		return continent_nodes
	#return nodes in list I own
	def get_owned(self, map, node_list):
		owned = []
		for node in node_list:
			if map[node][OWNER] == self.player:
				owned.append(node)
		return owned
	#return armies in node list
	def get_armies(self, map, node_list):
		armies = 0
		for node in node_list:
			armies += map[node][ARMY]
		return armies
	#REQUIRED PROCS
	def setup(self, map, bonus, player):
		#setup local variables
		self.bonus = bonus
		self.player = player
	def move_or_place(self, map):
		#return 'move' or 'place'
		for origin in range(len(map)):
			origin_node = map[origin]
			continent = origin_node[CONTINENT]
			
			#find total armies in continent
			cont_nodes = self.get_continent_nodes(map, continent)
			cont_my_nodes = self.get_owned(map, cont_nodes)
				
			cont_armies = self.get_armies(map, cont_nodes)
			cont_my_armies = self.get_armies(map, cont_my_nodes)
			
			best_targ = [-1, 999999]
			if cont_armies * 2 > cont_my_armies * 2 > cont_armies:
				#select neighbour with least armies in continent
				neighbours = origin_node[NEIGHBOURS]
				for target in neighbours:
					target_node = map[target]
					if target_node[OWNER] != self.player and target_node[ARMY] < best_targ[1] and target_node[CONTINENT] == continent:
						best_targ = [target, target_node[ARMY]]
			elif cont_armies == cont_my_armies:
				neighbours = origin_node[NEIGHBOURS]
				for target in neighbours:
					target_node = map[target]
					if target_node[OWNER] != self.player and target_node[ARMY] < best_targ[1]:
						best_targ = [target, target_node[ARMY]]
			if origin_node[ARMY] * 0.8 > best_targ[1]: return 'move'
		return 'place'
	def move(self, map, origin):
		#return something invalid to cancel, or [target, armies]
		origin_node = map[origin]
		#check continent I'm in
		continent = origin_node[CONTINENT]
		
		#find total armies in continent
		cont_nodes = self.get_continent_nodes(map, continent)
		cont_my_nodes = self.get_owned(map, cont_nodes)
			
		cont_armies = self.get_armies(map, cont_nodes)
		cont_my_armies = self.get_armies(map, cont_my_nodes)
		
		best_targ = [-1, 9999999]
		neighbours = origin_node[NEIGHBOURS]
		#if all neighbours belong to us, move army to random.random one
		friendly = 1
		for target in neighbours:
			if map[target][OWNER] != self.player:
				friendly = 0
				break
		if friendly == 1:
			random.shuffle(neighbours)
			return [neighbours[0], origin_node[ARMY]-1]
		#select neighbour with least armies in continent
		if cont_armies * 2 > cont_my_armies * 2 > cont_armies:
			for target in neighbours:
				target_node = map[target]
				if target_node[OWNER] != self.player and target_node[ARMY] < best_targ[1] and target_node[CONTINENT] == continent:
					best_targ = [target, target_node[ARMY]]
		#if we own continent, select enemy with least armies
		elif cont_armies == cont_my_armies:
			for target in neighbours:
				target_node = map[target]
				if target_node[OWNER] != self.player and target_node[ARMY] < best_targ[1]:
					best_targ = [target, target_node[ARMY]]
		if origin_node[ARMY] * 0.8 > best_targ[1] and best_targ[0] != -1: 
			return [best_targ[0], origin_node[ARMY]-1]
		return 0
	def place(self, map):
		#return target
		my_borders = self.get_my_borders(map)
		#Place army in border with worst ratio my_armies : enemy_armies if ratio < 0.5
		worst_ratio = [99999,0]
		for node in my_borders:
			most_neigh_armies = 0
			for neigh in map[node][NEIGHBOURS]:
				if map[neigh][OWNER] != self.player and map[neigh][ARMY] > most_neigh_armies and map[neigh][CONTINENT] == map[node][CONTINENT]:
					ratio = map[node][ARMY] * 1. / map[neigh][ARMY]
					if ratio < worst_ratio[0]: worst_ratio = [ratio, node]
		if worst_ratio[0] < 0.5: return worst_ratio[1]

		#Place army in continent I don't own and lowest (cont_armies - 1.5 * my_armies)
		best_cont = [0,-999999]
		for continent in range(len(self.bonus)):
			cont_nodes = self.get_continent_nodes(map, continent)
			cont_my_nodes = self.get_owned(map, cont_nodes)
			
			cont_armies = self.get_armies(map, cont_nodes)
			cont_my_armies = self.get_armies(map, cont_my_nodes)
			
			if cont_armies > 0: advantage = cont_armies - 1.5 * cont_my_armies
			else: advantage = len(cont_nodes)
			
			if advantage < best_cont[1] and cont_armies < cont_my_armies < 0:
				best_cont = [continent, advantage]
		#target = first node in best continent to be a border
		cont_nodes = self.get_continent_nodes(map, best_cont[0])
		random.shuffle(cont_nodes)
		target = -1
		for node in cont_nodes:
			if node in my_borders:
				target = node
				break
		if target == -1:
			random.shuffle(my_borders)
			target = my_borders[0]
		return target

class BOT3():
	#return list of all my nodes
	def get_my_nodes(self, map):
		my_nodes = []
		for node in range(len(map)):
			if map[node][OWNER] == self.player:
				my_nodes.append(node)
		return my_nodes
	#return number my armies
	def get_my_armies(self, map):
		my_armies = 0
		my_nodes = self.get_my_nodes(map)
		for node in my_nodes:
			my_armies += map[node][ARMY]
		return my_armies
	#return number enemy armies
	def get_enemy_armies(self, map):
		enemy_armies = 0
		for node in range(len(map)):
			if map[node][OWNER] != self.player:
				enemy_armies += map[node][ARMY]
		return enemy_armies
	#return list of my nodes neighbouring enemy nodes
	def get_my_borders(self, map):
		my_borders = []
		my_nodes = self.get_my_nodes(map)
		for node in my_nodes:
			neighbours = map[node][NEIGHBOURS]
			for neigh in neighbours:
				if map[neigh][OWNER] != self.player:
					my_borders.append(node)
					break
		return my_borders
	#return list of nodes in continent
	def get_continent_nodes(self, map, continent):
		continent_nodes = []
		for node in range(len(map)):
			if map[node][CONTINENT] == continent:
				continent_nodes.append(node)
		return continent_nodes
	#return nodes in list I own
	def get_owned(self, map, node_list):
		owned = []
		for node in node_list:
			if map[node][OWNER] == self.player:
				owned.append(node)
		return owned
	#return armies in node list
	def get_armies(self, map, node_list):
		armies = 0
		for node in node_list:
			armies += map[node][ARMY]
		return armies
	#REQUIRED PROCS
	def setup(self, map, bonus, player):
		#setup local variables
		self.bonus = bonus
		self.player = player
	def move_or_place(self, map):
		#return 'move' or 'place'
		for node in range(len(map)):
			if self.move(map, node, place_or_move_test = 1): return 'move'
		return 'place'
	def move(self, map, origin, place_or_move_test = 0):
		#return something invalid to cancel, or [target, armies]
		origin_node = map[origin]
		#check continent I'm in
		continent = origin_node[CONTINENT]
		
		#find total armies in continent
		cont_nodes = self.get_continent_nodes(map, continent)
		cont_my_nodes = self.get_owned(map, cont_nodes)
			
		cont_armies = self.get_armies(map, cont_nodes)
		cont_my_armies = self.get_armies(map, cont_my_nodes)
		
		best_targ = [-1, 9999999]
		neighbours = origin_node[NEIGHBOURS]
		#if all neighbours belong to us, move army to random.random one
		friendly = 1
		for target in neighbours:
			if map[target][OWNER] != self.player:
				friendly = 0
				break
		if friendly == 1 and not place_or_move_test:
			return [random.choice(neighbours), origin_node[ARMY]-1]
		#select neighbour with least armies in continent if we have enough armies
		if cont_armies * 2 > cont_my_armies * 2 > cont_armies:
			for target in neighbours:
				target_node = map[target]
				if target_node[OWNER] != self.player and target_node[ARMY] < best_targ[1] and target_node[CONTINENT] == continent:
					best_targ = [target, target_node[ARMY]]
		#if we own continent, select enemy with least armies
		elif cont_armies == cont_my_armies:
			for target in neighbours:
				target_node = map[target]
				if target_node[OWNER] != self.player and target_node[ARMY] < best_targ[1]:
					best_targ = [target, target_node[ARMY]]
		#if we have insufficient armies to take and don't own continent
		elif not place_or_move_test:
			#check all neighbouring continents, find one with best 'advantage'
			neighbouring_conts = []
			for target in neighbours:
				if map[target][CONTINENT] not in neighbouring_conts and map[origin][CONTINENT] != map[target][CONTINENT]: 
					neighbouring_conts.append(map[target][CONTINENT])
			if neighbouring_conts:
				best_cont = [0, -999999]
				for continent in neighbouring_conts:
					cont_nodes = self.get_continent_nodes(map, continent)
					cont_my_nodes = self.get_owned(map, cont_nodes)
					
					cont_armies = self.get_armies(map, cont_nodes)
					cont_my_armies = self.get_armies(map, cont_my_nodes)
					
					if cont_armies > 0: advantage = (map[origin][ARMY] + cont_my_armies * 2) - cont_armies
					else: advantage = len(cont_nodes)
					if advantage > best_cont[1] and (cont_armies > cont_my_armies > 0 or best_cont[0] == 0):
						best_cont = [continent, advantage]
						
				continent = best_cont[0]
					
				cont_nodes = self.get_continent_nodes(map, continent)
				cont_my_nodes = self.get_owned(map, cont_nodes)
					
				cont_armies = self.get_armies(map, cont_nodes)
				cont_my_armies = self.get_armies(map, cont_my_nodes)
				
				#print origin,neighbouring_conts,continent
				
				if map[origin][ARMY] * 1.5 > cont_armies - cont_my_armies:
				#pick neighbour in that cont with the least armies
					for target in neighbours:
						target_node = map[target]
						if target_node[OWNER] != self.player and target_node[ARMY] < best_targ[1] and target_node[CONTINENT] == continent:
							best_targ = [target, target_node[ARMY]]
					#print best_targ[0]
		if origin_node[ARMY] * 0.8 > best_targ[1] and best_targ[0] != -1: 
			return [best_targ[0], origin_node[ARMY]-1]
		return 0
	def place(self, map):
		#return target
		my_borders = self.get_my_borders(map)
		#Place army in border with worst ratio my_armies : enemy_armies if ratio < 0.5
		worst_ratio = [99999,0]
		for node in my_borders:
			most_neigh_armies = 0
			for neigh in map[node][NEIGHBOURS]:
				if map[neigh][OWNER] != self.player and map[neigh][ARMY] > most_neigh_armies:
					ratio = map[node][ARMY] * 1. / map[neigh][ARMY]
					if ratio < worst_ratio[0]: worst_ratio = [ratio, node]
		if worst_ratio[0] < 0.5: return worst_ratio[1]

		#Place army in continent I don't own and best 'advantage'
		best_cont = [-1, -999999]
		for continent in range(len(self.bonus)):
			cont_nodes = self.get_continent_nodes(map, continent)
			cont_my_nodes = self.get_owned(map, cont_nodes)
			
			if len(cont_my_nodes) > 0:
				cont_armies = self.get_armies(map, cont_nodes)
				cont_my_armies = self.get_armies(map, cont_my_nodes)
				
				if cont_armies > 0: advantage = cont_my_armies * 2 - cont_armies
				else: advantage = len(cont_nodes)
				
				if advantage > best_cont[1] and cont_armies != cont_my_armies:
					best_cont = [continent, advantage]
		if best_cont == -1:
			my_nodes = get_my_nodes(map)
			return random.choice(my_nodes)
		#target = random.random border node in best continent
		cont_nodes = self.get_continent_nodes(map, best_cont[0])
		random.shuffle(cont_nodes)
		target = -1
		for node in cont_nodes:
			if node in my_borders:
				target = node
				break
		if target == -1:
			target = random.choice(my_borders)
		return target

class BOT4():
	#return list of all my nodes
	def get_my_nodes(self, map):
		my_nodes = []
		for node in range(len(map)):
			if map[node][OWNER] == self.player:
				my_nodes.append(node)
		return my_nodes
	#return number my armies
	def get_my_armies(self, map):
		my_armies = 0
		my_nodes = self.get_my_nodes(map)
		for node in my_nodes:
			my_armies += map[node][ARMY]
		return my_armies
	#return number enemy armies
	def get_enemy_armies(self, map):
		enemy_armies = 0
		for node in range(len(map)):
			if map[node][OWNER] != self.player:
				enemy_armies += map[node][ARMY]
		return enemy_armies
	#return list of my nodes neighbouring enemy nodes
	def get_my_borders(self, map):
		my_borders = []
		my_nodes = self.get_my_nodes(map)
		for node in my_nodes:
			neighbours = map[node][NEIGHBOURS]
			for neigh in neighbours:
				if map[neigh][OWNER] != self.player:
					my_borders.append(node)
					break
		return my_borders
	#return list of nodes in continent
	def get_continent_nodes(self, map, continent):
		continent_nodes = []
		for node in range(len(map)):
			if map[node][CONTINENT] == continent:
				continent_nodes.append(node)
		return continent_nodes
	#return nodes in list I own
	def get_owned(self, map, node_list):
		owned = []
		for node in node_list:
			if map[node][OWNER] == self.player:
				owned.append(node)
		return owned
	#return armies in node list
	def get_armies(self, map, node_list):
		armies = 0
		for node in node_list:
			armies += map[node][ARMY]
		return armies
	#REQUIRED PROCS
	def setup(self, map, bonus, player):
		#setup local variables
		self.bonus = bonus
		self.player = player
	def move_or_place(self, map):
		#return 'move' or 'place'
		for node in range(len(map)):
			if self.move(map, node, place_or_move_test = 1): return 'move'
		return 'place'
	def move(self, map, origin, place_or_move_test = 0):
		#return something invalid to cancel, or [target, armies]
		origin_node = map[origin]
		#check continent I'm in
		continent = origin_node[CONTINENT]
		
		#find total armies in continent
		cont_nodes = self.get_continent_nodes(map, continent)
		cont_my_nodes = self.get_owned(map, cont_nodes)
			
		cont_armies = self.get_armies(map, cont_nodes)
		cont_my_armies = self.get_armies(map, cont_my_nodes)
		
		best_targ = [-1, 9999999]
		neighbours = origin_node[NEIGHBOURS]
		#if all neighbours belong to us, move army to random one
		friendly = 1
		for target in neighbours:
			if map[target][OWNER] != self.player:
				friendly = 0
				break
		if friendly == 1 and not place_or_move_test:
			return [random.choice(neighbours), origin_node[ARMY]-1]
		#select neighbour with least armies in continent if we have enough armies
		if cont_armies * 2 > cont_my_armies * 2 > cont_armies:
			for target in neighbours:
				target_node = map[target]
				if target_node[OWNER] != self.player and target_node[ARMY] < best_targ[1] and target_node[CONTINENT] == continent:
					best_targ = [target, target_node[ARMY]]
		#if we own continent, select enemy with least armies
		elif cont_armies == cont_my_armies:
			for target in neighbours:
				target_node = map[target]
				if target_node[OWNER] != self.player and target_node[ARMY] < best_targ[1]:
					best_targ = [target, target_node[ARMY]]
		#if we have insufficient armies to take and don't own continent, attack neigh cont w/ best advantage
		elif not place_or_move_test:
			#check all neighbouring continents, find one with best 'advantage'
			neighbouring_conts = []
			for target in neighbours:
				if map[target][CONTINENT] not in neighbouring_conts and map[origin][CONTINENT] != map[target][CONTINENT]: 
					neighbouring_conts.append(map[target][CONTINENT])
			if neighbouring_conts:
				best_cont = [0, -999999]
				for continent in neighbouring_conts:
					cont_nodes = self.get_continent_nodes(map, continent)
					cont_my_nodes = self.get_owned(map, cont_nodes)
					
					cont_armies = self.get_armies(map, cont_nodes)
					cont_my_armies = self.get_armies(map, cont_my_nodes)
					
					if cont_armies > 0: advantage = (map[origin][ARMY] + cont_my_armies * 2) - cont_armies
					else: advantage = len(cont_nodes)
					if advantage > best_cont[1] and (cont_armies > cont_my_armies > 0 or best_cont[0] == 0):
						best_cont = [continent, advantage]
						
				continent = best_cont[0]
					
				cont_nodes = self.get_continent_nodes(map, continent)
				cont_my_nodes = self.get_owned(map, cont_nodes)
					
				cont_armies = self.get_armies(map, cont_nodes)
				cont_my_armies = self.get_armies(map, cont_my_nodes)
				
				#print origin,neighbouring_conts,continent
				
				if map[origin][ARMY] * 1.5 > cont_armies - cont_my_armies:
				#pick neighbour in that cont with the least armies
					for target in neighbours:
						target_node = map[target]
						if target_node[OWNER] != self.player and target_node[ARMY] < best_targ[1] and target_node[CONTINENT] == continent:
							best_targ = [target, target_node[ARMY]]

		if origin_node[ARMY] * 0.8 > best_targ[1] and best_targ[0] != -1: 
			return [best_targ[0], origin_node[ARMY]-1]
		return 0
	def place(self, map):
		#return target
		my_borders = self.get_my_borders(map)
		#Place army in border with worst ratio my_armies : enemy_armies if ratio < 0.5
		#TODO: have a check to decide whether we really want to use armies to defend node
		worst_ratio = [99999,0]
		for node in my_borders:
			most_neigh_armies = 0
			for neigh in map[node][NEIGHBOURS]:
				if map[neigh][OWNER] != self.player and map[neigh][ARMY] > most_neigh_armies:
					ratio = map[node][ARMY] * 1. / map[neigh][ARMY]
					if ratio < worst_ratio[0]: worst_ratio = [ratio, node]
		if worst_ratio[0] < 0.5: return worst_ratio[1]

		#Place army in continent I don't own and best 'advantage'
		best_cont = [-1, -999999]
		for continent in range(len(self.bonus)):
			cont_nodes = self.get_continent_nodes(map, continent)
			cont_my_nodes = self.get_owned(map, cont_nodes)
			
			if len(cont_my_nodes) > 0:
				cont_armies = self.get_armies(map, cont_nodes)
				cont_my_armies = self.get_armies(map, cont_my_nodes)
				
				if cont_armies > 0: advantage = cont_my_armies * 2 - cont_armies
				else: advantage = len(cont_nodes)
				
				if advantage > best_cont[1] and cont_armies != cont_my_armies:
					best_cont = [continent, advantage]
		if best_cont == -1:
			my_nodes = get_my_nodes(map)
			return random.choice(my_nodes)
		#target = border node in best continent
		cont_nodes = self.get_continent_nodes(map, best_cont[0])
		targets = []
		for node in cont_nodes:
			if node in my_borders:
				targets.append(node)
		if targets == []:
			target = random.choice(my_borders)
		elif len(targets) == 1:
			target = targets[0]
		else:
			cont_my_nodes = self.get_owned(map, cont_nodes)
			#multiple potential nodes, choose one with biggest army
			#bordering enemy node in continent
			best_targ_pri = [-1, -1]
			#bordering any node
			best_targ_sec = [-1, -1]
			for target in targets:
				if map[target][ARMY] > best_targ_pri[1]:
					for neigh in map[target][NEIGHBOURS]:
						if neigh in cont_nodes and neigh not in cont_my_nodes:
							best_targ_pri= [target, map[target][ARMY]]
							break
					if map[target][ARMY] > best_targ_sec[1]:
						best_targ_sec = [target, map[target][ARMY]]
			if best_targ_pri[0] != -1:
				target = best_targ_pri[0]
			else:
				target = best_targ_sec[0]
		return target

class BOT5():
	#return list of all my nodes
	def get_my_nodes(self, map):
		my_nodes = []
		for node in range(len(map)):
			if map[node][OWNER] == self.player:
				my_nodes.append(node)
		return my_nodes
	#return number my armies
	def get_my_armies(self, map):
		my_armies = 0
		my_nodes = self.get_my_nodes(map)
		for node in my_nodes:
			my_armies += map[node][ARMY]
		return my_armies
	#return number enemy armies
	def get_enemy_armies(self, map):
		enemy_armies = 0
		for node in range(len(map)):
			if map[node][OWNER] != self.player:
				enemy_armies += map[node][ARMY]
		return enemy_armies
	#return list of my nodes neighbouring enemy nodes
	def get_my_borders(self, map):
		my_borders = []
		my_nodes = self.get_my_nodes(map)
		for node in my_nodes:
			neighbours = map[node][NEIGHBOURS]
			for neigh in neighbours:
				if map[neigh][OWNER] != self.player:
					my_borders.append(node)
					break
		return my_borders
	#return list of nodes in continent
	def get_continent_nodes(self, map, continent):
		continent_nodes = []
		for node in range(len(map)):
			if map[node][CONTINENT] == continent:
				continent_nodes.append(node)
		return continent_nodes
	#return nodes in list I own
	def get_owned(self, map, node_list):
		owned = []
		for node in node_list:
			if map[node][OWNER] == self.player:
				owned.append(node)
		return owned
	#return armies in node list
	def get_armies(self, map, node_list):
		armies = 0
		for node in node_list:
			armies += map[node][ARMY]
		return armies
	#REQUIRED PROCS
	def setup(self, map, bonus, player):
		#setup local variables
		self.bonus = bonus
		self.player = player
	def move_or_place(self, map):
		#return 'move' or 'place'
		for node in range(len(map)):
			if self.move(map, node, place_or_move_test = 1): return 'move'
		return 'place'
	def move(self, map, origin, place_or_move_test = 0):
		#return something invalid to cancel, or [target, armies]
		origin_node = map[origin]
		#check continent I'm in
		continent = origin_node[CONTINENT]
		
		#find total armies in continent
		cont_nodes = self.get_continent_nodes(map, continent)
		cont_my_nodes = self.get_owned(map, cont_nodes)
			
		cont_armies = self.get_armies(map, cont_nodes)
		cont_my_armies = self.get_armies(map, cont_my_nodes)
		
		best_targ = [-1, 9999999]
		neighbours = origin_node[NEIGHBOURS]
		#if all neighbours belong to us, move army to random one
		friendly = 1
		for target in neighbours:
			if map[target][OWNER] != self.player:
				friendly = 0
				break
		if friendly == 1 and not place_or_move_test:
			return [random.choice(neighbours), int(origin_node[ARMY] * .9)]
		#select neighbour with worst 'advantage' if sufficient armies in cont
		if cont_my_armies * 2 > cont_armies:
			#if we don't own continent, aim for neighbour in continent
			if cont_armies == cont_my_armies: own_cont = 1
			else: own_cont = 0
			for target in neighbours:
				target_node = map[target]
				target_neigh = target_node[NEIGHBOURS]
				owned_target_neigh = self.get_owned(map, target_neigh)
				owned_target_neigh_armies = self.get_armies(map, owned_target_neigh)
				#advantage = target_node[ARMY]
				advantage = target_node[ARMY] - owned_target_neigh_armies * 0.5
				if target_node[OWNER] != self.player and 0 > advantage < best_targ[1] and (target_node[CONTINENT] == continent or own_cont):
					best_targ = [target, advantage]
		#if we have insufficient armies to take and don't own continent, attack neigh cont w/ best advantage
		elif not place_or_move_test:
			#check all neighbouring continents, find one with best 'advantage'
			neighbouring_conts = []
			for target in neighbours:
				if map[target][CONTINENT] not in neighbouring_conts and map[origin][CONTINENT] != map[target][CONTINENT]: 
					neighbouring_conts.append(map[target][CONTINENT])
			if neighbouring_conts:
				best_cont = [0, -999999]
				for continent in neighbouring_conts:
					cont_nodes = self.get_continent_nodes(map, continent)
					cont_my_nodes = self.get_owned(map, cont_nodes)
					
					cont_armies = self.get_armies(map, cont_nodes)
					cont_my_armies = self.get_armies(map, cont_my_nodes)
					
					if cont_armies > 0: advantage = (map[origin][ARMY] + cont_my_armies * 2) - cont_armies
					else: advantage = len(cont_nodes)
					if advantage > best_cont[1] and (cont_armies > cont_my_armies > 0 or best_cont[0] == 0):
						best_cont = [continent, advantage]
						
				continent = best_cont[0]
					
				cont_nodes = self.get_continent_nodes(map, continent)
				cont_my_nodes = self.get_owned(map, cont_nodes)
					
				cont_armies = self.get_armies(map, cont_nodes)
				cont_my_armies = self.get_armies(map, cont_my_nodes)
				
				#print origin,neighbouring_conts,continent
				
				if map[origin][ARMY] * 1.5 > cont_armies - cont_my_armies:
				#pick neighbour in that cont with the least armies
					for target in neighbours:
						target_node = map[target]
						if target_node[OWNER] != self.player and origin_node[ARMY] * 0.75 > target_node[ARMY] < best_targ[1] and target_node[CONTINENT] == continent:
							best_targ = [target, target_node[ARMY]]

		if best_targ[0] != -1: 
			return [best_targ[0], int(origin_node[ARMY] * .9)]
		return 0
	def place(self, map):
		#return target
		my_borders = self.get_my_borders(map)
		#Place army in border with worst ratio my_armies : enemy_armies if ratio < 0.5
		#TODO: have a check to decide whether we really want to use armies to defend node
		#check: if 2 * cont_my_armies > cont_armies
		worst_ratio = [99999,0]
		for node in my_borders:
			continent = map[node][CONTINENT]
			cont_nodes = self.get_continent_nodes(map, continent)
			cont_my_nodes = self.get_owned(map, cont_nodes)
					
			cont_armies = self.get_armies(map, cont_nodes)
			cont_my_armies = self.get_armies(map, cont_my_nodes)
				
			if 2 * cont_my_armies > cont_armies:
				most_neigh_armies = 0
				for neigh in map[node][NEIGHBOURS]:
					if map[neigh][OWNER] != self.player and map[neigh][ARMY] > most_neigh_armies:
						ratio = (self.get_my_armies(map) / 100. + map[node][ARMY]) * 1. / map[neigh][ARMY]
						if ratio < worst_ratio[0]: worst_ratio = [ratio, node]
		if worst_ratio[0] < 0.5: return worst_ratio[1]

		#Place army in continent I don't own and best 'advantage'
		#TODO: include in this check bordering continents
		best_cont = [-1, -999999]
		for continent in range(len(self.bonus)):
			cont_nodes = self.get_continent_nodes(map, continent)
			cont_my_nodes = self.get_owned(map, cont_nodes)
			attackable_conts = []
			for border_node in my_borders:
				if map[border_node][CONTINENT] not in attackable_conts: attackable_conts.append(map[border_node][CONTINENT])
			#print attackable_conts
			if continent in attackable_conts:
				cont_armies = self.get_armies(map, cont_nodes)
				cont_my_armies = self.get_armies(map, cont_my_nodes)
				
				if cont_armies > 0: advantage = cont_my_armies - cont_armies * 2
				else: advantage = -999999
				
				if advantage > best_cont[1] and cont_armies != cont_my_armies:
					best_cont = [continent, advantage]
		if best_cont == -1:
			my_nodes = get_my_nodes(map)
			return random.choice(my_nodes)
		#target = random border node in best continent
		cont_nodes = self.get_continent_nodes(map, best_cont[0])
		targets = []
		for node in cont_nodes:
			if node in my_borders:
				targets.append(node)
		if targets == []:
			#if we have no nodes in that cont, select a node bordering it
			for border_node in my_borders:
				for neigh_node in map[border_node][NEIGHBOURS]:
					if map[neigh_node][CONTINENT] != map[border_node][CONTINENT]:
						targets.append(border_node)
			if targets == []: target = random.choice(my_borders)
			else: target = random.choice(targets)
			#if failure for some reason, just select random border node
		elif len(targets) == 1:
			target = targets[0]
		else:
			cont_my_nodes = self.get_owned(map, cont_nodes)
			#multiple potential nodes, choose one with biggest army
			#bordering enemy node in continent
			best_targ_pri = [-1, -1]
			#bordering any node
			best_targ_sec = [-1, -1]
			for target in targets:
				if map[target][ARMY] > best_targ_pri[1]:
					for neigh in map[target][NEIGHBOURS]:
						if neigh in cont_nodes and neigh not in cont_my_nodes:
							best_targ_pri= [target, map[target][ARMY]]
							break
					if map[target][ARMY] > best_targ_sec[1]:
						best_targ_sec = [target, map[target][ARMY]]
			if best_targ_pri[0] != -1:
				target = best_targ_pri[0]
			else:
				target = best_targ_sec[0]
		return target

class BOT6():
	#return list of all my nodes
	def get_my_nodes(self, map):
		my_nodes = []
		for node in range(len(map)):
			if map[node][OWNER] == self.player:
				my_nodes.append(node)
		return my_nodes
	#return number my armies
	def get_my_armies(self, map):
		my_armies = 0
		my_nodes = self.get_my_nodes(map)
		for node in my_nodes:
			my_armies += map[node][ARMY]
		return my_armies
	#return number enemy armies
	def get_enemy_armies(self, map):
		enemy_armies = 0
		for node in range(len(map)):
			if map[node][OWNER] != self.player:
				enemy_armies += map[node][ARMY]
		return enemy_armies
	#return list of my nodes neighbouring enemy nodes
	def get_my_borders(self, map):
		my_borders = []
		my_nodes = self.get_my_nodes(map)
		for node in my_nodes:
			neighbours = map[node][NEIGHBOURS]
			for neigh in neighbours:
				if map[neigh][OWNER] != self.player:
					my_borders.append(node)
					break
		return my_borders
	#return list of nodes in continent
	def get_continent_nodes(self, map, continent):
		continent_nodes = []
		for node in range(len(map)):
			if map[node][CONTINENT] == continent:
				continent_nodes.append(node)
		return continent_nodes
	#return nodes in list I own
	def get_owned(self, map, node_list):
		owned = []
		for node in node_list:
			if map[node][OWNER] == self.player:
				owned.append(node)
		return owned
	#return armies in node list
	def get_armies(self, map, node_list):
		armies = 0
		for node in node_list:
			armies += map[node][ARMY]
		return armies
	#REQUIRED PROCS
	def setup(self, map, bonus, player):
		#setup local variables
		self.bonus = bonus
		self.player = player
	def move_or_place(self, map):
		#return 'move' or 'place'
		for node in range(len(map)):
			if self.move(map, node, place_or_move_test = 1): return 'move'
		return 'place'
	def move(self, map, origin, place_or_move_test = 0):
		#return something invalid to cancel, or [target, armies]
		origin_node = map[origin]
		#check continent I'm in
		continent = origin_node[CONTINENT]
		
		#find total armies in continent
		cont_nodes = self.get_continent_nodes(map, continent)
		cont_my_nodes = self.get_owned(map, cont_nodes)
			
		cont_armies = self.get_armies(map, cont_nodes)
		cont_my_armies = self.get_armies(map, cont_my_nodes)
		
		best_targ = [-1, 9999999]
		neighbours = origin_node[NEIGHBOURS]
		#if all neighbours belong to us, move army to random one
		friendly = 1
		for target in neighbours:
			if map[target][OWNER] != self.player:
				friendly = 0
				break
		if friendly == 1 and not place_or_move_test:
			return [random.choice(neighbours), int(origin_node[ARMY] * .9)]
		#select neighbour with worst 'advantage' if sufficient armies in cont
		if cont_my_armies * 2 > cont_armies:
			#if we don't own continent, aim for neighbour in continent
			if cont_armies == cont_my_armies: own_cont = 1
			else: own_cont = 0
			for target in neighbours:
				target_node = map[target]
				target_neigh = target_node[NEIGHBOURS]
				owned_target_neigh = self.get_owned(map, target_neigh)
				owned_target_neigh_armies = self.get_armies(map, owned_target_neigh)
				#advantage = target_node[ARMY]
				advantage = target_node[ARMY] - owned_target_neigh_armies * 0.5
				if target_node[OWNER] != self.player and 0 > advantage < best_targ[1] and (target_node[CONTINENT] == continent or own_cont):
					best_targ = [target, advantage]
		#if we have insufficient armies to take and don't own continent, attack neigh cont w/ best advantage
		if not place_or_move_test and best_targ[0] == -1:
			#check all neighbouring continents, find one with best 'advantage'
			neighbouring_conts = []
			for target in neighbours:
				if map[target][CONTINENT] not in neighbouring_conts and map[origin][CONTINENT] != map[target][CONTINENT]: 
					neighbouring_conts.append(map[target][CONTINENT])
			if neighbouring_conts:
				best_cont = [0, -999999]
				for continent in neighbouring_conts:
					cont_nodes = self.get_continent_nodes(map, continent)
					cont_my_nodes = self.get_owned(map, cont_nodes)
					
					cont_armies = self.get_armies(map, cont_nodes)
					cont_my_armies = self.get_armies(map, cont_my_nodes)
					
					if cont_armies > 0: advantage = (map[origin][ARMY] + cont_my_armies * 2) - cont_armies
					else: advantage = len(cont_nodes)
					if advantage > best_cont[1] and (cont_armies > cont_my_armies > 0 or best_cont[0] == 0):
						best_cont = [continent, advantage]
						
				continent = best_cont[0]
					
				cont_nodes = self.get_continent_nodes(map, continent)
				cont_my_nodes = self.get_owned(map, cont_nodes)
					
				cont_armies = self.get_armies(map, cont_nodes)
				cont_my_armies = self.get_armies(map, cont_my_nodes)
				
				#print origin,neighbouring_conts,continent
				
				if map[origin][ARMY] * 1.5 > cont_armies - cont_my_armies:
				#pick neighbour in that cont with the least armies
					for target in neighbours:
						target_node = map[target]
						if target_node[OWNER] != self.player and origin_node[ARMY] * 0.75 > target_node[ARMY] < best_targ[1] and target_node[CONTINENT] == continent:
							best_targ = [target, target_node[ARMY]]

		if best_targ[0] != -1: 
			return [best_targ[0], int(origin_node[ARMY] * .9)]
		return 0
	def place(self, map):
		#return target
		my_borders = self.get_my_borders(map)
		#Place army in border with worst ratio my_armies : enemy_armies if ratio < 0.5
		#TODO: have a check to decide whether we really want to use armies to defend node
		#check: if 2 * cont_my_armies > cont_armies
		worst_ratio = [99999,0]
		for node in my_borders:
			continent = map[node][CONTINENT]
			cont_nodes = self.get_continent_nodes(map, continent)
			cont_my_nodes = self.get_owned(map, cont_nodes)
					
			cont_armies = self.get_armies(map, cont_nodes)
			cont_my_armies = self.get_armies(map, cont_my_nodes)
				
			if 2 * cont_my_armies > cont_armies:
				most_neigh_armies = 0
				for neigh in map[node][NEIGHBOURS]:
					if map[neigh][OWNER] != self.player and map[neigh][ARMY] > most_neigh_armies:
						ratio = (self.get_my_armies(map) / 100. + map[node][ARMY]) * 1. / map[neigh][ARMY]
						if ratio < worst_ratio[0]: worst_ratio = [ratio, node]
		if worst_ratio[0] < 0.0: return worst_ratio[1]

		#Place army in continent I don't own and best 'advantage'
		#TODO: include in this check bordering continents
		best_cont = [-1, -999999]
		for continent in range(len(self.bonus)):
			cont_nodes = self.get_continent_nodes(map, continent)
			cont_my_nodes = self.get_owned(map, cont_nodes)
			attackable_conts = []
			for border_node in my_borders:
				if map[border_node][CONTINENT] not in attackable_conts: attackable_conts.append(map[border_node][CONTINENT])
				for neigh_node in map[border_node][NEIGHBOURS]:
					if map[neigh_node][CONTINENT] not in attackable_conts: attackable_conts.append(map[neigh_node][CONTINENT])
			#print attackable_conts
			if continent in attackable_conts:
				cont_armies = self.get_armies(map, cont_nodes)
				cont_my_armies = self.get_armies(map, cont_my_nodes)
				
				if cont_armies > 0: advantage = 2 * cont_my_armies - cont_armies
				else: advantage = -999999
				
				if advantage > best_cont[1] and cont_armies != cont_my_armies:
					best_cont = [continent, advantage]
		if best_cont == -1:
			my_nodes = get_my_nodes(map)
			return random.choice(my_nodes)
		#target = random border node in best continent
		cont_nodes = self.get_continent_nodes(map, best_cont[0])
		targets = []
		for node in cont_nodes:
			if node in my_borders:
				targets.append(node)
		if targets == []:
			#if we have no nodes in that cont, select a node bordering it
			for border_node in my_borders:
				for neigh_node in map[border_node][NEIGHBOURS]:
					if map[neigh_node][CONTINENT] != map[border_node][CONTINENT]:
						targets.append(border_node)
			if targets == []: target = random.choice(my_borders)
			else: target = random.choice(targets)
			#if failure for some reason, just select random border node
		elif len(targets) == 1:
			target = targets[0]
		else:
			cont_my_nodes = self.get_owned(map, cont_nodes)
			#multiple potential nodes, choose one with biggest army
			#bordering enemy node in continent
			best_targ = [-1, -1]
			for target in targets:
				if map[target][ARMY] > best_targ[1]:
					for neigh in map[target][NEIGHBOURS]:
						if neigh in cont_nodes and neigh not in cont_my_nodes:
							best_targ = [target, map[target][ARMY]]
							break
			if best_targ[0] != -1:
				target = best_targ[0]
			else:
				target = random.choice(targets)
				print 1
		return target

class BOT7():
	#return list of all my nodes
	def get_my_nodes(self, map):
		my_nodes = []
		for node in range(len(map)):
			if map[node][OWNER] == self.player:
				my_nodes.append(node)
		return my_nodes
	#return number my armies
	def get_my_armies(self, map):
		my_armies = 0
		my_nodes = self.get_my_nodes(map)
		for node in my_nodes:
			my_armies += map[node][ARMY]
		return my_armies
	#return number enemy armies
	def get_enemy_armies(self, map):
		enemy_armies = 0
		for node in range(len(map)):
			if map[node][OWNER] != self.player:
				enemy_armies += map[node][ARMY]
		return enemy_armies
	#return list of my nodes neighbouring enemy nodes
	def get_my_borders(self, map):
		my_borders = []
		my_nodes = self.get_my_nodes(map)
		for node in my_nodes:
			neighbours = map[node][NEIGHBOURS]
			for neigh in neighbours:
				if map[neigh][OWNER] != self.player:
					my_borders.append(node)
					break
		return my_borders
	#return list of nodes in continent
	def get_continent_nodes(self, map, continent):
		continent_nodes = []
		for node in range(len(map)):
			if map[node][CONTINENT] == continent:
				continent_nodes.append(node)
		return continent_nodes
	#return nodes in list I own
	def get_owned(self, map, node_list):
		owned = []
		for node in node_list:
			if map[node][OWNER] == self.player:
				owned.append(node)
		return owned
	#return armies in node list
	def get_armies(self, map, node_list):
		armies = 0
		for node in node_list:
			armies += map[node][ARMY]
		return armies
	#REQUIRED PROCS
	def setup(self, map, bonus, player):
		#setup local variables
		self.bonus = bonus
		self.player = player
	def move_or_place(self, map):
		#return 'move' or 'place'
		for node in range(len(map)):
			if self.move(map, node, place_or_move_test = 1): return 'move'
		return 'place'
	def move(self, map, origin, place_or_move_test = 0):
		#return something invalid to cancel, or [target, armies]
		origin_node = map[origin]
		#check continent I'm in
		continent = origin_node[CONTINENT]
		
		#find total armies in continent
		cont_nodes = self.get_continent_nodes(map, continent)
		cont_my_nodes = self.get_owned(map, cont_nodes)
			
		cont_armies = self.get_armies(map, cont_nodes)
		cont_my_armies = self.get_armies(map, cont_my_nodes)
		
		best_targ = [-1, 9999999]
		neighbours = origin_node[NEIGHBOURS]
		#if all neighbours belong to us, move army to random one
		friendly = 1
		for target in neighbours:
			if map[target][OWNER] != self.player:
				friendly = 0
				break
		if friendly == 1 and not place_or_move_test:
			return [random.choice(neighbours), int(origin_node[ARMY] * .9)]
		#select neighbour with worst 'advantage' if sufficient armies in cont
		if cont_my_armies * 2 > cont_armies:
			#if we don't own continent, aim for neighbour in continent
			if cont_armies == cont_my_armies: own_cont = 1
			else: own_cont = 0
			for target in neighbours:
				target_node = map[target]
				target_neigh = target_node[NEIGHBOURS]
				owned_target_neigh = self.get_owned(map, target_neigh)
				owned_target_neigh_armies = self.get_armies(map, owned_target_neigh)
				#advantage = target_node[ARMY]
				advantage = target_node[ARMY] - owned_target_neigh_armies * 0.5
				if target_node[OWNER] != self.player and 0 > advantage < best_targ[1] and (target_node[CONTINENT] == continent or own_cont):
					best_targ = [target, advantage]
		#if we have insufficient armies to take and don't own continent, attack neigh cont w/ best advantage
		if not place_or_move_test and best_targ[0] == -1:
			#check all neighbouring continents, find one with best 'advantage'
			neighbouring_conts = []
			for target in neighbours:
				if map[target][CONTINENT] not in neighbouring_conts and map[origin][CONTINENT] != map[target][CONTINENT]: 
					neighbouring_conts.append(map[target][CONTINENT])
			if neighbouring_conts:
				best_cont = [0, -999999]
				for continent in neighbouring_conts:
					cont_nodes = self.get_continent_nodes(map, continent)
					cont_my_nodes = self.get_owned(map, cont_nodes)
					
					cont_armies = self.get_armies(map, cont_nodes)
					cont_my_armies = self.get_armies(map, cont_my_nodes)
					
					if cont_armies > 0: advantage = (map[origin][ARMY] + cont_my_armies * 2) - cont_armies
					else: advantage = len(cont_nodes)
					if advantage > best_cont[1] and (cont_armies > cont_my_armies > 0 or best_cont[0] == 0):
						best_cont = [continent, advantage]
						
				continent = best_cont[0]
					
				cont_nodes = self.get_continent_nodes(map, continent)
				cont_my_nodes = self.get_owned(map, cont_nodes)
					
				cont_armies = self.get_armies(map, cont_nodes)
				cont_my_armies = self.get_armies(map, cont_my_nodes)
				
				#print origin,neighbouring_conts,continent
				
				if map[origin][ARMY] * 1.5 > cont_armies - cont_my_armies:
				#pick neighbour in that cont with the least armies
					for target in neighbours:
						target_node = map[target]
						if target_node[OWNER] != self.player and origin_node[ARMY] * 0.75 > target_node[ARMY] < best_targ[1] and target_node[CONTINENT] == continent:
							best_targ = [target, target_node[ARMY]]

		if best_targ[0] != -1: 
			return [best_targ[0], int(origin_node[ARMY] * .9)]
	
		#still no attack, let's attack neighbour with least armies, if we can
		least_armies = 1e10
		best_node = -1
		neighbours = origin_node[NEIGHBOURS]
		for target in neighbours:
			if map[target][OWNER] != self.player and map[target][ARMY] < least_armies:
				best_node = target
				least_armies = map[target][ARMY]
		if best_node != -1 and least_armies < origin_node[ARMY] * .01:
			return [best_node, int(origin_node[ARMY] * .9)]
		return 0
	def place(self, map):
		#return target
		my_borders = self.get_my_borders(map)
		#Place army in border with worst ratio my_armies : enemy_armies if ratio < 0.5
		#TODO: have a check to decide whether we really want to use armies to defend node
		#check: if 2 * cont_my_armies > cont_armies
		worst_ratio = [99999,0]
		for node in my_borders:
			continent = map[node][CONTINENT]
			cont_nodes = self.get_continent_nodes(map, continent)
			cont_my_nodes = self.get_owned(map, cont_nodes)
					
			cont_armies = self.get_armies(map, cont_nodes)
			cont_my_armies = self.get_armies(map, cont_my_nodes)
				
			if 2 * cont_my_armies > cont_armies:
				most_neigh_armies = 0
				for neigh in map[node][NEIGHBOURS]:
					if map[neigh][OWNER] != self.player and map[neigh][ARMY] > most_neigh_armies:
						ratio = (self.get_my_armies(map) / 100. + map[node][ARMY]) * 1. / map[neigh][ARMY]
						if ratio < worst_ratio[0]: worst_ratio = [ratio, node]
		if worst_ratio[0] < 0.0: return worst_ratio[1]

		#Place army in continent I don't own and best 'advantage'
		#TODO: include in this check bordering continents
		best_cont = [-1, -999999]
		for continent in range(len(self.bonus)):
			cont_nodes = self.get_continent_nodes(map, continent)
			cont_my_nodes = self.get_owned(map, cont_nodes)
			attackable_conts = []
			for border_node in my_borders:
				if map[border_node][CONTINENT] not in attackable_conts: attackable_conts.append(map[border_node][CONTINENT])
				for neigh_node in map[border_node][NEIGHBOURS]:
					if map[neigh_node][CONTINENT] not in attackable_conts: attackable_conts.append(map[neigh_node][CONTINENT])
			#print attackable_conts
			if continent in attackable_conts:
				cont_armies = self.get_armies(map, cont_nodes)
				cont_my_armies = self.get_armies(map, cont_my_nodes)
				
				if cont_armies > 0: advantage = 2 * cont_my_armies - cont_armies
				else: advantage = -999999
				
				if advantage > best_cont[1] and cont_armies != cont_my_armies:
					best_cont = [continent, advantage]
		if best_cont == -1:
			my_nodes = get_my_nodes(map)
			return random.choice(my_nodes)
		#target = random border node in best continent
		cont_nodes = self.get_continent_nodes(map, best_cont[0])
		targets = []
		for node in cont_nodes:
			if node in my_borders:
				targets.append(node)
		if targets == []:
			#if we have no nodes in that cont, select a node bordering it
			for border_node in my_borders:
				for neigh_node in map[border_node][NEIGHBOURS]:
					if map[neigh_node][CONTINENT] != map[border_node][CONTINENT]:
						targets.append(border_node)
			if targets == []: target = random.choice(my_borders)
			else: target = random.choice(targets)
			#if failure for some reason, just select random border node
		elif len(targets) == 1:
			target = targets[0]
		else:
			cont_my_nodes = self.get_owned(map, cont_nodes)
			#multiple potential nodes, choose one with biggest army
			#bordering enemy node in continent
			best_targ = [-1, -1]
			for target in targets:
				if map[target][ARMY] > best_targ[1]:
					for neigh in map[target][NEIGHBOURS]:
						if neigh in cont_nodes and neigh not in cont_my_nodes:
							best_targ = [target, map[target][ARMY]]
							break
			if best_targ[0] != -1:
				target = best_targ[0]
			else:
				target = random.choice(targets)
				print 1
		return target

class RNDBOT():
	def setup(self, map, bonus, player):
		#setup local variables
		self.bonus = bonus
		self.player = player
	def move_or_place(self, map):
		#return 'move' or 'place'
		if random.random()<.5: return 'move' 
		else: return 'place'
	def move(self, map, origin):
		#return something invalid to cancel, or [target, armies]
		origin_node = map[origin]
		neighbours = origin_node[NEIGHBOURS]
		random.shuffle(neighbours)
		for target in neighbours:
			target_node = map[target]
			if target_node[OWNER] != self.player:
				break
		if origin_node[ARMY] > target_node[ARMY]:
			return [target, origin_node[ARMY]-1]
		return 0
	def place(self, map):
		#return target
		nodes = range(len(map))
		random.shuffle(nodes)
		for target in nodes:
			if map[target][OWNER] == self.player:
				return target
