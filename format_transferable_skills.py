import os
import re
import pandas as pd


def clean_name(name):
    """Clean string to lowercase with underscores."""
    name = re.sub(r"[^\w\s]", "", str(name))
    return name.strip().lower().replace(" ", "_")


# 1. Read input dataset from repository path
input_path = "data/onet_skills/transferable_skills.csv"
df = pd.read_csv(input_path)

# 2. Clean element names and scale labels
df["clean_element"] = df["Element Name"].apply(clean_name)
df["clean_scale"] = df["Scale ID"].apply(
    lambda x: "importance"
    if str(x).upper() == "IM"
    else ("level" if str(x).upper() == "LV" else clean_name(x))
)

# 3. Pivot long format into wide format
pivot_df = df.pivot_table(
    index=["O*NET-SOC Code", "Title"],
    columns=["clean_scale", "clean_element"],
    values="Data Value",
    aggfunc="first",
).reset_index()

# 4. Standardize output column prefixes
new_columns = ["O*NET-SOC Code", "Title"]
for col in pivot_df.columns[2:]:
    scale, element = col
    new_columns.append(f"transferable_skills_{scale}_{element}_value")

pivot_df.columns = new_columns

# 5. Build pipe-delimited ranked summary of top 5 skills
importance_df = df[df["clean_scale"] == "importance"].sort_values(
    by=["O*NET-SOC Code", "Data Value"], ascending=[True, False]
)

ranked_df = (
    importance_df.groupby("O*NET-SOC Code")["clean_element"]
    .apply(lambda x: "|".join(x.head(5)))
    .reset_index(name="transferable_skills_ranked")
)

# 6. Merge ranked summary back into wide dataset
final_df = pd.merge(pivot_df, ranked_df, on="O*NET-SOC Code", how="left")

# 7. Ensure target folder exists and export CSV
output_dir = "data/formatted_onet"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "formatted_transferable_skills.csv")

final_df.to_csv(output_path, index=False)

print(f"Success! Output saved to: {output_path}")
print(f"Rows: {len(final_df)} | Columns: {len(final_df.columns)}")