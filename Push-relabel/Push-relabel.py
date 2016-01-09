import numpy as np
Inf=float('inf')

def relabel_to_front(C, source, sink):
     n = len(C) # C is the capacity matrix
     #print n
     F = [[0] * n for _ in xrange(n)]
     #print F
     # residual capacity from u to v is C[u][v] - F[u][v]

     height = [0] * n # height of node
     excess = [0] * n # flow into node minus flow from node
     seen   = [0] * n # neighbours seen since last relabel
     # node "queue"
     nodelist = [i for i in xrange(n) if i != source and i != sink]
     #print nodelist
     def push(u, v):
         send = min(excess[u], C[u][v] - F[u][v])
         F[u][v] += send
         F[v][u] -= send
         excess[u] -= send
         excess[v] += send

     def relabel(u):
         min_height = Inf
         for v in xrange(n):
             if C[u][v] - F[u][v] > 0:
                 min_height = min(min_height, height[v])
                 height[u] = min_height + 1

     def discharge(u):
         while excess[u] > 0:
             if seen[u] < n: # check next neighbour
                 v = seen[u]
                 if C[u][v] - F[u][v] > 0 and height[u] > height[v]:
                     push(u, v)
                 else:
                     seen[u] += 1
             else: # we have checked all neighbours. must relabel
                 relabel(u)
                 seen[u] = 0

     height[source] = n   # longest path from source to sink is less than n long
     excess[source] = Inf # send as much flow as possible to neighbours of source
     for v in xrange(n):
         push(source, v)

     p = 0
     while p < len(nodelist):
         u = nodelist[p]
         old_height = height[u]
         discharge(u)
         if height[u] > old_height:
             nodelist.insert(0, nodelist.pop(p)) # move to front of list
             p = 0 # start from front of list
         else:
             p += 1

     return F#,sum(F[source])
     
def getdata():
    data=f.readline()
    data=data.split(' ')
    size=map(int,data)
    return size
f=open('problem2.data')
line_len=len(f.readlines())
f.seek(0)
for i in xrange(3):
    f.readline()
num=3   
dataset_mun=1
while num<line_len:
    size=getdata()
    col_sum=getdata()
    row_sum=getdata()
    num=num+3
    matrix_size=size[0]*size[1]+2
    #print matrix_size
    matrix=np.zeros((matrix_size,matrix_size),dtype=np.int)
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            matrix[i][size[0]+j]=1
    for i in xrange(size[0]):
        matrix[matrix_size-2][i]=col_sum[i]
    for j in xrange(size[1]):
        matrix[size[0]+j][matrix_size-1]=row_sum[j]
    F=relabel_to_front(matrix,matrix_size-2,matrix_size-1)
    result_matrix=np.zeros(size,dtype=np.int)
    
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            result_matrix[i][j]=F[i][size[0]+j]
    result_col_sum=np.sum(result_matrix,axis=1)
    result_row_sum=np.sum(result_matrix,axis=0)
    
    print 'The %d_st matrix is:'%dataset_mun
    print result_matrix
    print 'the sum of rows are:'
    print result_col_sum
    print 'the sum of columns are:'
    print result_row_sum
    dataset_mun=dataset_mun+1







