import pandas as pd
import numpy as np

ces2019 = pd.read_csv("CES2019.csv", encoding="latin-1")
ces2015 = pd.read_csv("CES2015_Combined_CSV.csv", encoding="latin-1")

trim19 = ['cps19_citizenship', 'cps19_yob', 'cps19_gender', 'cps19_province', 'cps19_education', 'cps19_votechoice',
          'cps19_vote_unlikely', 'cps19_v_advance', 'cps19_vote_lean', 'cps19_religion', 'cps19_sexuality',
          'cps19_employment', 'cps19_sector', 'cps19_income_number', 'cps19_income_cat']
trim15 = ['ID', 'sex_r', 'province', 'language', 'lklytovote', 'vote_for', 'vote_lean', 'vote_for_if', 'voted_for',
          'vote_lean', 'vote_for_if', 'voted_for', 'education', 'religion', 'age', 'emp_status', 'ethnic', 'income_full']

data19 = ces2019[trim19]
data15 = ces2015[trim15]

testdata = pd.read_excel("test.xls")

filenames = []
for i in range(1,353):
    filenames.append(str(i)+'.xls')

age_sex_2016 = []
for name in filenames:
    data = pd.read_excel(name)
    age_sex_2016.append(data)

##############################################################Larger Model

import pandas as pd

censusProfile16 = pd.read_csv("2016CensusProfile.csv", encoding="latin-1")
colNames = censusProfile16.columns
colTrim = [colNames[0], colNames[1], colNames[3], colNames[8], colNames[9], colNames[11], colNames[12], colNames[13]]
trimdata16 = censusProfile16[colTrim]

byDistricts = []
for i in range(352):
    dat = trimdata16.iloc[2247*i:2247*(i+1)]
    byDistricts.append(dat)

trim = []
trim = trim + list(range(0,2))
trim += list(range(7,33))
trim += list(range(690, 707))
trim += list(range(1337, 1616))
trim += list(range(1682, 1714))
trim += list(range(1864, 1869))

trimmedDistricts = []
for el in byDistricts:
    new_el = el.iloc[trim]
    trimmedDistricts.append(new_el.to_numpy())

########################################################Simplified Model

import pandas as pd
import numpy as np

censusProfile16 = pd.read_csv("2016CensusProfile.csv", encoding="latin-1")
colNames = censusProfile16.columns
colTrim = [colNames[0], colNames[1], colNames[2], colNames[3], colNames[8], colNames[9], colNames[11], colNames[12], colNames[13]]
trimdata16 = censusProfile16[colTrim]
trimdata16.columns = ['Census Year', 'Geo Code', 'Geo Level', 'Geo Name', 'Category', 'Member ID', 'Total', 'Male', 'Female']

byDistricts = []
for i in range(352):
    dat = trimdata16.iloc[2247*i:2247*(i+1)]
    byDistricts.append(dat)

trim = []
trim = trim + list(range(0,2))
trim += list(range(7,33))

trimDist = []
for el in byDistricts:
    new_el = el.iloc[trim]
    new_el = new_el.reset_index()
    del new_el['index']
    trimDist.append(new_el)

zerot = trimDist[0]

trim2 = [3]
trim2 += list(range(8,18))
trim2 += list(range(18,24))
trimDist2 = []
for el in trimDist:
    new_el = el.iloc[trim2]
    new_el = new_el.drop([new_el.index[11]])
    new_el = new_el.reset_index()
    del new_el['index']
    trimDist2.append(new_el)

zero = trimDist2[0]

districts = pd.read_csv("Districts.csv", encoding="latin-1")
i=0
nonridingIndex = []
for el in byDistricts:
    code = el.iloc[0,2]
    if code != 2:
        nonridingIndex.append(i)
    i += 1

distOnly = trimDist2.copy()
i=0
for ind in nonridingIndex:
    del distOnly[ind-i]
    i += 1

zero = distOnly[0]

#####Constructing Poststratification Frame

data = []
for dist_ind in range(1,339):
    for age_ind in range(1,17):
        for sex_ind in range(1, 3):
            entry = dict({'age': age_ind, 'gender': sex_ind,'district': dist_ind})
            data.append(entry)

poststratPrelim = pd.DataFrame(data)

response_col_dict = []
for dist_ind in range(338):
    dist = distOnly[dist_ind]
    for age_ind in range(16):
        for sex_ind in range(7,9):
            count = dist.iloc[age_ind, sex_ind]
            entry = dict({'Count': count})
            response_col_dict.append(entry)

postStratResponse = pd.DataFrame(response_col_dict)

poststrat16 = poststratPrelim.join(postStratResponse)

poststrat16.to_csv("2016 Poststratification Frame (By Districts, Simple Model).csv")



