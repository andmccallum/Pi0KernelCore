class Pi0UpdateableKernel(Pi0SecureKernel):  
    def __init__(self, users, req_auth=3):  
        super().__init__(users, req_auth)  
        self.config = {}  
        self.modules = {}  
  
    def register_module(self, name, fn):  
        self.modules[name] = fn  
        self._append_audit({'action':'reg_module','name':name})  
  
    def request_config_change(self, user, key, val):  
        ok = self.approve(user)  
        self._append_audit({'action':'request_change','user':user,'param':key,'value':val})  
        if ok:  
            self.config[key] = val  
            self.reset_approvals()  
            self._append_audit({'action':'apply_change','param':key,'value':val})  
  
    def inspect(self, record):  
        results = {}  
        for n,fn in self.modules.items():  
            try:  
                results[n] = fn(record, self.config)  
            except Exception as e:  
                results[n] = None  
        self._append_audit({'action':'inspect','record':record,'results':results})  
        return results  
  
    def summary_config(self):  
        print('+----------------------+---------------------------+')  
        print('| Parameter            | Value                     |')  
        print('+----------------------+---------------------------+')  
        for k,v in self.config.items():  
            print('| {0:20s} | {1:25s} |'.format(k,str(v)))  
        print('+----------------------+---------------------------+')  
  
    def summary_modules(self):  
        print('+----------------------+---------------------------+')  
        print('| Module               | Status                    |')  
        print('+----------------------+---------------------------+')  
        for n in self.modules:  
            print('| {0:20s} | Loaded                    |'.format(n))  
        print('+----------------------+---------------------------+')  