# quantum_ops.py  
  
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
            s=0.0  
            for k in range(n):  
                s += A[i][k]*B[k][j]  
            C[i][j] = s  
    return C  
  
def trace(M):  
    """Trace of M"""  
    return sum(M[i][i] for i in range(len(M)))  
  
def commutator(A, B):  
    """[A,B] = A·B − B·A"""  
    AB = matmul(A, B)  
    BA = matmul(B, A)  
    n=len(A)  
    return [[AB[i][j] - BA[i][j] for j in range(n)] for i in range(n)]  
  
def Q_correction(rho, A, W1, W2, eps):  
    """  
    Compute Q_q = Tr([N_rho, C_rho] · rho)  
    where  
      N_rho[rho] = W2·ReLU(W1·(Aᵀ·rho·A))·W2ᵀ  
      C_rho[rho] = -eps * rho·rho  
    """  
    # Build Aᵀ·rho·A  
    Arho = matmul([[A[j][i] for j in range(len(A))] for i in range(len(A))], rho)  
    Lrho = matmul(Arho, A)  
    # N_rho  
    tmp = [[0.0]*len(A) for _ in range(len(A))]  
    for i in range(len(A)):  
        for j in range(len(A)):  
            s=0.0  
            for k in range(len(A)):  
                s += W1[i][k]*Lrho[k][j]  
            tmp[i][j] = s if s>0 else 0  
    Nrho = matmul(matmul(W2, tmp), transpose(W2))  
    # C_rho  
    Crho = matmul(rho, rho)  
    for i in range(len(A)):  
        for j in range(len(A)):  
            Crho[i][j] *= -eps  
    # Commutator and trace  
    comm = commutator(Nrho, Crho)  
    QC = 0.0  
    for i in range(len(A)):  
        for j in range(len(A)):  
            QC += comm[i][j]*rho[j][i]  
    return QC  