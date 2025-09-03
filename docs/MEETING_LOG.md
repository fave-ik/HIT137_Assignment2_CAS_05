# MEETING LOG

## 2025-08-29

Roles assigned:
30/08/2025 — Esangbedo Favour (fave-ik)
Q1 – File Encryption/Decryption

• Implemented Q1_encryption/main_q1.py.
• Reads Q1_encryption/raw_text.txt and writes to Q1_encryption/outputs/:
  - encrypted_text.txt — encrypted content
  - decrypted_text.txt — decrypted content
• Added verification step that compares decrypted_text.txt to raw_text.txt and prints
  “Verification: Successful/Failed”.
• Followed the required rules:
  - lowercase a–m: shift forward by (shift1 * shift2)
  - lowercase n–z: shift backward by (shift1 + shift2)
  - uppercase A–M: shift backward by shift1
  - uppercase N–Z: shift forward by (shift2²)
  - non-letters unchanged
• Implemented a mapping-based inverse so decryption exactly reverses encryption.
• Tested locally with  shift pairs (0,0) and confirmed the decrypted text
  matches the original; outputs committed to the repo.

01/09/2025 — Suman (Suman39)

**Q2 – Weather Analysis**
- Implemented `Q2_weather/main_q2.py` to process **all** CSVs in `Q2_weather/temperatures/`.
- Wrote outputs to `Q2_weather/outputs/`:
  - `average_temp.txt` — seasonal averages across all years & stations
  - `largest_temp_range_station.txt` — station(s) with largest range + min/max
  - `temperature_stability_stations.txt` — most stable & most variable (StdDev)
- Ignored NaN values as required; used Australian seasons (Dec–Feb, Mar–May, Jun–Aug, Sep–Nov).
- Verified results locally; opened PR and helped resolve text-file conflicts from Q1 outputs by keeping `main` versions.

03/09/2025 — Mercy Kabang (Maeexox)
Q3 – Turtle Recursion

• Implemented Q3_turtle/main_q3.py using a recursive fractal_edge + polygon driver.
• Parameters: sides, length, depth; draws the pattern with turtle.
• Tested locally; structured into small functions for clarity. 
