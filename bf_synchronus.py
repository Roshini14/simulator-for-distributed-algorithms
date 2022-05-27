import model
from model import message,nodes,n,neigh,edge_matrix, colour_node, attr_edge, graph, add_edge, remove_edge
from math import inf
node_objects = []

class node(nodes):
	def __init__(self,unique_id,neighbours,n,matrix):
		self.id = unique_id
		nodes.__init__(self,unique_id,neighbours,n,matrix)
		self.a = inf
		self.parent = None
		self.isroot = False
		self.a_id = 1

	def step(self):
		if self.isroot:
			self.a = 0
			self.parent = self.id
		for i in self.neighbours:
			self.a_message = message(self.a_id,(self.a,self.id))
			self.send(self.a_message,i)
		mes_list = self.read()
		if mes_list:
			# print(self.)
			for mes in mes_list:
				a, parent = mes.content
				wt = edge_matrix[parent][self.id]
				if a + wt < self.a:
					if self.a != inf:
						remove_edge(self.parent,self.id)
						attr_edge(self.parent,self.id,style = 'invis')
					self.a = a + wt
					self.parent = parent
					add_edge(self.parent,self.id)
					attr_edge(self.parent,self.id,color = 'red',style = 'solid', penwidth = '5', label = str(self.a),fontsize = '40',fontcolor = 'green')
					graph()


# print(neigh)
# print(matrix)
for i in range(n):
	# print(i,neigh[i])
	node_objects.append(node(i,neigh[i],n,matrix))
for i in range(n):
	node_objects[i].objects_list(node_objects)
model.start(node_objects)
# for i in range(n):
# 	print("the maxid according to node", i, "is", node_objects[i].maxid, sep = " ")