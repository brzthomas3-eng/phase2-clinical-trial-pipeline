import pandas as pd
from sqlalchemy import create_engine

print("Connecting to PostgreSQL...")
engine = create_engine('postgresql://postgres:admin123@localhost:5432/phase2_clinical_db')

print("Extracting data...")
raw_dm = pd.read_sql("SELECT * FROM clinical_staging.raw_demographics", engine)
raw_vs = pd.read_sql("SELECT * FROM clinical_staging.raw_vitals", engine)
raw_ex = pd.read_sql("SELECT * FROM clinical_staging.raw_exposure", engine)

STUDYID = 'HTN-2026'
SITEID = '999'

# DM Domain
print("Transforming DM...")
sdtm_dm = pd.DataFrame()
sdtm_dm['STUDYID'] = STUDYID
sdtm_dm['DOMAIN'] = 'DM'
sdtm_dm['USUBJID'] = STUDYID + '-' + SITEID + '-' + raw_dm['subjid']
sdtm_dm['SUBJID'] = raw_dm['subjid']
sdtm_dm['AGE'] = raw_dm['age']
sdtm_dm['AGEU'] = 'YEARS'
sdtm_dm['SEX'] = raw_dm['sex']
sdtm_dm['ARM'] = raw_dm['rand_arm']
sdtm_dm['RFICDTC'] = pd.to_datetime(raw_dm['ic_date']).dt.strftime('%Y-%m-%d')
sdtm_dm = sdtm_dm[['STUDYID', 'DOMAIN', 'USUBJID', 'SUBJID', 'AGE', 'AGEU', 'SEX', 'ARM', 'RFICDTC']]
sdtm_dm.to_csv('data/SDTM_DM.csv', index=False)

# EX Domain
print("Transforming EX...")
sdtm_ex = pd.DataFrame()
sdtm_ex['STUDYID'] = STUDYID
sdtm_ex['DOMAIN'] = 'EX'
sdtm_ex['USUBJID'] = STUDYID + '-' + SITEID + '-' + raw_ex['subjid']
sdtm_ex['EXTRT'] = raw_ex['drug_name']
sdtm_ex['EXDOSE'] = raw_ex['dose_mg']
sdtm_ex['EXDOSU'] = 'mg'
sdtm_ex['EXSTDTC'] = pd.to_datetime(raw_ex['start_date']).dt.strftime('%Y-%m-%d')
sdtm_ex.to_csv('data/SDTM_EX.csv', index=False)

# VS Domain
print("Transforming VS...")
sdtm_vs = pd.melt(raw_vs, id_vars=['subjid', 'visit', 'visit_date'], 
                  value_vars=['vs_sysbp', 'vs_diabp'], 
                  var_name='VSTESTCD', value_name='VSORRES')
sdtm_vs['STUDYID'] = STUDYID
sdtm_vs['DOMAIN'] = 'VS'
sdtm_vs['USUBJID'] = STUDYID + '-' + SITEID + '-' + sdtm_vs['subjid']
sdtm_vs['VSTESTCD'] = sdtm_vs['VSTESTCD'].replace({'vs_sysbp': 'SYSBP', 'vs_diabp': 'DIABP'})
sdtm_vs['VISIT'] = sdtm_vs['visit']
sdtm_vs['VISITNUM'] = sdtm_vs['visit'].str.extract(r'(\d+)').astype(int) 
sdtm_vs['VSDTC'] = pd.to_datetime(sdtm_vs['visit_date']).dt.strftime('%Y-%m-%d')

sdtm_vs = sdtm_vs[['STUDYID', 'DOMAIN', 'USUBJID', 'VSTESTCD', 'VSORRES', 'VISITNUM', 'VISIT', 'VSDTC']]
sdtm_vs = sdtm_vs.sort_values(by=['USUBJID', 'VISITNUM', 'VSTESTCD'])
sdtm_vs.to_csv('data/SDTM_VS.csv', index=False)

print("Success! SDTM generation complete.")