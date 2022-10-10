"""Age and Gender data computations for the project"""
import pandas as pd
from dataclasses import dataclass

# pd.read_csv returns a DataFrame object that stores all columns of the csv file.
data = pd.read_csv('2019-2021.csv')
# store all the factors we want to investigate in the table
factors = ["REF_DATE", "Sex", "Age group", "VALUE"]
# find the column of data that corresponds to the factor we want to look at
filtered_data = data[factors]

# filter the filtered data by age group
youth_data = filtered_data.loc[filtered_data['Age group'] == '15 to 24 years']
young_adults_data = filtered_data.loc[filtered_data['Age group'] == '25 to 44 years']
mid_adults_data = filtered_data.loc[filtered_data['Age group'] == '45 to 64 years']


# Create class for each age group
@dataclass
class AgeGroup:
    """A class that stores the unemployment numbers and rates"""
    age: str
    pre_covid: dict
    covid: dict
    increase_factor: dict


# Create class for each gender group
@dataclass
class GenderGroup:
    """A class that stores the unemployment numbers and rates"""
    gender: str
    pre_covid: float
    covid: float
    increase_factor: float


# calculate the average unemployment value before the pandemic
def calculate_pre_covid(age_group: pd.DataFrame) -> dict:
    """calculate the average unemployment numbers during the year before covid (from April 2019 to April 2020)
     for each gender group at each age group and stores them in a dictionary
    """
    pre_covid_mean = {}
    both_sexes = age_group.loc[age_group['Sex'] == 'Both sexes']
    male = age_group.loc[age_group['Sex'] == 'Males']
    female = age_group.loc[age_group['Sex'] == 'Females']
    groups = {'Both sexes': both_sexes, 'Males': male, 'Females': female}
    for group in groups:
        # Stores all unemployment numbers in the gender group in a list
        lst1 = [i for i in groups[group]['VALUE']]
        precovid_unemployment = 0
        # Gets the unemployment values for the first 12 rows(this is the time range we want)
        for i in range(12):
            precovid_unemployment += lst1[i]
        pre_covid_mean[group] = precovid_unemployment / 12
    return pre_covid_mean


# calculate the average unemployment value during the pandemic
def calculate_covid(age_group: pd.DataFrame) -> dict:
    """calculate the average unemployment rate during covid (April 2020 - April 2021) for each
     gender group at each age group and stores them in a dictionary """
    covid_mean = {}
    both_sexes = age_group.loc[age_group['Sex'] == 'Both sexes']
    male = age_group.loc[age_group['Sex'] == 'Males']
    female = age_group.loc[age_group['Sex'] == 'Females']
    groups = {'Both sexes': both_sexes, 'Males': male, 'Females': female}
    for group in groups:
        lst1 = [i for i in groups[group]['VALUE']]
        covid_unemployment = 0
        for i in range(12, 25):
            covid_unemployment += lst1[i]
        covid_mean[group] = covid_unemployment / 12
    return covid_mean


# calculate the factor unemployment numbers increased by due to the pandemic
def calculate_increase(pre_covid: dict, covid: dict) -> dict:
    """calculate the increase factor in unemployment due to covid """
    dict_so_far = {}
    for gender in covid:
        dict_so_far[gender] = covid[gender] / pre_covid[gender]

    return dict_so_far


# Create a class object to calculate and store the unemployment info for each age group
y_pc = calculate_pre_covid(youth_data)
y_c = calculate_covid(youth_data)
youth = AgeGroup('15 to 24 years', y_pc, y_c, calculate_increase(y_pc, y_c))

ya_pc = calculate_pre_covid(young_adults_data)
ya_c = calculate_covid(young_adults_data)
young_adults = AgeGroup('25 to 44 years', ya_pc, ya_c, calculate_increase(ya_pc, ya_c))

ma_pc = calculate_pre_covid(mid_adults_data)
ma_c = calculate_covid(mid_adults_data)
mid_adults = AgeGroup('45 to 64 years', ma_pc, ma_c, calculate_increase(ma_pc, ma_c))

age_groups = [youth, young_adults, mid_adults]


# filter data by gender group
all_age_data = filtered_data.loc[filtered_data['Age group'] == '15 years and over']
male_data = all_age_data.loc[all_age_data['Sex'] == 'Males']
female_data = all_age_data.loc[all_age_data['Sex'] == 'Females']


# calculate the average unemployment value before the pandemic
def cal_pre_covid(gender_group: pd.DataFrame) -> float:
    """calculate the average unemployment rate the year before covid"""
    lst = [i for i in gender_group['VALUE']]
    precovid_unemployment = 0
    for i in range(12):
        precovid_unemployment += lst[i]
    return precovid_unemployment / 12


# calculate the average unemployment value during the pandemic
def cal_covid(gender_group: pd.DataFrame) -> float:
    """calculate the average unemployment rate the year during covid"""
    lst = [i for i in gender_group['VALUE']]
    covid_unemployment = 0
    for i in range(12, 25):
        covid_unemployment += lst[i]
    return covid_unemployment / 12


# Create a class object to calculate and store the unemployment info for each gender group
female = GenderGroup('Female', cal_pre_covid(female_data), cal_covid(female_data),
                     cal_covid(female_data) / cal_pre_covid(female_data))
male = GenderGroup('Male', cal_pre_covid(male_data), cal_covid(male_data),
                   cal_covid(male_data) / cal_pre_covid(male_data))

