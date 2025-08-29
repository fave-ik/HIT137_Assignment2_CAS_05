"""
Q2 – Temperature analysis across ALL CSV files in ./temperatures

Generates:
- outputs/average_temp.txt
- outputs/largest_temp_range_station.txt
- outputs/temperature_stability_stations.txt
"""

from pathlib import Path
import pandas as pd

TEMPS_DIR = Path(__file__).parent / "temperatures"
OUT_DIR = Path(__file__).parent / "outputs"

MONTHS = ["January","February","March","April","May","June",
          "July","August","September","October","November","December"]

MONTH_TO_SEASON = {
    "December": "Summer", "January": "Summer", "February": "Summer",
    "March": "Autumn", "April": "Autumn", "May": "Autumn",
    "June": "Winter", "July": "Winter", "August": "Winter",
    "September": "Spring", "October": "Spring", "November": "Spring",
}

def load_all_csvs() -> pd.DataFrame:
    frames = []
    for csv_path in sorted(TEMPS_DIR.glob("*.csv")):
        df = pd.read_csv(csv_path)
        # Add year if present in file name
        try:
            year = int(csv_path.stem.split("_")[-1])
        except Exception:
            year = None
        df["YEAR"] = year
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)

def compute_seasonal_average(long_df: pd.DataFrame, out_path: Path):
    season_avg = (long_df.groupby("SEASON")["TEMP_C"]
                  .mean()
                  .reindex(["Summer","Autumn","Winter","Spring"]))
    lines = [f"{season}: {val:.1f}°C" for season, val in season_avg.items() if pd.notna(val)]
    out_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

def compute_largest_range(long_df: pd.DataFrame, out_path: Path):
    station_cols = ["STATION_NAME","STN_ID"]
    stats = long_df.groupby(station_cols)["TEMP_C"].agg(["min","max"]).rename(columns={"min":"MIN_C","max":"MAX_C"})
    stats["RANGE_C"] = stats["MAX_C"] - stats["MIN_C"]
    max_range = stats["RANGE_C"].max()
    winners = stats[stats["RANGE_C"] == max_range].reset_index()
    lines = [
        f"Station {row['STATION_NAME']} (ID {int(row['STN_ID'])}): Range {row['RANGE_C']:.1f}°C (Max: {row['MAX_C']:.1f}°C, Min: {row['MIN_C']:.1f}°C)"
        for _, row in winners.iterrows()
    ]
    out_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

def compute_stability(long_df: pd.DataFrame, out_path: Path):
    station_cols = ["STATION_NAME","STN_ID"]
    stds = long_df.groupby(station_cols)["TEMP_C"].std(ddof=0).to_frame("STDDEV_C")
    min_std = stds["STDDEV_C"].min()
    max_std = stds["STDDEV_C"].max()
    most_stable = stds[stds["STDDEV_C"] == min_std].reset_index()
    most_variable = stds[stds["STDDEV_C"] == max_std].reset_index()

    lines = []
    for _, row in most_stable.iterrows():
        lines.append(f"Most Stable: Station {row['STATION_NAME']} (ID {int(row['STN_ID'])}): StdDev {row['STDDEV_C']:.1f}°C")
    for _, row in most_variable.iterrows():
        lines.append(f"Most Variable: Station {row['STATION_NAME']} (ID {int(row['STN_ID'])}): StdDev {row['STDDEV_C']:.1f}°C")
    out_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_all_csvs()
    if df.empty:
        print(f"No CSV files found in {TEMPS_DIR}. Put all stations_group_*.csv there.")
        return

    id_cols = [c for c in df.columns if c not in MONTHS]
    long_df = df.melt(id_vars=id_cols, value_vars=MONTHS, var_name="MONTH", value_name="TEMP_C").dropna(subset=["TEMP_C"])
    long_df["SEASON"] = long_df["MONTH"].map(MONTH_TO_SEASON)

    compute_seasonal_average(long_df, OUT_DIR / "average_temp.txt")
    compute_largest_range(long_df, OUT_DIR / "largest_temp_range_station.txt")
    compute_stability(long_df, OUT_DIR / "temperature_stability_stations.txt")

    print("Generated outputs in", OUT_DIR)

if __name__ == "__main__":
    main()
