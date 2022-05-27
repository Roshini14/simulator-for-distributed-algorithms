import model
from model import message,nodes,n,neigh,edge_matrix,add_edge,remove_edge, attr_edge, graph
import random
from math import inf
node_objects = []

class node(nodes):
	def __init__(self,unique_id,neighbours,n,edge_matrix):
		''' extended class from nodes '''
		
		self.id = unique_id
		nodes.__init__(self,unique_id,neighbours,n,edge_matrix)
		self.distance_id = 1
		self.invited = False
		self.parent = None
		self.isroot = False
		self.child = []
		self.distance = inf
		
	def step(self):

		if self.isroot:
			'''code for the root node'''
			self.distance = 0
			distance_msg = message(self.distance_id,(self.id,self.distance))
			for i in self.neighbours:
				self.send(distance_msg,i)
		else:
			'''code for non root nodes'''
			mes = self.read()
			if mes:
				'''if a message is received by the node'''
				if mes.unique_id == self.distance_id:
					p,d = mes.content
					if d+1 < self.distance:
						self.distance = d + 1
						if self.parent:
							remove_edge(self.parent,self.id)
							attr_edge(self.parent,self.id)
						self.parent = p
						add_edge(p,self.id)
						''' coloring the nodes based on the level of the node'''
						color = 'red'
						if self.level % 2:
							color = 'green'
						attr_edge(p,self.id, color = color, penwidth = '5')
						distance_msg = message(self.distance_id,(self.id,self.distance))
						for i in self.neighbours:
							self.send(distance_msg,i)
						'''getting a snap of the network'''
						graph()

for i in range(n):
	node_objects.append(node(i,neigh[i],n,edge_matrix))
model.start(node_objects)

