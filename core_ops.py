# core_ops.py  
  
import math  
  
def drift(x, A):  
    """L[x] = Aᵀ · x  (graph drift)"""  
    n = len(x)  
    out = [0.0]*n  
    for i in range(n):  
        s = 0.0  
        for j in range(n):  
            s += A[j][i]*x[j]  
        out[i] = s  
    return out  
  
def expand(x, W1, W2):  
    """N[x] = W2 · ReLU(W1 · x)  (nonlinear expansion)"""  
    n = len(x)  
    # W1·x  
    tmp = [0.0]*n  
    for i in range(n):  
        s = 0.0  
        for j in range(n):  
            s += W1[i][j]*x[j]  
        tmp[i] = s if s>0 else 0.0  
    # W2·tmp  
    out = [0.0]*n  
    for i in range(n):  
        s = 0.0  
        for j in range(n):  
            s += W2[i][j]*tmp[j]  
        out[i] = s  
    return out  
  
def collapse(x, eps):  
    """C[x] = -ε · (x⊙x)  (superposition penalty)"""  
    return [-eps*(xi*xi) for xi in x]  
  
def normalize(x, eps_norm=1e-12):  
    """M[x] = x/||x||₂  (stability)"""  
    sum_sq = eps_norm  
    for xi in x:  
        sum_sq += xi*xi  
    norm = math.sqrt(sum_sq)  
    return [xi/norm for xi in x]  
  
def update_vector(x, A, W1, W2, eps):  
    """One update step: x → M(x + N(L(x)) + C(x))"""  
    d = drift(x, A)  
    e = expand(d, W1, W2)  
    c = collapse(x, eps)  
    y = [d_i + e_i + c_i for d_i,e_i,c_i in zip(d,e,c)]  
    return normalize(y)  