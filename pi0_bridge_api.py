# pi0_bridge_api.py  
  
def create_contract(header_blob: bytes, approvers: List[UserID]) -> ContractID:  
    '''  
    Stage 1: Initializes contract. Records header as encrypted audit entry.  
    '''  
    cid = generate_cid()  
    audit.log_hidden(cid, 'create', header_blob)  
    state[cid] = { 'votes': set(), 'header': header_blob }  
    return cid  
  
def approve_contract(cid: ContractID, user: UserID) -> bool:  
    '''  
    Records an approver’s vote. Once quorum reached, unlocks next operator.  
    '''  
    state[cid]['votes'].add(user)  
    audit.log_hidden(cid, 'approve', user)  
    if len(state[cid]['votes']) >= quorum(cid):  
        state[cid]['approved'] = True  
    return state[cid]['approved']  
  
def execute_operator(cid: ContractID, op: str, psi: QuantumState) -> QuantumState:  
    '''  
    Executes L/N/C/M only if approved. Emits tokens to audit.  
    '''  
    if not state[cid].get('approved'):  
        raise PermissionError('Quorum not reached')  
    operator = get_operator(op, state[cid])  
    psi_out, token = operator(psi)  
    audit.log_hidden(cid, op, token)  
    return psi_out  
  
def get_audit(cid: ContractID, auditor_key: Key) -> List[AuditEntry]:  
    '''  
    Returns decrypted audit trail only for authorized auditors.  
    '''  
    if not auditor_key in regulators:  
        raise PermissionError  
    return audit.retrieve(cid, auditor_key)  