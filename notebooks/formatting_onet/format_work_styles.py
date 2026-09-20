import pandas as pd
import re
from pathlib import Path

# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

input_path = (
    PROJECT_ROOT
    / "data"
    / "onet_work_styles"
    / "work_styles.csv"
)

output_path = (
    PROJECT_ROOT
    / "notebooks"
    / "formatting_onet"
    / "formatted_work_styles.csv"
)

# Change this only if the team agrees on a different number.
TOP_N = 10


# ---------------------------------------------------------
# Load the Work Styles data
# ---------------------------------------------------------

df = pd.read_csv(input_path)

print("Original shape:", df.shape)


# ---------------------------------------------------------
# Rename required identifier columns
# ---------------------------------------------------------

df = df.rename(
    columns={
        "O*NET-SOC Code": "ONET_SOC_CODE",
        "Title": "title",
    }
)


# ---------------------------------------------------------
# Clean work style names for use as column names
# ---------------------------------------------------------

def clean_name(name):
    return re.sub(
        r"[^a-z0-9]+",
        "_",
        str(name).lower()
    ).strip("_")


df["field_name"] = df["Element Name"].apply(clean_name)


# ---------------------------------------------------------
# Create readable names for the two scales
# ---------------------------------------------------------

scale_names = {
    "DR": "distinctiveness_rank",
    "WI": "impact",
}

df["scale_clean"] = df["Scale ID"].map(scale_names)


# ---------------------------------------------------------
# Make sure each occupation/style/scale combination is unique
# ---------------------------------------------------------

duplicate_count = df.duplicated(
    subset=[
        "ONET_SOC_CODE",
        "Element Name",
        "Scale ID",
    ]
).sum()

print("Duplicate occupation/style/scale rows:", duplicate_count)

if duplicate_count != 0:
    raise ValueError(
        "Duplicate occupation/style/scale combinations found."
    )


# ---------------------------------------------------------
# Create the value column names
#
# Example:
# work_styles_impact_innovation_value
# work_styles_distinctiveness_rank_innovation_value
# ---------------------------------------------------------

df["value_column"] = (
    "work_styles_"
    + df["scale_clean"]
    + "_"
    + df["field_name"]
    + "_value"
)


# ---------------------------------------------------------
# Pivot from long format to wide format
# ---------------------------------------------------------

wide_values = (
    df.pivot(
        index=["ONET_SOC_CODE", "title"],
        columns="value_column",
        values="Data Value",
    )
    .reset_index()
)

wide_values.columns.name = None


# ---------------------------------------------------------
# Ranked Work Styles using Work Styles Impact
#
# Higher WI value = higher impact
# ---------------------------------------------------------

impact_ranked = (
    df[df["Scale ID"] == "WI"]
    .sort_values(
        ["ONET_SOC_CODE", "Data Value"],
        ascending=[True, False],
        kind="stable",
    )
    .groupby(
        ["ONET_SOC_CODE", "title"]
    )["field_name"]
    .apply(
        lambda x: "|".join(x.head(TOP_N))
    )
    .reset_index(
        name="work_styles_impact_ranked"
    )
)


# ---------------------------------------------------------
# Ranked Work Styles using Distinctiveness Rank
#
# DR = 1 is the highest rank.
# DR = 0 means the style is not given a positive
# distinctiveness ranking.
# ---------------------------------------------------------

distinctiveness = df[
    (df["Scale ID"] == "DR")
    & (df["Data Value"] > 0)
].copy()

distinctiveness_ranked = (
    distinctiveness
    .sort_values(
        ["ONET_SOC_CODE", "Data Value"],
        ascending=[True, True],
        kind="stable",
    )
    .groupby(
        ["ONET_SOC_CODE", "title"]
    )["field_name"]
    .apply(
        lambda x: "|".join(x.head(TOP_N))
    )
    .reset_index(
        name="work_styles_distinctiveness_ranked"
    )
)


# ---------------------------------------------------------
# Combine values and ranked summaries
# ---------------------------------------------------------

formatted = (
    wide_values
    .merge(
        impact_ranked,
        on=["ONET_SOC_CODE", "title"],
        how="left",
    )
    .merge(
        distinctiveness_ranked,
        on=["ONET_SOC_CODE", "title"],
        how="left",
    )
)


# ---------------------------------------------------------
# Put identifier and ranked columns first
# ---------------------------------------------------------

first_columns = [
    "ONET_SOC_CODE",
    "title",
    "work_styles_impact_ranked",
    "work_styles_distinctiveness_ranked",
]

remaining_columns = sorted(
    [
        col
        for col in formatted.columns
        if col not in first_columns
    ]
)

formatted = formatted[
    first_columns + remaining_columns
]


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

print("Formatted shape:", formatted.shape)
print(
    "Unique occupations:",
    formatted["ONET_SOC_CODE"].nunique()
)

if len(formatted) != df["ONET_SOC_CODE"].nunique():
    raise ValueError(
        "Output does not have exactly one row per occupation."
    )


# ---------------------------------------------------------
# Save final formatted CSV
# ---------------------------------------------------------

formatted.to_csv(
    output_path,
    index=False,
)

print("\nSaved:")
print(output_path)

print("\nFirst five rows:")
print(formatted.head())