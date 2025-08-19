# pi0_system.py  
  
import math  
  
# — Core Vector Primitives —   
def drift(x, A):  
    """L[x] = Aᵀ·x  (graph drift)"""  
    n = len(x)  
    out = [0.0]*n  
    for i in range(n):  
        s = 0.0  
        for j in range(n):  
            s += A[j][i]*x[j]  
        out[i] = s  
    return out  
  
def expand(x, W1, W2):  
    """N[x] = W2·ReLU(W1·x)  (nonlinear expansion)"""  
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
  
def collapse(x, eps):  
    """C[x] = –ε·(x⊙x)  (superposition penalty)"""  
    return [-eps*(xi*xi) for xi in x]  
  
def normalize(x, eps_norm=1e-12):  
    """M[x] = x/||x||₂  (stability)"""  
    sum_sq = eps_norm  
    for xi in x:  
        sum_sq += xi*xi  
    norm = math.sqrt(sum_sq)  
    return [xi/norm for xi in x]  
  
def update_vector(x, A, W1, W2, eps):  
    """  
    One step: x_{t+1} = M(x_t + N(L(x_t)) + C(x_t))  
    """  
    d = drift(x, A)  
    e = expand(d, W1, W2)  
    c = collapse(x, eps)  
    y = [d_i + e_i + c_i for d_i,e_i,c_i in zip(d,e,c)]  
    return normalize(y)  
  
&nbsp;  
 # — Quantum-Calculus Primitives —   
def lift_density(x):  
    """ρ = diag(x)"""  
    n = len(x)  
    return [[x[i] if i==j else 0.0 for j in range(n)] for i in range(n)]  
  
def matmul(A, B):  
    """Matrix multiply A·B"""  
    n = len(A)  
    C = [[0.0]*n for _ in range(n)]  
    for i in range(n):  
        for j in range(n):  
            s = 0.0  
            for k in range(n):  
                s += A[i][k]*B[k][j]  
            C[i][j] = s  
    return C  
  
def transpose(A):  
    """Transpose of A"""  
    n = len(A)  
    return [[A[j][i] for j in range(n)] for i in range(n)]  
  
def trace(M):  
    """Trace of M"""  
    return sum(M[i][i] for i in range(len(M)))  
  
def commutator(A, B):  
    """[A,B] = A·B − B·A"""  
    return [[AB - BA for AB,BA in zip(ARow, BRow)]   
            for ARow,BRow in zip(matmul(A,B), matmul(B,A))]  
  
def Q_correction(rho, A, W1, W2, eps):  
    """  
    Q_q = Tr([N_rho, C_rho]·rho)  
    where N_rho and C_rho lift classical expansion and collapse.  
    """  
    # L_rho = Aᵀ·ρ·A  
    At = transpose(A)  
    Ar = matmul(At, rho)  
    Lrho = matmul(Ar, A)  
    # N_rho  
    n = len(A)  
    tmp = [[0.0]*n for _ in range(n)]  
    for i in range(n):  
        for j in range(n):  
            s = 0.0  
            for k in range(n):  
                s += W1[i][k]*Lrho[k][j]  
            tmp[i][j] = s if s>0 else 0.0  
    Nrho = matmul(matmul(W2, tmp), transpose(W2))  
    # C_rho  
    Crho = matmul(rho, rho)  
    for i in range(n):  
        for j in range(n):  
            Crho[i][j] *= -eps  
    # commutator and trace  
    comm = commutator(Nrho, Crho)  
    QC = 0.0  
    for i in range(n):  
        for j in range(n):  
            QC += comm[i][j]*rho[j][i]  
    return QC  