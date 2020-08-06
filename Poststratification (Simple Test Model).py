####################### 2016 CENSUS POSTSTRATIFICATION FRAME ##########################
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
    for age_ind in range(1,16):
        for sex_ind in range(0, 2):
            entry = dict({'age': age_ind, 'gender': sex_ind,'district': dist_ind})
            data.append(entry)

poststratPrelim = pd.DataFrame(data)

response_col_dict = []
for dist_ind in range(338):
    dist = distOnly[dist_ind]
    for age_ind in range(15):
        for sex_ind in range(7,9):
            count = dist.iloc[age_ind, sex_ind]
            entry = dict({'Count': count})
            response_col_dict.append(entry)

postStratResponse = pd.DataFrame(response_col_dict)

poststrat16 = poststratPrelim.join(postStratResponse)

poststrat16.to_csv("2016 Poststratification Frame (By Districts, Simple Model) (age cap 15).csv")

####################### POSTSTRATIFICATION FRAME FOR 2011 CENSUS ######################
import pandas as pd

censusProfile11 = pd.read_csv('2011CensusProfile.CSV', encoding='latin-1')
colNames = censusProfile11.columns
colTrim = ['Geo_Code', 'Prov_Name', 'FED_Name', 'Characteristic', 'Total', 'Male', 'Female']
trimData1 = censusProfile11[colTrim]

byDistricts = []
for i in range(338):
    data = trimData1.iloc[i*472:(i+1)*472]
    byDistricts.append(data)

trim = []
trim += list(range(8,12))
trim += list(range(17,31))

trimDist = []
for el in byDistricts:
    el = el.reset_index()
    del el['index']
    new_el = el.iloc[trim]
    trimDist.append(new_el)

modDist = []
for el in trimDist:
    total = el.iloc[0,4]+el.iloc[1,4]+el.iloc[2,4]
    male = el.iloc[0,5]+el.iloc[1,5]+el.iloc[2,5]
    female = el.iloc[0,6]+el.iloc[1,6]+el.iloc[2,6]
    entry = [el.iloc[0,0], el.iloc[0,1], el.iloc[0,2],  '0 to 14 years', total, male, female]
    el.loc[0] = entry
    el = el.sort_index()
    el = el.reset_index()
    del el['index']
    el = el.drop([el.index[1], el.index[2], el.index[3]])
    el = el.reset_index()
    del el['index']
    modDist.append(el)

zero = modDist[0]

data = []
for dist_ind in range(1,339):
    for age_ind in range(1,17):
        for sex_ind in range(1, 3):
            entry = dict({'age': age_ind, 'gender': sex_ind,'district': dist_ind})
            data.append(entry)

poststratPrelim = pd.DataFrame(data)

response_col_dict = []
for dist_ind in range(338):
    dist = modDist[dist_ind]
    for age_ind in range(16):
        for sex_ind in range(5,7):
            count = dist.iloc[age_ind, sex_ind]
            entry = dict({'Count': count})
            response_col_dict.append(entry)

postStratResponse = pd.DataFrame(response_col_dict)

poststrat11 = poststratPrelim.join(postStratResponse)

########################################COMBINING###############################

time_dict11 = []
time_dict16 = []
for ct in range(10816):
    entry11 = dict({'Year': 1})
    entry16 = dict({'Year': 2})
    time_dict11.append(entry11)
    time_dict16.append(entry16)

time_frame11 = pd.DataFrame(time_dict11)
time_frame16 = pd.DataFrame(time_dict16)

time_comb_poststrat11 = time_frame11.join(poststrat11)
time_comb_poststrat16 = time_frame16.join(poststrat16)

postStratFrame = pd.concat([time_comb_poststrat11, time_comb_poststrat16], axis=0)
postStratFrame = postStratFrame.reset_index()
del postStratFrame['index']

