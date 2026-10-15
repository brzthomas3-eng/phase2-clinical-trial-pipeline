import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import random

print("Connecting to PostgreSQL...")
engine = create_engine('postgresql://postgres:admin123@localhost:5432/phase2_clinical_db')

NUM_PATIENTS = 200
np.random.seed(42)

print(f"Generating longitudinal trial data for {NUM_PATIENTS} patients...")

# 1. Demographics & Randomization
subjects = [f"{i:03d}" for i in range(1, NUM_PATIENTS + 1)]
arms = np.random.choice(['Investigational Drug', 'Placebo'], size=NUM_PATIENTS, p=[0.5, 0.5])
ages = np.random.randint(45, 75, size=NUM_PATIENTS)
sexes = np.random.choice(['M', 'F'], size=NUM_PATIENTS)

dm_df = pd.DataFrame({
    'subjid': subjects,
    'age': ages,
    'sex': sexes,
    'rand_arm': arms,
    'ic_date': [datetime(2026, 1, 1) + timedelta(days=random.randint(0, 30)) for _ in range(NUM_PATIENTS)]
})

# 2. Longitudinal Vitals (Injection of Treatment Effect)
vs_records = []
for index, row in dm_df.iterrows():
    subj = row['subjid']
    arm = row['rand_arm']
    base_date = row['ic_date'] + timedelta(days=random.randint(7, 14))
    patient_base_sys = np.random.normal(155, 10) 
    
    for visit_num in [1, 2, 3]:
        if visit_num == 1:
            v_date = row['ic_date'] + timedelta(days=2) 
            sys_bp = patient_base_sys + np.random.normal(0, 3)
        elif visit_num == 2:
            v_date = base_date 
            sys_bp = patient_base_sys + np.random.normal(0, 3)
        elif visit_num == 3:
            v_date = base_date + timedelta(days=30) 
            if arm == 'Investigational Drug':
                sys_bp = patient_base_sys - np.random.normal(18, 5) # Efficacy injected here
            else:
                sys_bp = patient_base_sys + np.random.normal(0, 4) 
                
        vs_records.append({
            'subjid': subj,
            'visit': f'VISIT {visit_num}',
            'visit_date': v_date.strftime('%Y-%m-%d'),
            'vs_sysbp': round(sys_bp),
            'vs_diabp': round(sys_bp - 40 + np.random.normal(0, 5))
        })

vs_df = pd.DataFrame(vs_records)

# 3. Exposure
ex_records = []
for index, row in dm_df.iterrows():
    ex_records.append({
        'subjid': row['subjid'],
        'drug_name': row['rand_arm'],
        'dose_mg': 50 if row['rand_arm'] == 'Investigational Drug' else 0,
        'start_date': (row['ic_date'] + timedelta(days=14)).strftime('%Y-%m-%d')
    })
ex_df = pd.DataFrame(ex_records)

# Push to Database
print("Injecting into clinical_staging schema...")
dm_df.to_sql('raw_demographics', engine, schema='clinical_staging', if_exists='replace', index=False)
vs_df.to_sql('raw_vitals', engine, schema='clinical_staging', if_exists='replace', index=False)
ex_df.to_sql('raw_exposure', engine, schema='clinical_staging', if_exists='replace', index=False)

print("Success! Database populated.")