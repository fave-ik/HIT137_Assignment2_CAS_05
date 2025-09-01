from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent
TEMPS_DIR = ROOT / "temperatures"
OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]
SEASON_OF = {
    "December": "Summer", "January": "Summer", "February": "Summer",
    "March": "Autumn", "April": "Autumn", "May": "Autumn",
    "June": "Winter", "July": "Winter", "August": "Winter",
    "September": "Spring", "October": "Spring", "November": "Spring",
}

csvs = sorted(TEMPS_DIR.glob("*.csv"))
if not csvs:
    print(f"No CSV files found in {TEMPS_DIR}")
    raise SystemExit(1)

season_values = {s: [] for s in ["Summer","Autumn","Winter","Spring"]}
by_station_values = {}

for path in csvs:
    df = pd.read_csv(path)
    month_cols = [c for c in MONTHS if c in df.columns]
    df[month_cols] = df[month_cols].apply(pd.to_numeric, errors="coerce")

    for m in month_cols:
        season = SEASON_OF[m]
        vals = df[m].to_numpy(dtype="float64", copy=False)
        season_values[season].extend(vals[~np.isnan(vals)].tolist())

    names = df["STATION_NAME"].astype(str).tolist()
    arr = df[month_cols].to_numpy(dtype="float64")
    for i, name in enumerate(names):
        vals = arr[i, :]
        by_station_values.setdefault(name, [])
        by_station_values[name].extend(vals[~np.isnan(vals)].tolist())

avg_lines = []
for season in ["Summer","Autumn","Winter","Spring"]:
    vals = np.array(season_values[season], dtype="float64")
    mean = np.nanmean(vals) if vals.size else float("nan")
    avg_lines.append(f"{season}: {mean:.1f}°C")
(OUT_DIR / "average_temp.txt").write_text("\n".join(avg_lines), encoding="utf-8")

stats = []
for name, vals in by_station_values.items():
    a = np.array(vals, dtype="float64")
    if a.size == 0:
        continue
    maxv = float(np.nanmax(a))
    minv = float(np.nanmin(a))
    rang = maxv - minv
    std  = float(np.nanstd(a, ddof=0))
    stats.append((name, rang, maxv, minv, std))

if not stats:
    raise SystemExit("No station data read")

max_range = max(s[1] for s in stats)
largest = [s for s in stats if abs(s[1]-max_range) < 1e-9]
range_lines = [f"{name}: Range {rang:.1f}°C (Max: {maxv:.1f}°C, Min: {minv:.1f}°C)" for name,rang,maxv,minv,std in largest]
(OUT_DIR / "largest_temp_range_station.txt").write_text("\n".join(range_lines), encoding="utf-8")

stds = [s[4] for s in stats]
min_std, max_std = min(stds), max(stds)
most_stable   = [s for s in stats if abs(s[4]-min_std) < 1e-9]
most_variable = [s for s in stats if abs(s[4]-max_std) < 1e-9]
stable_lines   = [f"Most Stable: {name}: StdDev {std:.1f}°C"   for name,r,g,h,std in most_stable]
variable_lines = [f"Most Variable: {name}: StdDev {std:.1f}°C" for name,r,g,h,std in most_variable]
(OUT_DIR / "temperature_stability_stations.txt").write_text("\n".join(stable_lines + variable_lines), encoding="utf-8")

print("Wrote:")
for fn in ["average_temp.txt","largest_temp_range_station.txt","temperature_stability_stations.txt"]:
    print(" -", fn)
