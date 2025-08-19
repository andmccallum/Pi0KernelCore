# pi0_init.py  
"""  
Initialize the full Pi0 environment:  
 - C kernel for low-level domain setup  
 - C++ SecureKernel for five-party token management  
 - Pi0Archive and Harmonizer for blind storage  
 - QuantNumPyTon MeasurementOperator factory  
"""  
  
import pi0bridge as pb  
from measurement import MeasurementOperator  
  
class Pi0Environment:  
    def __init__(self, domain="Compute"):  
        # 1. Initialize C kernel (must precede any C operations)  
        init_code = pb.init_c(domain)  
        print("C kernel initialized for domain:", domain)  
  
        # 2. Initialize C++ SecureKernel (five-party token engine)  
        self.secure_kernel = pb.SecureKernel(domain)  
        print("SecureKernel instantiated for domain:", domain)  
  
        # 3. Attach Archive/Harmonizer via bridge  
        # These are static in the bridge; no instantiation needed  
        print("Pi0Archive and Harmonizer ready (blind)")  
  
    def mint_token(self, data_bytes):  
        """  
        Mint a five-party token for raw or processed data.  
        Returns: blob_id (string)  
        """  
        blob_id = self.secure_kernel.mint(data_bytes)  
        print("Minted token, blob_id:", blob_id)  
        return blob_id  
  
    def store_blob(self, blob_id, data_bytes):  
        """  
        Blind-store encrypted blob  
        """  
        pb.store(blob_id, data_bytes)  
        print("Blind-stored data under blob_id:", blob_id)  
  
    def harmonize_blob(self, blob_id):  
        """  
        Perform in-situ blind harmonization, returns new blob_id  
        """  
        new_id = self.secure_kernel.harmonize(blob_id)  
        print("Harmonized blob; new blob_id:", new_id)  
        return new_id  
  
    def load_blob(self, blob_id):  
        """  
        Decrypt and load harmonized or raw data  
        """  
        data = pb.load(blob_id)  
        print("Loaded data bytes for blob_id:", blob_id)  
        return data  
  
    def make_measurement(self, data_array, mode=4, alpha=0.7, beta=0.3, ℓP2=1e-68):  
        """  
        Factory for a Planck-corrected MeasurementOperator  
        """  
        M = MeasurementOperator(mode=mode, alpha=alpha, beta=beta, ℓP2=ℓP2)  
        result = M.apply(data_array)  
        print(f"Computed measurement in mode {mode}")  
        return result, M.postprocess(result)  
  
# Expose a singleton for easy import  
_pi0_env = None  
  
def init_pi0(domain="Compute"):  
    """  
    Initialize (once) and return the Pi0Environment singleton.  
    """  
    global _pi0_env  
    if _pi0_env is None:  
        _pi0_env = Pi0Environment(domain)  
    return _pi0_env  