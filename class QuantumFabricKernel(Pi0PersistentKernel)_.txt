class QuantumFabricKernel(Pi0PersistentKernel):  
    def __init__(self, modules, cloud_endpoint, p):  
        super().__init__()  
        self.modules = modules  
        self.entangle_client = EntangleClient(cloud_endpoint)  
        self.zk_circuit = define_g4_circuit(p)  
        self.hypercube = {}  
  
    def tick(self):  
        # 1. evolve system DNA & generation  
        self.python_instigator('evolve_system')  
        # 2. tear down classical scaffold  
        self.python_instigator('uss_communicate', 'teardown')  
        # 3. bootstrap quantum entanglement  
        key = self.entangle_client.bootstrap()  
        # 4. run each module’s classical+quantum step  
        state = {  
            'A': self.state_matrix, 'W1': self.W1, 'W2': self.W2,  
            'eps': self.eps, 'raw_input': self.get_input()  
        }  
        for mod in self.modules:  
            mod.step(state, self)  
        # 5. exchange hypercube via quantum cloud  
        payload = {  
            'hypercube': self.hypercube,  
            'generation': self.persistent_state['generation']  
        }  
        response = self.entangle_client.exchange(payload, key)  
        self.hypercube = response['hypercube']  
        # 6. run zero‐knowledge G4 audit  
        proof = run_zk_snark(self.zk_circuit,  
                             public_input=response['hypercube']['G4_oracle'])  
        self.hypercube['G4_proof_valid'] = proof.is_valid()  
        return self.hypercube  