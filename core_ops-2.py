# core_ops.py  
  
# Drift: A^T x  
def drift(x, A):  
    n = len(x)  
    out = [0.0]*n  
    for i in range(n):  
        s = 0.0  
        for j in range(n):  
            s += A[j][i] * x[j]  
        out[i] = s  
    return out  
  
# ReLU  
def relu(v):  
    return [v_i if v_i>0 else 0.0 for v_i in v]  
  
# Expansion: W2·ReLU(W1·x)  
def expand(x, W1, W2):  
    n = len(x)  
    tmp = [0.0]*n  
    for i in range(n):  
        s = 0.0  
        for j in range(n):  
            s += W1[i][j]*x[j]  
        tmp[i] = s if s>0 else 0.0  
    out = [0.0]*n  
    for i in range(n):  
        s = 0.0  
        for j in range(n):  
            s += W2[i][j]*tmp[j]  
        out[i] = s  
    return out  
  
# Collapse: -ε·x⊙x  
def collapse(x, eps):  
    return [-eps*(v*v) for v in x]  
  
# Normalize: x/||x||2  
import math  
def normalize(x):  
    norm = math.sqrt(sum(v*v for v in x)) + 1e-12  
    return [v/norm for v in x]  
  
# One update step  
def update(x, A, W1, W2, eps):  
    d = drift(x, A)  
    e = expand(d, W1, W2)  
    c = collapse(x, eps)  
    y = [d_i + e_i + c_i for d_i,e_i,c_i in zip(d,e,c)]  
    return normalize(y)  