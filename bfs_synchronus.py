import model
from model import message, nodes,n,neigh,edge_matrix,add_edge,remove_edge, graph, attr_edge
import random
from math import inf
node_objects = []

class node(nodes):
	def __init__(self,unique_id,neighbours,n,edge_matrix):
		self.id = unique_id
		nodes.__init__(self,unique_id,neighbours,n,edge_matrix)
		self.distance_id = 1
		self.invited = False
		self.parent = None
		self.isroot = False
		self.child = []
		self.distance = inf
		self.invite_id = 2
		self.invite = message(self.invite_id, [self.id])
		self.accept_id = 3
		self.accept = message(self.accept_id, [self.id])

	def step(self):

		if self.isroot:
			for i in self.neighbours:
				self.invited = True
				self.send(self.invite,i)
				self.child.append(i)
		else:
			mes_list = self.read()
			if mes_list:
				for mes in mes_list:
					if mes.unique_id == self.invite_id and not self.invited:
						# print(mes.content,self.unique_id)
						self.invited = True
						self.send(self.accept,mes.content[0])
						for i in self.neighbours:
							if i != mes.content[0]:
								self.send(self.invite,i)
						add_edge(mes.content[0],self.id)
						col = 'red'
						if self.level%2 == 0:
							col = 'green'
						attr_edge(mes.content[0],self.id,color = col, penwidth = '5')
					if mes.unique_id == self.accept_id:
						self.child.append(mes.content[0])
				graph()
for i in range(n):
	node_objects.append(node(i,neigh[i],n,edge_matrix))
for i in range(n):
	node_objects[i].objects_list(node_objects)
model.start(node_objects)
