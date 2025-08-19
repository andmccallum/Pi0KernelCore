#!/usr/bin/env python3
"" Pi0 Stand-Alone Kernel – single-file edition
Just drop `pi0_single_kernel.py` into any directory and run:
    python pi0_single_kernel.py 0.3 0.3 0.4
It will compute entropy, meter gas, and emit a settlement receipt.

import time, math, hashlib, json, sys

def settle(receipt):
    print("Pi0Market-SETTLE →", json.dumps(receipt, indent=2))

# decorator
REGISTRY = {}

def pi0op(func):
    REGISTRY[func.__name__] = func
    def wrapper(*args):
        t0 = time.perf_counter()
        out = func(*args)
        dt = time.perf_counter() - t0
        joules = 1.2e-10 * (len(out) if hasattr(out, '__len__') else 1)
        gas = joules * 1e6
        receipt = dict(kernel=func.__name__, gas=gas, elapsed_s=dt,
                       hash=hashlib.sha256((func.__name__+str(out)).encode()).hexdigest()[:16])
        settle(receipt)
        return out
    return wrapper

@pi0op
def entropy_core(p_list):
    return [ -p*math.log(p,2) if p>0 else 0 for p in p_list ]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python pi0_single_kernel.py 0.1 0.2 0.7'); sys.exit(1)
    probs = [float(x) for x in sys.argv[1:]]
    res = entropy_core(probs)
    print('
Result Table')
    print('p	entropy(p)')
    for p,e in zip(probs,res):
        print(f'{p:.4f}	{e:.6f}')
