######## POSTSTRATIFICATION FRAME FOR 2011 CENSUS ################
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
            entry = dict({'District': dist_ind, 'Age': age_ind, 'Sex': sex_ind})
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


###################### 2016 CENSUS POSTSTRATIFICATION FRAME ##########################
######## POSTSTRATIFICATION FRAME FOR 2011 CENSUS ################
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
            entry = dict({'District': dist_ind, 'Age': age_ind, 'Sex': sex_ind})
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