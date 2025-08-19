
import numpy as np
def q_cov_theta(wigner_tensor, metric='FRW'):
    return float(np.var(wigner_tensor))
