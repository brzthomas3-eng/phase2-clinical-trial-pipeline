import pandas as pd

print("Deriving Analysis Data Model (ADVS)...")

# Load SDTM files
vs = pd.read_csv('data/SDTM_VS.csv')
dm = pd.read_csv('data/SDTM_DM.csv')

# 1. Merge Treatment Arm (TRTP) from DM into VS
advs = pd.merge(vs, dm[['USUBJID', 'ARM']], on='USUBJID', how='left')
advs.rename(columns={'ARM': 'TRTP'}, inplace=True) # TRTP = Planned Treatment

# 2. Format Analysis Values
advs['AVAL'] = pd.to_numeric(advs['VSORRES'])
advs['PARAMCD'] = advs['VSTESTCD']
advs['AVISIT'] = advs['VISIT']
advs['AVISITN'] = advs['VISITNUM']

# 3. Derive Baseline (BASE)
# In our protocol, Visit 2 is the Baseline / Day 1 visit
baseline = advs[advs['AVISITN'] == 2][['USUBJID', 'PARAMCD', 'AVAL']].copy()
baseline.rename(columns={'AVAL': 'BASE'}, inplace=True)

# Merge BASE back onto the main dataset
advs = pd.merge(advs, baseline, on=['USUBJID', 'PARAMCD'], how='left')

# 4. Calculate Change from Baseline (CHG)
advs['CHG'] = advs['AVAL'] - advs['BASE']

# Clean and order ADaM columns
advs = advs[['STUDYID', 'USUBJID', 'TRTP', 'PARAMCD', 'AVISITN', 'AVISIT', 'AVAL', 'BASE', 'CHG']]
advs = advs.sort_values(by=['USUBJID', 'PARAMCD', 'AVISITN'])

advs.to_csv('data/ADVS.csv', index=False)
print("Success! ADVS.csv saved with baseline and change calculations.")