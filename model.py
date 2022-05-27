import random
import sys
import graphviz
import os
import configparser
import copy

class message:
    ''' message object class'''
    def __init__(self, unique_id, content, wt = 0):
        self.unique_id = unique_id
        self.content = content
        self.edge_wt = wt


def attr_edge(node_1, node_2, color = 'black', style = 'solid', label = "", penwidth = '1', fontsize = '14', fontcolor = 'black'):
    ''' change the attributes of an edge'''
    if (node_1,node_2) not in edge_attrs:
        edge_attrs[(node_1,node_2)] = {}
    edge_attrs[(node_1,node_2)]['color'] = color
    edge_attrs[(node_1,node_2)]['style'] = style
    edge_attrs[(node_1,node_2)]['label'] = label
    edge_attrs[(node_1,node_2)]['penwidth'] = penwidth
    edge_attrs[(node_1,node_2)]['fontsize'] = fontsize 
    edge_attrs[(node_1,node_2)]['fontcolor'] = fontcolor 


def graph():
    ''' get a snap of the current network'''
    global count,node_objs, matrix,n,name
    filename = name+'/'+name+str(count).zfill(6)
    if flag:
        g = graphviz.Digraph('F', filename = filename, format = 'png', strict = 'True') 
    else:
        g = graphviz.Digraph('F', filename = filename, format = 'png')
    g.attr(label=algorithm)
    g.attr(fontsize = '100')
    for i in range(n):
        g.node(str(i),color = node_objs[i].colour,style = node_objs[i].style, fontsize = node_objs[i].fontsize)
    '''
    flag attribute
    0 ---- directed graph
    1 ---- undirected graph
    '''
    if flag:
        for i in range(n):
            for j in range(n):
                ''' attributes of the edges taken from the stored data'''
                col = 'black'
                if (i,j) in edge_attrs and 'color' in edge_attrs[(i,j)]:
                    col = edge_attrs[(i,j)]['color']
                elif (i,j) in edges and node_objs[i].level%2==0:
                    col = 'green'
                elif (i,j) in edges:
                    col = 'red'
                style = ""
                if (i,j) in edge_attrs and 'style' in edge_attrs[(i,j)]:
                    style = edge_attrs[(i,j)]['style']
                penwidth = '1'
                if (i,j) in edge_attrs and 'penwidth' in edge_attrs[(i,j)]:
                    penwidth = edge_attrs[(i,j)]['penwidth']	
                label = ""
                if (i,j) in edge_attrs and 'label' in edge_attrs[(i,j)]:
                    label = " " + edge_attrs[(i,j)]['label'] + " "
                fontsize = '14'
                if (i,j) in edge_attrs and 'fontsize' in edge_attrs[(i,j)]:
                    fontsize = edge_attrs[(i,j)]['fontsize']
                fontcolor = 'black'
                if (i,j) in edge_attrs and 'fontcolor' in edge_attrs[(i,j)]:
                    fontcolor = edge_attrs[(i,j)]['fontcolor']
                if (i,j) in edges:
                    g.edge(str(i),str(j),color = col, style = style, penwidth = penwidth,label = label,fontsize = fontsize,fontcolor = fontcolor)	
                else:
                    if matrix[i][j]:
                        # print('hi')
                        g.edge(str(i),str(j),dir = 'none',color = col,style = style,label = label,penwidth = penwidth,fontsize = fontsize, fontcolor = fontcolor)			
    else:
        for i in range(n):
            for j in range(n):
                if matrix[i][j]:
                    col = 'black'
                    if (i,j) in edge_attrs and 'color' in edge_attrs[(i,j)]:
                        col = edge_attrs[(i,j)]['color']
                    elif (i,j) in edges and node_objs[i].level%2==0:
                        col = 'green'
                    elif (i,j) in edges:
                        col = 'red'
                    style = ""
                    if (i,j) in edge_attrs and 'style' in edge_attrs[(i,j)]:
                        style = edge_attrs[(i,j)]['style']
                    penwidth = '1'
                    if (i,j) in edge_attrs and 'penwidth' in edge_attrs[(i,j)]:
                        penwidth = edge_attrs[(i,j)]['penwidth']	
                    fontsize = '14'
                    if (i,j) in edge_attrs and 'fontsize' in edge_attrs[(i,j)]:
                        fontsize = edge_attrs[(i,j)]['fontsize']
                    fontcolor = 'black'
                    if (i,j) in edge_attrs and 'fontcolor' in edge_attrs[(i,j)]:
                        fontcolor = edge_attrs[(i,j)]['fontcolor']
                    label = ""
                    if (i,j) in edge_attrs and 'label' in edge_attrs[(i,j)]:
                        label = " " + edge_attrs[(i,j)]['label'] + " "
                    g.edge(str(i),str(j),color = col, style = style, penwidth = penwidth,label = label,fontsize = fontsize,fontcolor = fontcolor)
                    
    count += 1
    g.render()

