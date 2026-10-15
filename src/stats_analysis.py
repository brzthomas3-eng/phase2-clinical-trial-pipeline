import pandas as pd
from scipy.stats import ttest_ind

print("Executing Phase II Statistical Analysis...\n")

advs = pd.read_csv('data/ADVS.csv')

# Filter for the Primary Endpoint: 
# Systolic Blood Pressure at End of Study (Visit 3)
eos_sysbp = advs[(advs['AVISITN'] == 3) & (advs['PARAMCD'] == 'SYSBP')].copy()

# Separate the Change (CHG) values by Treatment Arm
drug_chg = eos_sysbp[eos_sysbp['TRTP'] == 'Investigational Drug']['CHG'].dropna()
pbo_chg = eos_sysbp[eos_sysbp['TRTP'] == 'Placebo']['CHG'].dropna()

# Perform Independent T-Test
t_stat, p_val = ttest_ind(drug_chg, pbo_chg)

# Output Clinical Study Report (CSR) Summary
print("-" * 40)
print("CLINICAL STUDY REPORT: EFFICACY SUMMARY")
print("-" * 40)
print(f"Investigational Drug (N={len(drug_chg)}):")
print(f"  Mean Change from Baseline: {drug_chg.mean():.2f} mmHg")
print(f"Placebo (N={len(pbo_chg)}):")
print(f"  Mean Change from Baseline:  {pbo_chg.mean():.2f} mmHg\n")

print(f"T-Statistic: {t_stat:.2f}")
print(f"P-Value:     {p_val:.5e}")

if p_val < 0.05:
    print("\nCONCLUSION: Statistically significant reduction in blood pressure achieved.")
else:
    print("\nCONCLUSION: No statistically significant difference detected.")