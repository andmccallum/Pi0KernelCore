import hashlib  
import hmac  
  
class USSKernel:  
    def __init__(self, name='USSKernel', secret_key='defaultsecret'):  
        self.name = name  
        self.protocol = 'USS-Quantum'  
        self.audit_log = []  
        self.memory = []  
        self._counter = 0  
        # Secret key for HMAC and XOR cipher (bytes)  
        self.secret_key = secret_key.encode('utf-8')  
  
    def _xor_cipher(self, data_bytes):  
        """  
        Simple XOR encryption/decryption with repeating secret_key.  
        """  
        key = self.secret_key  
        return bytes(b ^ key[i % len(key)] for i, b in enumerate(data_bytes))  
  
    def _sign(self, data_bytes):  
        """  
        HMAC-SHA256 signature of data_bytes.  
        """  
        return hmac.new(self.secret_key, data_bytes, hashlib.sha256).hexdigest()  
  
    def communicate(self, target, message):  
        # 1) timestamp  
        self._counter += 1  
        timestamp = self._counter  
  
        # 2) prepare plaintext record  
        record_plain = f"{target}|{message}|{timestamp}"  
        record_bytes = record_plain.encode('utf-8')  
  
        # 3) encrypt  
        encrypted = self._xor_cipher(record_bytes)  
  
        # 4) sign encrypted payload  
        signature = self._sign(encrypted)  
  
        # 5) protocol hash (unchanged)  
        protocol_hash = sum(ord(c) for c in record_plain) % 100000  
  
        packet = {  
            'target': target,  
            'encrypted': encrypted,         # bytes  
            'protocol_hash': protocol_hash, # int  
            'timestamp': timestamp,         # int  
            'signature': signature          # hex string  
        }  
        self.audit_log.append(packet)  
        self.memory.append(packet)  
        return packet  
  
    def verify(self, packet):  
        """  
        Verify integrity of a received packet.  
        Returns decrypted plaintext on success, else raises ValueError.  
        """  
        encrypted = packet['encrypted']  
        signature = packet['signature']  
        # Recompute HMAC  
        expected = self._sign(encrypted)  
        if not hmac.compare_digest(expected, signature):  
            raise ValueError("Signature mismatch: data corrupted or tampered")  
        # Decrypt  
        decrypted = self._xor_cipher(encrypted)  
        return decrypted.decode('utf-8')  
  
    def iterate(self):  
        # Version bump based on audit count  
        self.protocol = self.protocol + '-v' + str(len(self.audit_log) + 1)  
        return {  
            'kernel': self.name,  
            'protocol': self.protocol,  
            'audit_count': len(self.audit_log)  
        }  
  
    def export(self):  
        return {  
            'type': self.name,  
            'protocol': self.protocol,  
            'audit_log': list(self.audit_log),  
            'memory': list(self.memory)  
        }  
  
# ASCII Table: USSKernel Security Steps  
security_table = """  
┌─────────┬───────────────────────────────────────────────┐  
│ Step    │ Operation                                     │  
├─────────┼───────────────────────────────────────────────┤  
│ 1       │ Timestamping (counter++)                      │  
│ 2       │ Plaintext assembly: "target|message|timestamp"│  
│ 3       │ XOR encryption with secret_key                │  
│ 4       │ HMAC-SHA256 signature over encrypted payload  │  
│ 5       │ Compute protocol_hash for audit tracking      │  
└─────────┴───────────────────────────────────────────────┘  
"""  
print(security_table)  