import pandas as pd
from pybaseball import batting_stats, cache

cache.enable()
START_YEAR = 1871
END_YEAR = 2024
CHUNK_SIZE = 10  
MIN_HR_FILTER = 50  
OUTPUT_FILE = "career_hr.csv"

frames = []
for start in range(START_YEAR, END_YEAR + 1, CHUNK_SIZE):
    end = min(start + CHUNK_SIZE - 1, END_YEAR)
    print(f"📦 Loading batting stats {start}-{end} ...")
    try:
        df_chunk = batting_stats(start, end)
        frames.append(df_chunk)
    except Exception as e:
        print(f"⚠️ Skipped {start}-{end} due to error: {e}")

if not frames:
    raise RuntimeError("No data could be loaded. Try reducing the date range or check your connection.")

data = pd.concat(frames, ignore_index=True)
print(f"✅ Loaded {len(data)} total player-seasons.")

df = data[['Season', 'Name', 'HR']].dropna(subset=['HR']).copy()
df['Season'] = df['Season'].astype(int)
df['HR'] = df['HR'].astype(int)
df = df.sort_values(['Name', 'Season'])

df['career_hr'] = df.groupby('Name')['HR'].cumsum()

# filter
if MIN_HR_FILTER > 0:
    df = df[df['career_hr'] >= MIN_HR_FILTER]

df = df.rename(columns={'Season': 'year', 'Name': 'player'})
output_df = df[['year', 'player', 'career_hr']].sort_values(['year', 'career_hr'], ascending=[True, False])

output_df.to_csv(OUTPUT_FILE, index=False)
print(f"💾 Saved file: {OUTPUT_FILE}")

print("\nSample of data:")
print(output_df.head(10))
print(f"\nTotal players: {output_df['player'].nunique()}")
print(f"Year range: {output_df['year'].min()}–{output_df['year'].max()}")
print("Done!")
