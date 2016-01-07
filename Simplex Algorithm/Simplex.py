# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 18:15:27 2015

@author: Ldy
"""
import numpy as np
import time
def Pivot(N,B,A,b,c,v,l,e):
    A_=np.zeros(A.shape)
    b_=np.zeros(b.shape)
    c_=np.zeros(c.shape)
    b_[e]=b[l]/A[l][e]
    for j in N-{e}:
        A_[e][j]=A[l][j]/A[l][e]
    A_[e][l]=1.0/A[l][e]
    for i in B-{l}:
        b_[i]=b[i]-A[i][e]*b_[e]
        for j in N-{e}:
            A_[i][j]=A[i][j]-A[i][e]*A_[e][j]
        A_[i][l]=-A[i][e]*A_[e][l]
    v=v+c[e]*b_[e]
    for j in N-{e}:
        c_[j]=c[j]-c[e]*A_[e][j]
    c_[l]=-c[e]*A_[e][l]
    N=N-{e}|{l}
    B=B-{l}|{e}
    return N,B,A_,b_,c_,v
    
def Simplex(N,B,A,b,c,v):
    e=0
    l=0
    temp=[]
    det=np.zeros(b.shape)
    while True in (c>0):
        for i in N:
            if c[i]>0:
                e=i
                break
        for i in B:
            if A[i][e]>0:
                det[i]=b[i]/A[i][e]
            else:
                det[i]=float("inf")
        for i in B:
            temp.append(det[i])  
        det=list(det)
        l=det.index(min(temp))
        if det[l]==float("inf"):
            print 'unbounded'
        else:
            N,B,A,b,c,v=Pivot(N,B,A,b,c,v,l,e)
    x=np.zeros(b.shape)
    for i in xrange(b.shape[0]):
        if i in B:
            x[i]=b[i]
    return v,x
            

A=np.array([\
[0.0,0,0,0,0,0,0],\
[0,0,0,0,0,0,0],\
[0,0,0,0,0,0,0],\
[0,0,0,0,0,0,0],\
[0,1,1,3,0,0,0],\
[0,2,2,5,0,0,0],\
[0,4,1,2,0,0,0]
])
b=np.array([0.0,0,0,0,30,24,36])
c=np.array([0.,3,1,2,0,0,0])
N=set([1,2,3])
B=set([4,5,6])
l=6
e=1
v=0.

start=time.clock()
v,x=Simplex(N,B,A,b,c,v)
end=time.clock()
times_cost=end-start
print 'The maxinum value is: ',v
print 'The value of var is: ',x[1:]
print 'Cost time: ',times_cost,'seconds'













    
    