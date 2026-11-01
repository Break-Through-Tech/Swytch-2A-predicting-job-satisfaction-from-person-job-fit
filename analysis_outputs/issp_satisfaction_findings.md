# ISSP Job Satisfaction Imbalance Investigation

## Main finding

The apparent ~9% "satisfied" class in the baseline model is caused by a reversed interpretation of the ISSP job satisfaction scale.

The original ISSP coding is:

- 1 = Completely satisfied
- 2 = Very satisfied
- 3 = Fairly satisfied
- 4 = Neither satisfied nor dissatisfied
- 5 = Fairly dissatisfied
- 6 = Very dissatisfied
- 7 = Completely dissatisfied

The baseline model currently defines values 5-7 as "satisfied." These values actually represent dissatisfied respondents.

For the exact U.S. baseline dataset:

- Satisfied (1-3): 84.80%
- Neutral (4): 6.62%
- Dissatisfied (5-7): 8.58%

Therefore, the reported ~9% satisfied / 91% not satisfied imbalance is primarily a target-labeling issue rather than evidence that only 9% of respondents are satisfied.

## Full ISSP sample

Across respondents with valid job satisfaction responses:

- Satisfied: 81.59%
- Neutral: 11.21%
- Dissatisfied: 7.20%

For U.S. respondents in the full ISSP dataset:

- Satisfied: 85.56%
- Neutral: 6.46%
- Dissatisfied: 7.99%

## Country differences

Job satisfaction varies across countries. Among countries with at least 100 valid responses, the dissatisfied share ranges substantially.

Examples from the analysis include:

- Country 392: 17.25% dissatisfied
- Country 710: 13.06% dissatisfied
- Country 643: 12.28% dissatisfied
- Country 840 (United States): 7.99% dissatisfied

This suggests country composition can affect the overall satisfaction distribution.

## Survey year

The ISSP data combines several different survey waves:

- 1989: 5.41% dissatisfied
- 1997: 7.19% dissatisfied
- 2005: 7.73% dissatisfied
- 2015: 7.26% dissatisfied

Because the dataset combines responses collected across several decades, labor-market conditions may differ across respondents.

## Age patterns

Dissatisfaction decreases across older age groups in this sample:

- Age 14-24: 9.26% dissatisfied
- Age 25-34: 8.31%
- Age 35-44: 7.02%
- Age 45-54: 6.90%
- Age 55-64: 5.62%
- Age 65+: 3.24%

Age may therefore be an informative predictor of job satisfaction.

## Occupation patterns

Satisfaction also varies by occupation. Some O*NET occupations have much higher dissatisfied shares than the overall dataset.

Because some occupation groups have relatively small samples, these comparisons should be interpreted cautiously. The analysis only reports occupations with at least 50 respondents.

## Modeling implications

1. Correct the target coding before trying oversampling or other class-imbalance techniques.
2. The current baseline already uses stratified train/test splitting and balanced class weights, so the label definition should be fixed before adding additional imbalance methods.
3. Consider country, survey year, age, and occupation when interpreting job satisfaction patterns.
4. Be cautious about combining respondents from different countries and survey years as if they represent the same labor-market context.
5. After correcting the target, rerun the baseline models and reevaluate accuracy, F1, balanced accuracy, and AUC.
