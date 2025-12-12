# 2025 JEB power analysis (Cohen's f)
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# STATS
from statsmodels.stats.power import TTestIndPower, FTestPower, TTestPower, FTestPowerF2
from statsmodels.stats.multitest import multipletests
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.graphics.regressionplots import plot_regress_exog, plot_partregress
from statsmodels.stats.power import FTestPower

# --------------------
# Data
# --------------------
from load_data import load_data
file_path = 'data/2025_data.xlsx'
new_df = load_data(file_path)

# --------------------
# Regplot capped brood vs diet type
# --------------------
plt.figure(figsize=(10, 6))
sns.regplot(
    x=new_df['Protein'],
    y=new_df['Capped_Brood'],
    scatter=True,
    scatter_kws={'s': 50},
    line_kws={'color': 'orange', 'label': 'OLS Regression'}
)
plt.title('Relationship between Protein and Capped Brood')
plt.xlabel('Protein Levels')
plt.ylabel('Capped Brood')
plt.legend(loc='upper left')
plt.xticks([6, 12, 18, 25, 30], ['6', '12', '18', '25', '30'])
plt.ylim(0, 400)
plt.grid(True)
plt.show()

# --------------------
# OLS regression using sm.OLS
# --------------------
X_prot = new_df[['Protein']]
y_dcon = new_df['Diet_Consumption']
y_capp = new_df['Capped_Brood']
X_prot_const = sm.add_constant(X_prot)

model = sm.OLS(y_capp, X_prot_const).fit()
print(model.summary())

# --------------------
# Cohen's f (effect size) from R²
# df_denom = n - k - 1 (n = sample size, k = number of predictors)
# --------------------
sample_size = len(new_df)
effect_size = np.sqrt(model.rsquared / (1 - model.rsquared))  # Cohen's f
df_num = 1  # one predictor: Protein
df_denom = sample_size - df_num - 1

adjusted_r2 = model.rsquared_adj
adjusted_cohens_f = np.sqrt(adjusted_r2 / (1 - adjusted_r2))

print(f"Sample size: {sample_size}")
print(f"Adjusted R-squared: {adjusted_r2}")
print(f"R-squared: {model.rsquared}")
print(f"Degrees of freedom (denominator): {df_denom}")
print(f"Degrees of freedom (numerator/predictor): {df_num}")
print(f"Adjusted Cohen's f: {adjusted_cohens_f}")
print(f"Effect size (Cohen's f): {effect_size}")

# --------------------
# Power analysis with FTestPowerF2
# --------------------
Fpower_analysis = FTestPowerF2()
Fpower = Fpower_analysis.solve_power(
    effect_size=effect_size,
    df_num=df_num,
    df_denom=df_denom,
    alpha=0.05,
    power=None,
)
print(f"Power (1-β) (Cohen f): {Fpower:0.9f}")

# Sample size needed to achieve 80% power
size_needed = Fpower_analysis.solve_power(
    effect_size=effect_size,
    alpha=0.05,
    power=0.8,
    df_num=df_num,
)
print(f"Sample size needed for 80% power (Cohen f): {size_needed:.0f}")

# --------------------
# Dataframe summary
# --------------------
print("\n=== Power Analysis Summary ===\n")
results_table = pd.DataFrame({
    "Metric": [
        "Sample size (n)",
        "Adjusted R-squared",
        "R-squared",
        "Degrees of freedom (denominator)",
        "Number of predictors (numerator)",
        "Adjusted Cohen's f",
        "Effect size (Cohen's f)",
        "Power (1−β) (Cohen f)",
        "Sample size needed for 80% power (Cohen f)",
    ],
    "Value": [
        f"{sample_size:.0f}",
        f"{adjusted_r2:.2f}",
        f"{model.rsquared:.2f}",
        f"{df_denom:.0f}",
        f"{df_num:.0f}",
        f"{adjusted_cohens_f:.2f}",
        f"{effect_size:.2f}",
        f"{Fpower}"[:4],
        f"{size_needed:.0f}",
    ],
})

print(results_table.to_string(index=False))
