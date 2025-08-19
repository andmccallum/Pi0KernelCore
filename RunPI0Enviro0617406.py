# run_pi0_endtoend.py  
"""  
Unified end-to-end run:  
 - Compile & install pi0bridge C/C++ extension  
 - Initialize Pi0 kernels & archive/harmonizer  
 - Blind-store raw data blob  
 - Harmonize in situ  
 - Convert to numeric array & measure (mode 4)  
 - Mint & verify tokens  
 - Print a step-by-step summary table  
"""  
  
import subprocess  
import sys  
import os  
import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt  
  
# 1. Build and install the pi0bridge extension in-place  
print(">>> Building pi0bridge extension…")  
build_cmd = [  
    sys.executable, "-m", "pip", "install", "--upgrade", "--force-reinstall",  
    "."  # assumes this script lives in the pi0bridge project root with setup.py  
]  
subprocess.check_call(build_cmd)  
print("pi0bridge installed successfully\n")  
  
# 2. Import the newly installed bridge and initialization helper  
import pi0bridge as pb  
from pi0_init import init_pi0  
  
# 3. Initialize π₀ environment for domain “Compute”  
print(">>> Initializing Pi0 environment…")  
env = init_pi0("Compute")  
print()  
  
# 4. Blind‐store raw data and mint token  
raw_data = b"beam:param=A;value=123.456"  
print(">>> Minting token for raw data and blind-storing…")  
raw_blob_id = env.mint_token(raw_data)  
env.store_blob(raw_blob_id, raw_data)  
print()  
  
# 5. Harmonize the raw blob in-situ  
print(">>> Harmonizing raw blob…")  
harm_blob_id = env.harmonize_blob(raw_blob_id)  
print()  
  
# 6. Load harmonized data and convert to numeric array  
print(">>> Loading harmonized data…")  
harm_bytes = env.load_blob(harm_blob_id)  
data_array = np.frombuffer(harm_bytes, dtype=np.uint8).astype(float)  
print(f"Loaded array length: {data_array.size}\n")  
  
# 7. Perform Planck-corrected measurement (mode 4)  
print(">>> Performing measurement with mode=4…")  
meas, (smoothed, spectrum) = env.make_measurement(data_array, mode=4)  
print()  
  
# 8. Mint & blind‐store processed measurement blob  
print(">>> Minting and storing processed result…")  
proc_blob = meas.tobytes()  
proc_blob_id = env.mint_token(proc_blob)  
env.store_blob(proc_blob_id, proc_blob)  
print()  
  
# 9. Verify all tokens  
print(">>> Verifying tokens…")  
ver_raw  = env.secure_kernel.verify(raw_blob_id)  
ver_harm = env.secure_kernel.verify(harm_blob_id)  
ver_proc = env.secure_kernel.verify(proc_blob_id)  
print(f"raw_blob_id valid:   {ver_raw}")  
print(f"harm_blob_id valid:  {ver_harm}")  
print(f"proc_blob_id valid:  {ver_proc}\n")  
  
# 10. Summarize each step in a table  
summary = pd.DataFrame([  
    {"Step":"Raw mint & store",   "BlobID":raw_blob_id,  "Verified":ver_raw},  
    {"Step":"Harmonize",          "BlobID":harm_blob_id, "Verified":ver_harm},  
    {"Step":"Proc mint & store",  "BlobID":proc_blob_id, "Verified":ver_proc},  
])  
print("Summary of operations:")  
print("---------------------------------------------")  
print(f"{'Step':<20}{'Verified':<10}{'BlobID (prefix)'}")  
print("---------------------------------------------")  
for row in summary.itertuples():  
    print(f"{row.Step:<20}{str(row.Verified):<10}{row.BlobID[:12]}…")  
print("---------------------------------------------\n")  
  
# 11. Plot input vs. measurement vs. smoothed  
plt.figure(figsize=(8,4))  
plt.plot(data_array,      label="Harmonized Data", alpha=0.5)  
plt.plot(meas,            label="Measured (mode 4)", linewidth=1)  
plt.plot(smoothed,        label="Smoothed", linestyle="--")  
plt.title("Pi0 End-to-End Run Results")  
plt.xlabel("Sample Index")  
plt.ylabel("Value")  
plt.legend()  
plt.tight_layout()  
plt.show()  