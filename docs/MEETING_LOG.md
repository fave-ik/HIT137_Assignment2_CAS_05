# MEETING LOG

## 2025-08-29
Attendees: <names>
Decisions:
- Roles assigned (Member 1–4)
- Branch workflow agreed
Action items:
- M1: Q1 encryption/decryption
- M2: Q2 seasonal averages
- M3: Q2 range + stability
- M4: Q3 recursion

01/09/2025 — Suman (Suman39)

**Q2 – Weather Analysis**
- Implemented `Q2_weather/main_q2.py` to process **all** CSVs in `Q2_weather/temperatures/`.
- Wrote outputs to `Q2_weather/outputs/`:
  - `average_temp.txt` — seasonal averages across all years & stations
  - `largest_temp_range_station.txt` — station(s) with largest range + min/max
  - `temperature_stability_stations.txt` — most stable & most variable (StdDev)
- Ignored NaN values as required; used Australian seasons (Dec–Feb, Mar–May, Jun–Aug, Sep–Nov).
- Verified results locally; opened PR and helped resolve text-file conflicts from Q1 outputs by keeping `main` versions.
