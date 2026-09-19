import pandas as pd

# Load data
df = pd.read_csv("../../data/onet_abilities/knowledge.csv")

# Normalize element names to lowercase/underscore for safe column/string tokens
df["clean_name"] = (
    df["Element Name"]
    .str.lower()
    .str.replace(" ", "_")
)

# Pivot to one row per occupation, one column per element+scale combo
wide = df.pivot_table(
    index=["O*NET-SOC Code", "Title"],
    columns=["clean_name", "Scale ID"],
    values="Data Value"
)

# Flatten the MultiIndex columns into knowledge_<element>_<importance OR level> names
wide.columns = [
    f"knowledge_{name}_{'importance' if scale == 'IM' else 'level'}"
    for name, scale in wide.columns
]

# Sort a group's elements by value (descending) and join their names with |
def rank_elements(group):
    sorted_group = group.sort_values("Data Value", ascending=False)
    return "|".join(sorted_group["clean_name"])

# Build the pipe-delimited ranked summary column for Importance
im_only = df[df["Scale ID"] == "IM"]
ranked_im = im_only.groupby(["O*NET-SOC Code", "Title"]).apply(rank_elements)
ranked_im.name = "knowledge_importance_ranked"

# Build the pipe-delimited ranked summary column for Level
im_only = df[df["Scale ID"] == "LV"]
ranked_lvl = im_only.groupby(["O*NET-SOC Code", "Title"]).apply(rank_elements)
ranked_lvl.name = "knowledge_level_ranked"

# Combine ranked columns first, then all individual value columns
final = ranked_im.to_frame().join(ranked_lvl).join(wide)
final = final.reset_index()
final = final.rename(columns={"O*NET-SOC Code": "ONET_SOC_CODE", "Title": "title"}) # rename for consistency
final.to_csv("formatted_knowledge.csv", index=False)
