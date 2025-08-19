# pi0system/core.py    
"""  
Core kernel loop and operator registry for PI0System.  
"""  
  
class PI0Kernel:  
    def __init__(self):  
        # registry maps name to function  
        self.registry = {}  
  
    def register_operator(self, name, func):  
        """  
        Register a core operator by name.  
        name: str, func: callable(state: bytes, **kwargs)->bytes  
        """  
        self.registry[name] = func  
  
    def apply_operator(self, name, state, **kwargs):  
        """  
        Apply a registered operator to state.  
        """  
        if name not in self.registry:  
            raise KeyError("Operator not found:" + name)  
        return self.registry[name](state, **kwargs)  
  
    def step(self, state, operators):  
        """  
        Single kernel iteration: apply sequence of operators.  
        operators: list of (name, kwargs) tuples.  
        """  
        new_state = state  
        for name, params in operators:  
            new_state = self.apply_operator(name, new_state, **params)  
        return new_state  