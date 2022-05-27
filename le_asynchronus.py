import model
from model import nodes,n,neigh,message,edge_matrix, add_edge, attr_edge, remove_edge, graph

node_objects = []

class node(nodes):
	def __init__(self,unique_id,neighbours,n,edge_matrix):
		self.maxid = unique_id
		nodes.__init__(self,unique_id,neighbours,n,edge_matrix)
		self.id_message_id = 1

	def step(self):
		mes = self.read()
		if mes:
			# print("message = ", mes.content)
			if mes.unique_id == self.id_message_id:
				if mes.content > self.maxid:
					self.maxid = mes.content
		id_message = message(self.id_message_id,self.maxid)
		# i = random.choice(self.neighbours)
			# print(i)
		for i in self.neighbours:
			self.send(id_message,i)
			add_edge(self.id,i)
			attr_edge(self.id,i,color = 'red', penwidth = '5')
		graph()
		for i in self.neighbours:
			remove_edge(self.id,i)
			attr_edge(self.id,i)

# print(neigh)
# print(edge_matrix)
for i in range(n):
	node_objects.append(node(i,neigh[i],n,edge_matrix))
for i in range(n):
	node_objects[i].objects_list(node_objects)


model.start(node_objects)
for i in range(n):
	print("the maxid according to node", i, "is", node_objects[i].maxid, sep = " ")