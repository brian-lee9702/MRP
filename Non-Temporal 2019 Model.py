import pandas as pd
import numpy as np

ces2019 = pd.read_csv("CES2019.csv", encoding="latin-1")

trim19 = ['cps19_citizenship', 'cps19_yob', 'cps19_gender', 'cps19_province', 'cps19_education', 'cps19_votechoice',
          'cps19_vote_unlikely', 'cps19_v_advance', 'cps19_vote_lean', 'cps19_religion', 'cps19_sexuality',
          'cps19_employment', 'cps19_sector', 'cps19_income_number', 'cps19_income_cat', 'constituencynumber', 'constituencyname']

############################################2019 DATA CLEANING ####################################################
ptrim19 = ['cps19_yob', 'cps19_gender', 'cps19_votechoice',
          'cps19_vote_unlikely', 'cps19_v_advance', 'cps19_vote_lean', 'constituencynumber', 'constituencyname', 'cps19_income_cat']

#for i in range(23, 44):
#    entry = 'cps19_ethnicity_' + str(i)
#    ptrim19.append(entry)

data19 = ces2019[trim19]

###### Only take citizens #####
pdata19 = data19[data19['cps19_citizenship'] == 4]
pdata19 = pdata19.reset_index()
del pdata19['index']

pdata19 = pdata19[ptrim19]

###### Combine vote columns #####
pdata_vote1 = pdata19['cps19_votechoice']
for i in range(len(pdata_vote1)):
    el = pdata_vote1.iloc[i]
    if np.isnan(el) == True:
        pdata_vote1.iloc[i] = 0

pdata_vote2 = pdata19['cps19_vote_unlikely']
for i in range(len(pdata_vote2)):
    el = pdata_vote2.iloc[i]
    if np.isnan(el) == True:
        pdata_vote2.iloc[i] = 0

pdata_vote3 = pdata19['cps19_v_advance']
for i in range(len(pdata_vote3)):
    el = pdata_vote3.iloc[i]
    if np.isnan(el) == True:
        pdata_vote3.iloc[i] = 0

pdata_vote4 = pdata19['cps19_vote_lean']
for i in range(len(pdata_vote4)):
    el = pdata_vote4.iloc[i]
    if np.isnan(el) == True:
        pdata_vote4.iloc[i] = 0

add_dict = []
for i in range(36480):
   sum = pdata_vote1.iloc[i]+pdata_vote2.iloc[i]+pdata_vote3.iloc[i]+pdata_vote4.iloc[i]
   entry = dict({'Summed Vote': sum})
   add_dict.append(entry)

sum_vote_col = pd.DataFrame(add_dict)
vote_trimmed19 = pdata19[['cps19_yob', 'cps19_gender', 'constituencynumber', 'constituencyname', 'cps19_income_cat']]
CES19_data = vote_trimmed19.join(sum_vote_col)


##### Combine ethnicity columns #####


##### Manipulate income data ######
CES19_data = CES19_data.dropna(subset=['cps19_income_cat'])

##### Manipulate district data #####

districts = pd.read_csv("Districts.csv", encoding="latin-1")
districts.index = districts.index +1
districts = districts.reset_index()

districts_code = districts[['index', 'ED_CODE', 'ED_NAMEE']]

for i in range(338):
    dist_code = districts_code.iloc[i,1]
    index = districts_code.iloc[i,0]
    CES19_data.loc[CES19_data['constituencynumber'] == dist_code, 'constituencynumber'] = index

CES19_data = CES19_data.dropna(subset=['constituencynumber'])

CES19_data = CES19_data[['cps19_yob', 'cps19_gender', 'constituencynumber', 'cps19_income_cat', 'Summed Vote']]

##### Manipulate age data #####
CES19_data.loc[(CES19_data['cps19_yob'] > 0) & (CES19_data['cps19_yob'] < 15), 'cps19_yob'] = 1
CES19_data.loc[(CES19_data['cps19_yob'] > 14) & (CES19_data['cps19_yob'] < 20), 'cps19_yob'] = 2
CES19_data.loc[(CES19_data['cps19_yob'] > 19) & (CES19_data['cps19_yob'] < 25), 'cps19_yob'] = 3
CES19_data.loc[(CES19_data['cps19_yob'] > 24) & (CES19_data['cps19_yob'] < 30), 'cps19_yob'] = 4
CES19_data.loc[(CES19_data['cps19_yob'] > 29) & (CES19_data['cps19_yob'] < 35), 'cps19_yob'] = 5
CES19_data.loc[(CES19_data['cps19_yob'] > 34) & (CES19_data['cps19_yob'] < 40), 'cps19_yob'] = 6
CES19_data.loc[(CES19_data['cps19_yob'] > 39) & (CES19_data['cps19_yob'] < 45), 'cps19_yob'] = 7
CES19_data.loc[(CES19_data['cps19_yob'] > 44) & (CES19_data['cps19_yob'] < 50), 'cps19_yob'] = 8
CES19_data.loc[(CES19_data['cps19_yob'] > 49) & (CES19_data['cps19_yob'] < 55), 'cps19_yob'] = 9
CES19_data.loc[(CES19_data['cps19_yob'] > 54) & (CES19_data['cps19_yob'] < 60), 'cps19_yob'] = 10
CES19_data.loc[(CES19_data['cps19_yob'] > 59) & (CES19_data['cps19_yob'] < 65), 'cps19_yob'] = 11
CES19_data.loc[(CES19_data['cps19_yob'] > 64) & (CES19_data['cps19_yob'] < 70), 'cps19_yob'] = 12
CES19_data.loc[(CES19_data['cps19_yob'] > 69) & (CES19_data['cps19_yob'] < 75), 'cps19_yob'] = 13
CES19_data.loc[(CES19_data['cps19_yob'] > 74) & (CES19_data['cps19_yob'] < 80), 'cps19_yob'] = 14
CES19_data.loc[(CES19_data['cps19_yob'] > 79) & (CES19_data['cps19_yob'] < 85), 'cps19_yob'] = 15
CES19_data.loc[CES19_data['cps19_yob'] > 84, 'cps19_yob'] = 16

##### Add Temporal Column #####
CES19_year_dict = []
for i in range(len(CES19_data)):
    entry = dict({"Year": 1})
    CES19_year_dict.append(entry)

year_col19 = pd.DataFrame(CES19_year_dict)

CES19_data = year_col19.join(CES19_data)

CES19_data.columns = ['age', 'gender', 'district', 'income', 'vote']

CES19_data.to_csv('CES2019 MRP Frame (nontemporal, AGDI).csv')


##### Binary Model #####
CES19_bin = CES19_data.copy()

CES19_bin = CES19_bin[CES19_bin.vote < 3]
CES19_bin.loc[CES19_bin['vote'] == 1, 'vote'] = 0
CES19_bin.loc[CES19_bin['vote'] == 2, 'vote'] = 1
CES19_bin.loc[CES19_bin['gender'] == 1, 'gender'] = 0
CES19_bin.loc[CES19_bin['gender'] == 2, 'gender'] = 1

CES19_bin.to_csv("CES2019 MRP Frame (Binary).csv")

############################# 2015 DATA CLEANING ########################################

