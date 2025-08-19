# pi0_hybrid_ops.py  
  
def L_operator(psi_in: QuantumState, salt_delay: int) -> (QuantumState, ContractHdr):  
    '''  
    Applies U_enc, returns transformed state and salted header.  
    '''  
    psi_L = U_enc @ psi_in @ U_enc.dag()  
    header = salt_header(current_time()+salt_delay)  
    return psi_L, header  
  
def N_operator(psi_L: QuantumState, weights: Matrix, alphas: List[float]) -> (QuantumState, DraftToken):  
    '''  
    Applies expansion and emits a draft token for negotiation.  
    '''  
    psi_N = sigma(weights @ psi_L) + sum(alpha*F_k(psi_L) for alpha, F_k in zip(alphas, fractal_ops))  
    draft = DraftToken(generate_id('N'))  
    return psi_N, draft  
  
def C_operator(psi_N: QuantumState, reference: QuantumState, keys: Tuple[Key,Key]) -> (QuantumState, SealedToken):  
    '''  
    Applies penalty calculus, seals under 2-key encryption.  
    '''  
    penalty = -eta*kl_divergence(psi_N, reference) - kappa*(psi_N.norm()**4)  
    psi_C = psi_N + penalty  
    sealed = SealedToken(seal_id=generate_id('C'), keys=keys)  
    return psi_C, sealed  
  
def M_operator(psi_C: QuantumState, keys: Tuple[Key,Key]) -> (QuantumState, ClosedToken):  
    '''  
    Normalizes state, finalizes contract under 2-of-2 keys.  
    '''  
    psi_M = psi_C / psi_C.norm(m_metric)  
    closed = ClosedToken(close_id=generate_id('M'), keys=keys)  
    return psi_M, closed  