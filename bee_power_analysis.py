#2024_(JEB)_power_sample_size_(cohen f)
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#STATS
from statsmodels.graphics import utils
from statsmodels.stats.power import TTestIndPower, FTestPower, TTestPower, TTestIndPower, FTestPowerF2
from statsmodels.stats.multitest import multipletests
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.graphics.regressionplots import plot_regress_exog, plot_partregress
from statsmodels.stats.power import FTestPower

# Data
file_path = 'C:/Users/rufes/Desktop/01 - (JEB) data analysis/bee_power_analysis/2025_capp_brood(protein-nutrition).xlsx'
new_df = pd.ExcelFile(file_path, engine='openpyxl')
new_df = pd.read_excel(file_path)
new_df.head(50)

# Drop NANs
new_df = new_df[new_df['Capped_Brood'].notna()]
new_df.head(50)

# Regplot capped brood vs diet type
plt.figure(figsize=(10, 6))
sns.regplot(x=new_df['Protein'], y=new_df['Capped_Brood'], scatter=True, scatter_kws={'s': 50}, line_kws={'color': 'orange', 'label': 'OLS Regression'})
plt.title('Relationship between Protein and Capped Brood')
plt.xlabel('Protein Levels')
plt.ylabel('Capped Brood')
plt.legend(loc='upper left')
plt.xticks([6, 12, 18, 25, 30], ['6', '12', '18', '25', '30'])
plt.ylim(0, 400)  # Set y-axis to start at 0
#plt.xlim(0, None)  # Set x-axis to start at 0
plt.grid(True)
plt.show()

# OLS regression using sm.ols
X_prot = new_df[['Protein']]
y_dcon = new_df['Diet_Consumption']
y_capp = new_df['Capped_Brood']
X_prot_const = sm.add_constant(X_prot)
model = sm.OLS(y_capp, X_prot_const).fit()
print(model.summary())

#Cohen's f (effect size)= r2 from the model | [ df_{denom} = n - k - 1 ] n is total sample size, k is number of predictors | df numerator (k) = 1 number of predictors protein
sample_size = len(new_df)
effect_size = np.sqrt((model.rsquared)/(1 - model.rsquared)) #Cohen's f
df_num = 1 #just one predictor
df_denom = sample_size - 1 - 1
#comparing cohens f Via adjusted rsquared(more conservative)
adjusted_r2 = model.rsquared_adj
adjusted_cohens_f = np.sqrt(adjusted_r2 / (1 - adjusted_r2))
print(f"Sample size: {sample_size}")
print(f"Adjusted R-squared: {adjusted_r2}")
print(f"R-squared: {model.rsquared}")
print(f"Degrees of freedom (denominator): {df_denom}") 
print(f"Degrees of freedom (numerator/predictor): {df_num}") #number of groups - 1
print(f"Adjusted Cohen's f: {adjusted_cohens_f}")
print(f"Effect size (Cohen's f): {effect_size}")

#Power analysis via FtestPowerF2 and Calculate the power of the test with a 27 sample size
Fpower_analysis = FTestPowerF2()
Fpower = Fpower_analysis.solve_power(effect_size, df_num, df_denom, alpha=0.05, power=None)
print(f"Power (1-β)(cohen f): {Fpower:0.9f}")
#Sample size needed to achieve a power of 0.8
size_needed = Fpower_analysis.solve_power(effect_size=effect_size, alpha=0.05, power=0.8, df_num=df_num)
print(f"Sample size needed for 80 power (cohen f): {size_needed:.0f}")

#Dataframe summary
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
        "Power (1−β) (cohen f)",
        "Sample size needed for 80% power (cohen f)"
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
        f"{size_needed:.0f}"
    ]
})

print(results_table.to_string(index=False))

