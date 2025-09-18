# import libraries
import pandas as pd
import numpy as np
from calculator import *
from incentive_rate import *
from input import *


# INCENTIVE TABLE FOR VIBRANT MONTHLY
if incentive == 'vib_monthly':    
    table=pd.DataFrame()
    Incen_data= df[(df['INV_DT']>=start_date) & (df['INV_DT']<=end_date)]
    table['DMName']=Incen_data.groupby('TERRNAME')['DMNAME'].first()
    NPS = WNPS(Incen_data)
    table = pd.merge(table, NPS, on='TERRNAME',how='inner')
    
    #subsequent month NPS and acheivement calculation
    Next_data= df[(df['INV_DT']>=next_start_date) & (df['INV_DT']<=next_end_date)]
    subseqMonth = UWNPS(Next_data)
    subseqMonth = subseqMonth.rename(columns={'UWNPS':'NEXT_NPS','TGTVAL':'NEXT_TGTVAL','TGT_ACH':'NEXT_TGTACH'})    
    table = pd.merge(table, subseqMonth, on='TERRNAME',how='inner')
    
    #quater NPS and acheivement calculation
    quarter_data= df[(df['INV_DT']>=quater_start_date) & (df['INV_DT']<=quater_end_date)]
    quarter = UWNPS(quarter_data)
    quarter = quarter.rename(columns={'UWNPS':'QTR_NPS','TGTVAL':'QTR_TGTVAL','TGT_ACH':'QTR_TGTACH'})    
    table = pd.merge(table, quarter, on='TERRNAME',how='inner')
    #calculating qualifying acheivement
    table['QUALIFY_ACH'] = table['NEXT_NPS']/table['NPS']*100

    #calculating incetive percentage
    table['Incentive_rate']= table['TGT_ACH'].apply(vib_monthly_rate)

    # Apply the conditions subsequent or qualifying acheivment in calculating Incentive_Amount
    table['Incentive_Amount'] = np.where(
        ((table['NEXT_TGTACH'] > 90) | (table['QUALIFY_ACH'] > 90)) & (table['QTR_TGTACH'] > 95), 
        round(table['NPS'] * table['Incentive_rate']*1000,0), 0)
    # print(table)

    # filter incentive cases
    final_table = table[table['Incentive_Amount'] > 0]
    print(final_table)
    
else:
    pass


# INCENTIVE TABLE FOR PHARMA MONTHLY
if incentive == 'pharma_bimonthly':    
    table=pd.DataFrame()
    Incen_data= df[(df['INV_DT']>=start_date) & (df['INV_DT']<=end_date)]
    table['DMName']=Incen_data.groupby('TERRNAME')['DMNAME'].first()
    NPS = WNPS(Incen_data)
    table = pd.merge(table, NPS, on='TERRNAME',how='inner')

#current year NPS
    current_data= df[(df['INV_DT']>=current_year_start) & (df['INV_DT']<=current_year_end)]
    current_year_NPS = UWNPS(current_data)
    current_year_NPS = current_year_NPS.rename(columns={'UWNPS':'Current_NPS','TGTVAL':'Current_TGTVAL','TGT_ACH':'current_TGTACH'})    
    table = table.merge(current_year_NPS[['TERRNAME','Current_NPS']], on='TERRNAME',how='left')

#previous year NPS
    last_data= df[(df['INV_DT']>=last_year_start) & (df['INV_DT']<=last_year_end)]
    last_year_NPS = UWNPS(last_data)
    last_year_NPS = last_year_NPS.rename(columns={'UWNPS':'last_NPS','TGTVAL':'last_TGTVAL','TGT_ACH':'last_TGTACH'})    
    table = table.merge(last_year_NPS[['TERRNAME','last_NPS']], on='TERRNAME',how='left')
    table['Growth']=(table['Current_NPS']-table['last_NPS'])/table['last_NPS']*100
    
    #subsequent month NPS and acheivement calculation
    Next_data= df[(df['INV_DT']>=next_start_date) & (df['INV_DT']<=next_end_date)]
    subseqMonth = UWNPS(Next_data)
    subseqMonth = subseqMonth.rename(columns={'UWNPS':'NEXT_NPS','TGTVAL':'NEXT_TGTVAL','TGT_ACH':'NEXT_TGTACH'})    
    table = pd.merge(table, subseqMonth, on='TERRNAME',how='inner')

    #calculating incetive percentage
    table['Incentive_rate']= table['TGT_ACH'].apply(phar_bimonthly_cons_rate)

    # Apply the conditions subsequent or qualifying acheivment in calculating Incentive_Amount
    table['Incentive_Amount'] = np.where(
        (table['NEXT_TGTACH'] >= 92) & (table['Growth'] > 0), 
        round(table['NPS'] * table['Incentive_rate']*1000,0), 0)
    # print(table)

    # filter incentive cases
    final_table = table[table['Incentive_Amount'] > 0]
    # print(final_table)    
else:
    pass

# INCENTIVE TABLE FOR VIBRANT MONTHLY
if incentive == 'pharma_bimonthly_amb_bif':
    table=pd.DataFrame()
    Incen_data= df[(df['INV_DT']>=start_date) & (df['INV_DT']<=end_date)]
    table['DMName']=Incen_data.groupby('TERRNAME')['DMNAME'].first()
    NPS = WNPS(Incen_data)
    table = pd.merge(table, NPS, on='TERRNAME',how='inner')
    amb_data = Incen_data[Incen_data['PRODCODE'].isin(amb_group)]
    amb_table = UWNPS(amb_data)
    amb_table = amb_table.rename(columns={'UWNPS':'AMB_NPS','TGTVAL':'AMB_TGTVAL','TGT_ACH':'AMB_TGTACH'})    
    table = pd.merge(table, amb_table, on='TERRNAME',how='inner')

    bif_data = Incen_data[Incen_data['PRODCODE'].isin(bif_group)]
    bif_table = UWNPS(bif_data)
    bif_table = bif_table.rename(columns={'UWNPS':'BIF_NPS','TGTVAL':'BIF_TGTVAL','TGT_ACH':'BIF_TGTACH'})    
    table = pd.merge(table, bif_table, on='TERRNAME',how='inner')
    
    #subsequent month NPS and acheivement calculation
    Next_data= df[(df['INV_DT']>=next_start_date) & (df['INV_DT']<=next_end_date)]
    subseqMonth = UWNPS(Next_data)
    subseqMonth = subseqMonth.rename(columns={'UWNPS':'NEXT_NPS','TGTVAL':'NEXT_TGTVAL','TGT_ACH':'NEXT_TGTACH'})    
    table = pd.merge(table, subseqMonth, on='TERRNAME',how='inner')

    #calculating incetive percentage
    table['Incentive_rate']= table['TGT_ACH'].apply(phar_bimonthly_rupe_rate)

    # Apply the conditions subsequent or qualifying acheivment in calculating Incentive_Amount
    conditions = [(table['NEXT_TGTACH'] >= 92) & (table['BIF_TGTACH'] >=95) & (table['AMB_TGTACH'] >=90),(table['NEXT_TGTACH'] >= 92)]
    choices =[1,0.7]
    table['entitlement']=np.select(conditions, choices, default=0)
    table['Incentive_Amount'] = round(table['NPS'] * table['Incentive_rate']*table['entitlement']*1000,0)
    # print(table)

    # filter incentive cases
    final_table = table[table['Incentive_Amount'] > 0]
    # print(final_table)    
else:
    pass
          

# print(table)

# Save to CSV
# table.T.to_csv('incentive.csv', index=True)
final_table.T.to_csv('incentive.csv', index=True)

