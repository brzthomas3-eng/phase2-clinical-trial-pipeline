import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Generating Clinical Efficacy Visual...")

# Load the ADaM dataset
advs = pd.read_csv('data/ADVS.csv')

# Filter for the Primary Endpoint: Systolic BP Change at End of Study
eos_sysbp = advs[(advs['AVISITN'] == 3) & (advs['PARAMCD'] == 'SYSBP')].copy()

# Set up the professional clinical styling
plt.figure(figsize=(9, 6))
sns.set_theme(style="whitegrid")

# Create a Boxplot comparing the Change from Baseline (CHG) between arms
ax = sns.boxplot(
    x='TRTP', 
    y='CHG', 
    data=eos_sysbp, 
    palette={"Investigational Drug": "#2ca02c", "Placebo": "#d62728"}
)

# Add a reference line at 0 (No change in blood pressure)
plt.axhline(0, color='black', linestyle='--', linewidth=1.5, alpha=0.7)

# Format the labels and title for a Clinical Study Report (CSR)
plt.title('Primary Endpoint: Change in Systolic Blood Pressure at Day 30', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Treatment Arm', fontsize=12, fontweight='bold')
plt.ylabel('Change from Baseline (mmHg)', fontsize=12, fontweight='bold')

# Save the figure to your main project folder for GitHub
plt.savefig('Efficacy_Results.png', dpi=300, bbox_inches='tight')
print("Success! Efficacy_Results.png saved to your main project folder.")