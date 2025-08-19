from pi0system.core import PI0Kernel  
kernel = PI0Kernel()  
  
# Example operator: identity  
def identity_op(state: bytes, **kwargs) -> bytes:  
    return state  
  
kernel.register_operator('Identity', identity_op)  