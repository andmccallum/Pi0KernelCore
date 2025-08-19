# pi0system/security.py    
"""  
USSManager: handles D12S12 salting/slating.  
D12S12Mask: simple XOR-based mask generator.  
"""  
import hmac, hashlib, time  
  
class USSManager:  
    def __init__(self, master_key: bytes):  
        self.master_key = master_key  
  
    def salt(self, context: str) -> bytes:  
        """  
        Generate salt using HMAC(master_key, context||timestamp).  
        """  
        ts = str(time.time()).encode()  
        return hmac.new(self.master_key, context.encode() + ts, hashlib.sha256).digest()  
  
    def slate(self, salt: bytes, dim: int) -> bytes:  
        """  
        Derive slate key for dimension dim.  
        """  
        return hmac.new(salt, str(dim).encode(), hashlib.sha256).digest()  
  
class D12S12Mask:  
    def __init__(self, slate_keys: list):  
        # slate_keys: list of 12 byte-strings  
        self.slates = slate_keys  
  
    def generate_mask(self, length: int) -> bytes:  
        """  
        Build a repeating XOR mask from slate keys.  
        """  
        mask = bytearray()  
        idx = 0  
        while len(mask) < length:  
            key = self.slates[idx % len(self.slates)]  
            mask.extend(key)  
            idx += 1  
        return bytes(mask[:length])  
  
    def apply_mask(self, data: bytes, mask: bytes) -> bytes:  
        """  
        XOR data with mask.  
        """  
        return bytes(a ^ b for a, b in zip(data, mask))  