import model
from model import message,nodes,n,neigh,edge_matrix,add_edge,remove_edge, attr_edge, graph
node_objects = []

class node(nodes):
	def __init__(self,unique_id,neighbours,n,edge_matrix):
		self.id = unique_id
		nodes.__init__(self,unique_id,neighbours,n,edge_matrix)
		self.message_id = 1
		self.parent = None
		self.child = []
		self.isroot = False
		self.message = message(self.message_id,("hello",self.id))
	def step(self):
		''' code for root node '''
		if self.isroot and self.parent == None:
			self.parent = self.id
			for i in self.neighbours:
				self.send(self.message,i)
				add_edge(self.id,i)
				attr_edge(self.id,i,color = 'red',penwidth = '5')
			graph()
			for i in self.neighbours:
				remove_edge(self.id,i)
				attr_edge(self.id, i)

		else:
			''' code for non root node '''
			mes = self.read()
			if mes:
				if mes.unique_id == self.message_id:
					if self.parent == None:
						msg, p = mes.content
						''' marking the parent as p'''
						self.parent = p
						self.node_objects[p].child.append(self.id)
						
						for i in self.neighbours:
							self.send(self.message,i)
							add_edge(self.id,i)
							attr_edge(self.id,i,color = 'red',penwidth = '5')

						graph()
						for i in self.neighbours:
							remove_edge(self.id,i)
							attr_edge(self.id, i)
					''' coloring the tree edges in green '''
					attr_edge(self.parent,self.id,color = 'green',penwidth = '5')


for i in range(n):
	node_objects.append(node(i,neigh[i],n,edge_matrix))
model.start(node_objects)