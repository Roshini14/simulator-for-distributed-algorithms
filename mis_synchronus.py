import model
from model import message,nodes,n,neigh,edge_matrix, colour_node
import random
from math import inf
node_objects = []

class node(nodes):
	def __init__(self,unique_id,neighbours,n,edge_matrix):
		self.id = unique_id
		nodes.__init__(self,unique_id,neighbours,n,edge_matrix)
		self.status = 'undecided'
		self.marked = False
		self.degree = len(neighbours)
		self.rank_id = 1
		self.mis_id = 2
		
		self.rank = random.uniform(0,1)
	def step(self):
		if self.status == 'undecided':
			if self.degree == 0:
				self.status = 'YES'
				colour_node(self.id,'red')
			else:
				self.marked = True
				rank_mes = message(self.rank_id, (self.rank,self.id))
				for i in self.neighbours:
					self.send(rank_mes, i)
			mes_list = self.read()
			if mes_list:
				# print(self.id)
				for mes in mes_list:
					# print(mes.unique_id,mes.content)
					if mes.unique_id == self.rank_id:
						rank, sender = mes.content
						if rank < self.rank:
							self.marked = False
							self.rank = random.uniform(0,1)
					else:
						self.status = 'NO'
						self.marked = False
				if self.marked:
					colour_node(self.id,'red')
					self.status = 'YES'

					mis_mes = message(self.mis_id, (self.rank,self.id))
					for i in self.neighbours:
						self.send(mis_mes,i)
		if self.status == 'YES':
			colour_node(self.id,'red')
			mis_mes = message(self.mis_id, (self.rank,self.id))
			for i in self.neighbours:
				self.send(mis_mes,i)


# print(neigh)
# print(edge_edge_matrix)
for i in range(n):
	# print(i,neigh[i])
	node_objects.append(node(i,neigh[i],n,edge_matrix))
for i in range(n):
	node_objects[i].objects_list(node_objects)
model.start(node_objects)
# for i in range(n):
# 	print("the maxid according to node", i, "is", node_objects[i].maxid, sep = " ")