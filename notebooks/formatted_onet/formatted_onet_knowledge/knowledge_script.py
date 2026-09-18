import pandas as pd

df = pd.read_csv("../../../data/onet_abilities/knowledge.csv")

df["clean_name"] = (
    df["Element Name"]
    .str.lower()
    .str.replace(" ", "_")
)

wide = df.pivot_table(
    index=["O*NET-SOC Code", "Title"],
    columns=["clean_name", "Scale ID"],
    values="Data Value"
)

wide.columns = [
    f"knowledge_{name}_{'importance' if scale == 'IM' else 'level'}"
    for name, scale in wide.columns
]

def rank_elements(group):
    sorted_group = group.sort_values("Data Value", ascending=False)
    return "|".join(sorted_group["clean_name"])

im_only = df[df["Scale ID"] == "IM"]
ranked_im = im_only.groupby(["O*NET-SOC Code", "Title"]).apply(rank_elements)
ranked_im.name = "knowledge_importance_ranked"

im_only = df[df["Scale ID"] == "LV"]
ranked_lvl = im_only.groupby(["O*NET-SOC Code", "Title"]).apply(rank_elements)
ranked_lvl.name = "knowledge_level_ranked"

final = ranked_im.to_frame().join(ranked_lvl).join(wide)
final = final.reset_index()
final.to_csv("formatted_knowledge.csv", index=False)
