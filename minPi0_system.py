# pi0_system.py  
# Minimal Pi0System core: energy/value, market integration,  
# consciousness operators, and a simple Pi0Architect.  
  
import hashlib  
import json  
  
# — Core Operators —  
  
def EHF(E, B, V):  
    """Energy Harvesting: combine field magnitudes over volume."""  
    return 0.5 * (E + B) * V  
  
def VCF(E, κ):  
    """Convert energy into value units."""  
    return κ * (1 + E).bit_length()  # simple surrogate for log  
  
def MMO(E, R, α, β):  
    """Mint/Mine: issue Pi0Coin from energy and reserve."""  
    return α * E + β * R  
  
def SEAO(S, T, γ, T0):  
    """Staking & Energy Allocation."""  
    return S * (1 + γ * T / T0)  
  
def DEPM(E, P0, δ, E0, ε, f):  
    """Dynamic Energy Pricing."""  
    return P0 + δ * (1 + E // E0) + ε * f  
  
def ModularIntegration(E_list, R_list):  
    """Aggregate entity outputs by roles."""  
    total = 0  
    for e, r in zip(E_list, R_list):  
        total += e * r  
    return total  
  
def UCAP(C_list, S_list):  
    """Unified Consciousness Activation."""  
    prod = 1  
    for c, s in zip(C_list, S_list):  
        prod *= c * s  
    return prod  
  
# — Simple Pi0Architect —  
  
class Pi0Architect:  
    def __init__(self, registry="pi0_registry.json"):  
        self.registry = registry  
        try:  
            with open(registry) as f:  
                self.data = json.load(f)  
        except:  
            self.data = {}  
  
    def wrap(self, modules, config, version):  
        """Serialize modules+config into a package."""  
        pkg = {"version": version, "modules": modules, "config": config}  
        return json.dumps(pkg, sort_keys=True)  
  
    def sign(self, package):  
        """Attach SHA-256 signature."""  
        sig = hashlib.sha256(package.encode()).hexdigest()  
        return sig  
  
    def publish(self, package, sig, version):  
        """Register immutable kernel iteration."""  
        self.data[version] = {"package": package, "signature": sig}  
        with open(self.registry, "w") as f:  
            json.dump(self.data, f, indent=2)  
        return version, sig  