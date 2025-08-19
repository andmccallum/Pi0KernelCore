import threading, time, json, hashlib  
  
class Pi0SecureKernel:  
    def __init__(self, users, req_auth=3, audit_file='secure_audit.log'):  
        # Multi-party gating  
        self._lock = threading.Lock()  
        self._required = req_auth  
        self._approvals = set()  
        # Audit chain  
        self._chain = []  
        self._prev_hash = '0'*64  
        self._audit_file = audit_file  
        self._users = set(users)  
  
    def _append_audit(self, entry):  
        ts = time.time()  
        rec = {'entry':entry, 'prev':self._prev_hash, 'ts':ts}  
        data = json.dumps(rec, sort_keys=True).encode()  
        h = hashlib.sha256(data).hexdigest()  
        rec['hash'] = h  
        self._chain.append(rec)  
        self._prev_hash = h  
        with open(self._audit_file,'a') as f:  
            f.write(json.dumps(rec)+'\n')  
  
    def approve(self, user):  
        if user not in self._users:  
            raise PermissionError('Unknown user')  
        with self._lock:  
            self._approvals.add(user)  
            ok = len(self._approvals)>=self._required  
        self._append_audit({'action':'approve','user':user,'granted':ok})  
        return ok  
  
    def reset_approvals(self):  
        with self._lock:  
            self._approvals.clear()  
        self._append_audit({'action':'reset_approvals'})  
  
    def summary_audit(self):  
        print('+-------+----------------------+--------------------------------+')  
        print('|  #    | Timestamp            | Entry                          |')  
        print('+-------+----------------------+--------------------------------+')  
        for i,rec in enumerate(self._chain,1):  
            ts = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(rec['ts']))  
            e = rec['entry']  
            print('| {0:5d} | {1:20s} | {2:30s} |'.format(i,ts,str(e)[:30]))  
        print('+-------+----------------------+--------------------------------+')  