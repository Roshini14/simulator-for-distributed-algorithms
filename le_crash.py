import model
from model import message,nodes,n,neigh,edge_matrix,empty_edges, attr_edge, graph, add_edge, visualize, remove_edge
import random
from math import log2,sqrt
from collections import Counter
node_objects = []

class node(nodes):
    def __init__(self,unique_id,neighbours,n,edge_matrix):
        self.id = unique_id
        nodes.__init__(self,unique_id,neighbours,n,edge_matrix)
        self.prob = 2*log2(n)/n
        l = [i for i in range(1,n**4)]
        self.status = 'undecided'
        self.rank = random.choice(l)
        if random.uniform(0,1) > self.prob:
            self.advert_id = 1
            self.advert_msg = message(self.advert_id,(self.id,self.rank))
        else:
            self.status = 'NON-ELECTED'
        self.num = int(2*sqrt(n*log2(n)))
        self.winner_id = 2
        self.winner_msg = message(self.winner_id,"you won")

    def step(self):
        if not self.crashed:
            if self.status != 'NON-ELECTED':
                if self.round_num%3 == 1:
                    neighbours = random.choices(self.neighbours,k = self.num)
                    for i in neighbours:
                        if self.node_objects[i].crashed:
                            neighbours.remove(i)
                    items = Counter(neighbours).keys()
                    self.num = len(items)
                    for i in neighbours:
                        self.send(self.advert_msg,i)
                        add_edge(self.id,i)
                        attr_edge(self.id, i, style = "solid", color = 'red', penwidth = '5')
                    self.crash()
                    graph()
                    for i in neighbours:
                        remove_edge(self.id,i)
                        attr_edge(self.id, i, style = 'invis')

            if self.round_num%3 == 2:
                msg_list = self.read()
                if msg_list:
                    u,max_r = 0,0
                    for msg in msg_list:
                        if msg.content[1] > max_r:
                            u,max_r = msg.content
                    self.crash()
                    self.send(self.winner_msg,u)
                    add_edge(self.id,u)
                    attr_edge(self.id, u, color = 'green', style = 'solid',penwidth = '5')
                    graph()
                    
            if self.round_num%3 == 0:
                msg_list = self.read()

                if msg_list:
                    if len(msg_list) == self.num:
                        self.status = 'ELECTED'
                        print('winner',self.id)
                        self.color = 'yellow'
                        self.style = 'filled'
                        graph()
                        print("exiting the algorithm....")
                        visualize()
                        exit()
                    else:
                        self.crash()
                else:
                    self.crash()
                empty_edges()
                
for i in range(n):
    node_objects.append(node(i,neigh[i],n,edge_matrix))
model.start(node_objects)
print("nodes can't agree on a leader")