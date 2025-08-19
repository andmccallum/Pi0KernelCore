# A. CONFIG & KEYS  
CONFIG = {...}  
  
# B. Init QGCM  
def init_qgcm(config):  
    return QGCM_Instance(config.get('qgcm_params', {}))  
  
# C–E. Core updates  
def step_classical(...)  
def compute_markers(...)  
def center_check(...)  
  
# F. MAC computation  
def hmac_state(...)  
  
# G. Audit logger  
def audit_log(entry): ...  
  
# H. Secure timestep  
def secure_step(state):  
    t0 = time.time()  
    s_new = step_classical(...)  
    m_new = compute_markers(s_new)  
    assert center_check(m_new, state['m0'])  
    rho_new = state['qgcm'].evolve_quantum(state['qgcm_rho'], dt)  
    mac = hmac_state(s_new.tobytes(), m_new.tobytes(), CONFIG['HMAC_KEY'])  
    entry = {'time':t0, 's':s_new.tolist(), 'm':m_new.tolist(),  
             'C_center':float(CONFIG['W'].dot(m_new-state['m0'])), 'mac':mac.hex()}  
    audit_log(entry)  