def add_edge(node_1,node_2):
    ''' add edges to the main list'''
    edges.append((node_1,node_2))
    if node_objs[node_1].level:
        node_objs[node_2].level = node_objs[node_1].level+1

def empty_edges():
    global edges
    for (u,v) in edges:
        attr_edge(u,v,style = 'invis')
    edges = []

def remove_edge(node_1,node_2):
    ''' remove edges from the main list'''
    edges.remove((node_1,node_2))

class scheduler:
    '''
    scheduler class object for picking nodes randomly
    '''
    def __init__(self, nodes, weights = None):
        self.nodes = nodes
        if weights:
            self.weights = weights
        else:
            self.weights = [1]*len(nodes)

    def pick(self):
        ''' picks a node everytime scheduler is called'''
        current_node = random.choices(self.nodes,weights = self.weights)
        return current_node[0]

class nodes:
    ''' main processor class'''
    def __init__(self,unique_id, neighbours,n,matrix):
        self.id = unique_id
        self.neighbours = neighbours
        self.inbox = []
        self.matrix = matrix
        self.number_of_nodes = n
        self.node_objects = []
        self.level = None
        self.colour = 'black'
        self.style = ""
        self.fontsize = '40'
        self.penwidth = '10'
        self.crashed  = False

    def objects_list(self, node_objects):

        ''' list of processor objects'''

        self.node_objects = node_objects

    def read(self):

        ''' returns the message object or message list'''

        global round_num
        if is_synch:
            if self.inbox:
                curr_messages = []
                while(self.inbox and self.inbox[0].content[-1]==round_num-1):
                    m = len(self.inbox[0].content)
                    self.inbox[0].content = self.inbox[0].content[:m-1]
                    curr_messages.append(self.inbox.pop(0))
                return curr_messages
        else:
            if self.inbox:
                curr_message = self.inbox.pop(0)
                return curr_message
        return None

    def crash(self,node = None):
        ''' crashing of the nodes '''
        global curr_crash, crash_probability
        crashed = False
        if curr_crash < crashes: 
            if node: # if a specific node is asked to crash
                crashed = True
                self.node_objects[node].crashed = True
            else:
                p = random.random()
                if p < crash_probability:
                    crashed = True
                    node = random.randint(1,n-1)
                    while self.node_objects[node].crashed:
                        node = random.randint(1,n-1)
                    self.node_objects[node].crashed = True
            if crashed: # visualizing a crashed node
                ''' colouring the node and removing all the edges around the node'''
                fp = open(logfile,"a")
                fp.write("Node "+str(node) +" crashed\n")
                fp.close()
                self.node_objects[node].color = "magenta"
                self.node_objects[node].style = "filled"

                for i in self.node_objects[node].neighbours:
                    if (self.node_objects[node].id,i) in edge_attrs:
                        edge_attrs[(self.node_objects[node].id,i)]['style'] = 'invis'
                    if (i,self.node_objects[node].id) in edge_attrs:
                        edge_attrs[(i,self.node_objects[node].id)]['style'] = 'invis'
            curr_crash += 1


    def send(self,curr_message,node):
        ''' updates the inbox of the receiver'''
        fp = open(logfile,"a")
        fp.write("sending message with message id " + str(curr_message.unique_id)+" from node "+str(self.id)+" to "+str(node)+'\n')
        fp.close()
        global round_num
        p = self.node_objects[node]
        if is_synch:
            curr = copy.copy(curr_message)
            message = list(curr.content)
            message.append(round_num)
            curr.content = message
            p.inbox.append(curr)
        else:
            p.inbox.append(curr_message)
