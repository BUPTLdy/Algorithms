import numpy as np
class Edge(object):
    def __init__(self, u, v, w):
        self.source = u
        self.sink = v  
        self.capacity = w
    def __repr__(self):
        return "%s->%s:%s" % (self.source, self.sink, self.capacity)

class FlowNetwork(object):
    def __init__(self):
        self.adj = {}
        self.flow = {}
 
    def add_vertex(self, vertex):
        self.adj[vertex] = []
 
    def get_edges(self, v):
        return self.adj[v]
 
    def add_edge(self, u, v, w=0):
        if u == v:
            raise ValueError("u == v")
        edge = Edge(u,v,w)
        redge = Edge(v,u,0)
        edge.redge = redge
        redge.redge = edge
        self.adj[u].append(edge)
        self.adj[v].append(redge)
        self.flow[edge] = 0
        self.flow[redge] = 0
 
    def find_path(self, source, sink, path):
        if source == sink:
            return path
        for edge in self.get_edges(source):
            residual = edge.capacity - self.flow[edge]
            if residual > 0 and edge not in path:
                result = self.find_path( edge.sink, sink, path + [edge]) 
                if result != None:
                    return result
 
    def max_flow(self, source, sink):
        path = self.find_path(source, sink, [])
        while path != None:
            residuals = [edge.capacity - self.flow[edge] for edge in path]
            flow = min(residuals)
            for edge in path:
                self.flow[edge] += flow
                self.flow[edge.redge] -= flow
            path = self.find_path(source, sink, [])
        return sum(self.flow[edge] for edge in self.get_edges(source))

def get_max_flow(matrix):
    size=matrix.shape
    girls=range(1,size[0]+1)
    boys=np.array(range(1,size[1]+1))
    boys=-boys
    boys=list(boys)
    nodes=girls+boys
    nodes.append('s')
    nodes.append('t')
    #print nodes
    g=FlowNetwork()
    [g.add_vertex(v) for v in nodes]   
    for girl in girls:
        g.add_edge('s',girl,1)
    for boy in boys:
        g.add_edge(boy,'t',1) 
    g1=0
    for girl in girls:
        b=0
        for boy in boys:
            g.add_edge(girl,boy,matrix[g1][b])  
            b=b+1
        g1=g1+1
    
    return g.max_flow('s','t')

def getdata():
    data=f.readline()
    data=data.split(' ')
    size=map(int,data)
    return size
f=open('problem1.data')
line_len=len(f.readlines())
#print line_len
f.seek(0)
for i in xrange(3):
    f.readline()
num=3    
dataset_num=1
while num<line_len:
    size=getdata()
    matrix=np.zeros(size)
    num=num+size[0]+1
    for i in xrange(size[0]):
        data=getdata()
        #print data
        if data[0]!=0:
            for j in xrange(data[0]):
                matrix[i][data[j+1]-1]=1
    max_flow=get_max_flow(matrix)
    print 'In the %d_st dataset'%dataset_num,'there are %d girls and %d boys,'%(size[0],size[1]),\
    'and the maximum pairs is %d'%max_flow
    dataset_num=dataset_num+1
   
        

