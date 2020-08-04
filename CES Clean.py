import pandas as pd
import numpy as np

ces2019 = pd.read_csv("CES2019.csv", encoding="latin-1")
ces2015 = pd.read_csv("CES2015_Combined_CSV.csv", encoding="latin-1")

trim19 = ['cps19_citizenship', 'cps19_yob', 'cps19_gender', 'cps19_province', 'cps19_education', 'cps19_votechoice',
          'cps19_vote_unlikely', 'cps19_v_advance', 'cps19_vote_lean', 'cps19_religion', 'cps19_sexuality',
          'cps19_employment', 'cps19_sector', 'cps19_income_number', 'cps19_income_cat']
trim15 = ['ID', 'sex_r', 'province', 'language', 'lklytovote', 'vote_for', 'vote_lean', 'vote_for_if', 'voted_for',
          'vote_lean', 'vote_for_if', 'voted_for', 'education', 'religion', 'age', 'emp_status', 'ethnic', 'income_full']

trim11 = ['' ]

data19 = ces2019[trim19]
data15 = ces2015[trim15]