'''
Parsing the configuration file
'''

print("Parsing the configuration file ..... ")
parser = configparser.ConfigParser()
parser.read('config.ini')
file = parser.get('INPUT','edge_file')
sched_file = parser.get('INPUT','scheduler_file')
flag = int(parser.get('INPUT','flag'))
runs = int(parser.get('INPUT','number_of_runs'))
algorithm = parser.get('INPUT','algorithm')
root = (parser.get('INPUT','fixed_root'))
synch = (parser.get('SYNCH','type'))
invis_edges = int(parser.get('INPUT','invisible_edges'))
is_synch = (synch == 'SYNCH')
crashes = int(parser.get('FAILURE','maximum_faulty_nodes'))
crash_probability = float(parser.get('FAILURE','crash_probability'))
logfile = parser.get('OUTPUT','log_file')
name = parser.get('OUTPUT','snap_folder')
video_name = parser.get('OUTPUT','video')
curr_crash = 0
os.system("rm -rf "+ name)
if root:
    given_root = int(root)
fp = open(file,'r')
f = open(logfile,"w")
f.close()
'''
private variables start
'''

edge_attrs = dict()
graph_name = name+'graph'
count = 0
graph_count = 0
l = (fp.readlines())
n = int(l[0])
matrix = [[None for _ in range(n)] for _ in range(n)]
edge_matrix = [[None for _ in range(n)] for _ in range(n)]
neigh = [[] for _ in range(n)]
edges = []
weights = []
round_num = 1
node_objs = []

'''
private variables end
'''

for line in l[1:]:
    e1,e2,wt = map(int,line.split())
    matrix[e1][e2] = wt
    edge_matrix[e1][e2] = wt
    neigh[e1].append(e2)
    if invis_edges: # if the edges are asked to be invisible
        edge_attrs[(e1,e2)] = {}
        edge_attrs[(e1,e2)]['style'] = 'invis'
    if flag: # if the graph is given as undirected
        edge_matrix[e1][e2] = wt
        edge_attrs[(e2,e1)] = {}
        neigh[e2].append(e1)
        if invis_edges:
            edge_attrs[(e2,e1)]['style'] = 'invis'
fp.close()
fp = open(sched_file,'r')

for i in fp.readlines()[:n]:
    weights.append(int(i))
fp.close()
sched = scheduler([i for i in range(n)],weights)

def visualize():
    ''' creating the video '''
    global name,video_name
    os.system("ffmpeg -y -framerate 1 -i "+name+'/'+name+"%06d.png "+video_name+" 2> test.txt")
    # os.system("rm -r "+name)
    os.system("xdg-open "+video_name)
def start(nodes):
    global round_num,n,matrix,node_objs
    node_objs = nodes

    for i in range(n):
        nodes[i].objects_list(node_objs)
    if root:
        nodes[given_root].isroot = True
        nodes[given_root].level = 1
    if not is_synch:
        ''' asynchronous system '''
        for i in range(runs):
            p = sched.pick()
            if not nodes[p].crashed:
                fp = open(logfile,"a")
                fp.write("Node "+str(p)+" is triggered\n")
                fp.close()
                nodes[p].step()
    else:
        ''' synchronous system '''
        for _ in range(runs):
            fp = open(logfile,"a")
            fp.write('\n')
            fp.write("Round "+str(round_num))
            fp.write('\n')
            for i in range(n):
                if not nodes[i].crashed:
                    fp = open(logfile,"a")
                    fp.write("Node "+str(i)+" is triggered\n")
                    fp.close()
                    nodes[i].round_num = round_num
                    nodes[i].step()
            round_num += 1

    
    visualize()

