import pandas as pd

# Load the full constructed ISSP dataset
df = pd.read_csv("data/constructed_datasets/issp.csv")

# Keep respondents with a valid satisfaction response
analysis = df[df["job_satisfaction"].between(1, 7)].copy()

# Correct ISSP interpretation:
# 1 = Completely satisfied
# 2 = Very satisfied
# 3 = Fairly satisfied
# 4 = Neither satisfied nor dissatisfied
# 5 = Fairly dissatisfied
# 6 = Very dissatisfied
# 7 = Completely dissatisfied

analysis["satisfaction_group"] = pd.cut(
    analysis["job_satisfaction"],
    bins=[0, 3, 4, 7],
    labels=["Satisfied", "Neutral", "Dissatisfied"]
)

print("=" * 70)
print("ISSP JOB SATISFACTION IMBALANCE INVESTIGATION")
print("=" * 70)

print("\n1. OVERALL DISTRIBUTION")
overall = (
    analysis["satisfaction_group"]
    .value_counts(normalize=True)
    .reindex(["Satisfied", "Neutral", "Dissatisfied"])
    .mul(100)
    .round(2)
)

print(overall)

print("\nCurrent baseline mistake:")
wrong_rate = (analysis["job_satisfaction"] >= 5).mean() * 100
print(
    f"The current baseline labels job_satisfaction >= 5 as 'satisfied': "
    f"{wrong_rate:.2f}%"
)
print("However, ISSP values 5-7 actually mean dissatisfied.")

# --------------------------------------------------
# 2. United States
# --------------------------------------------------

usa = analysis[analysis["country"] == 840].copy()

print("\n2. UNITED STATES DISTRIBUTION")

usa_distribution = (
    usa["satisfaction_group"]
    .value_counts(normalize=True)
    .reindex(["Satisfied", "Neutral", "Dissatisfied"])
    .mul(100)
    .round(2)
)

print(usa_distribution)

# --------------------------------------------------
# 3. Country comparison
# --------------------------------------------------

print("\n3. COUNTRY COMPARISON")

country_summary = (
    analysis.groupby("country")["satisfaction_group"]
    .value_counts(normalize=True)
    .mul(100)
    .rename("percent")
    .reset_index()
    .pivot(index="country", columns="satisfaction_group", values="percent")
    .reset_index()
)

country_counts = (
    analysis.groupby("country")
    .size()
    .rename("n")
    .reset_index()
)

country_summary = country_summary.merge(country_counts, on="country")

# Only compare countries with at least 100 valid satisfaction responses
country_summary = country_summary[country_summary["n"] >= 100]

country_summary = country_summary.sort_values(
    "Dissatisfied",
    ascending=False
)

print("\nCountries with highest dissatisfied share:")
print(
    country_summary[
        ["country", "n", "Satisfied", "Neutral", "Dissatisfied"]
    ]
    .head(10)
    .round(2)
    .to_string(index=False)
)

print("\nUnited States compared with all countries:")
print(
    country_summary[country_summary["country"] == 840]
    [["country", "n", "Satisfied", "Neutral", "Dissatisfied"]]
    .round(2)
    .to_string(index=False)
)

country_summary.to_csv(
    "analysis_outputs/issp_satisfaction_by_country.csv",
    index=False
)

# --------------------------------------------------
# 4. Survey year comparison
# --------------------------------------------------

print("\n4. SATISFACTION BY MODULE YEAR")

year_summary = (
    analysis.groupby("module_year")["satisfaction_group"]
    .value_counts(normalize=True)
    .mul(100)
    .rename("percent")
    .reset_index()
    .pivot(index="module_year", columns="satisfaction_group", values="percent")
    .reset_index()
)

year_counts = (
    analysis.groupby("module_year")
    .size()
    .rename("n")
    .reset_index()
)

year_summary = year_summary.merge(year_counts, on="module_year")

print(
    year_summary[
        ["module_year", "n", "Satisfied", "Neutral", "Dissatisfied"]
    ]
    .round(2)
    .to_string(index=False)
)

year_summary.to_csv(
    "analysis_outputs/issp_satisfaction_by_year.csv",
    index=False
)

# --------------------------------------------------
# 5. Age comparison
# --------------------------------------------------

print("\n5. SATISFACTION BY AGE GROUP")

analysis["age_group"] = pd.cut(
    analysis["age"],
    bins=[13, 24, 34, 44, 54, 64, 120],
    labels=["14-24", "25-34", "35-44", "45-54", "55-64", "65+"]
)

age_summary = (
    analysis.dropna(subset=["age_group"])
    .groupby("age_group", observed=True)["satisfaction_group"]
    .value_counts(normalize=True)
    .mul(100)
    .rename("percent")
    .reset_index()
    .pivot(index="age_group", columns="satisfaction_group", values="percent")
    .reset_index()
)

age_counts = (
    analysis.dropna(subset=["age_group"])
    .groupby("age_group", observed=True)
    .size()
    .rename("n")
    .reset_index()
)

age_summary = age_summary.merge(age_counts, on="age_group")

print(
    age_summary[
        ["age_group", "n", "Satisfied", "Neutral", "Dissatisfied"]
    ]
    .round(2)
    .to_string(index=False)
)

age_summary.to_csv(
    "analysis_outputs/issp_satisfaction_by_age.csv",
    index=False
)

# --------------------------------------------------
# 6. Occupation comparison
# --------------------------------------------------

print("\n6. SATISFACTION BY OCCUPATION")

occupation = analysis.dropna(subset=["ONET_SOC_CODE"]).copy()

occupation_summary = (
    occupation.groupby("ONET_SOC_CODE")["satisfaction_group"]
    .value_counts(normalize=True)
    .mul(100)
    .rename("percent")
    .reset_index()
    .pivot(index="ONET_SOC_CODE", columns="satisfaction_group", values="percent")
    .reset_index()
)

occupation_counts = (
    occupation.groupby("ONET_SOC_CODE")
    .size()
    .rename("n")
    .reset_index()
)

occupation_summary = occupation_summary.merge(
    occupation_counts,
    on="ONET_SOC_CODE"
)

# Avoid interpreting tiny occupation samples
occupation_summary = occupation_summary[
    occupation_summary["n"] >= 50
]

occupation_summary = occupation_summary.sort_values(
    "Dissatisfied",
    ascending=False
)

print("\nOccupations with highest dissatisfied share (minimum n=50):")
print(
    occupation_summary[
        ["ONET_SOC_CODE", "n", "Satisfied", "Neutral", "Dissatisfied"]
    ]
    .head(15)
    .round(2)
    .to_string(index=False)
)

occupation_summary.to_csv(
    "analysis_outputs/issp_satisfaction_by_occupation.csv",
    index=False
)

# --------------------------------------------------
# Final findings
# --------------------------------------------------

print("\n" + "=" * 70)
print("KEY FINDINGS")
print("=" * 70)

print(
    "1. The low positive class in the baseline is not the satisfied class. "
    "It represents respondents with ISSP scores 5-7, which are dissatisfied."
)

print(
    "2. The baseline target should be corrected before applying "
    "oversampling or other class-imbalance techniques."
)

print(
    "3. Satisfaction varies by country, survey year, age group, and "
    "occupation, so these should be considered when interpreting the model."
)

print(
    "4. Because ISSP combines survey waves from different years and countries, "
    "the team should be careful about treating all responses as coming from "
    "the same labor-market context."
)
