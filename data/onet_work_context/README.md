# O*NET work-context extract

`freedom_to_make_decisions.csv` contains the 894 occupation rows for **Freedom to Make Decisions**, scale **CX**, from the O*NET 30.3 Work Context file. All original columns are retained, including rating dates and suppression flags. Downloaded November 13, 2026.

Source: https://www.onetcenter.org/dl_files/database/db_30_3_text/Work%20Context.txt

CX ratings range from 1 to 5. The person–job fit notebook excludes suppressed ratings and converts the remaining ratings to 0–1 using `(rating - 1) / 4`. This is an occupation-level autonomy proxy; it does not measure each respondent's job or schedule flexibility.

Source attribution: O*NET 30.3 Database, National Center for O*NET Development. Used under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This extract selects rows from the source; the notebook creates additional derived features. O*NET® is a trademark of USDOL/ETA.
